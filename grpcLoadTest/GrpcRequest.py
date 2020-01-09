import os
import pkg_resources
import sys
import grpc
import importlib
import json
import time
import random
from grpc_tools import protoc
from pathlib import Path
from shutil import copyfile

class GrpcRequest():
    def __init__(self, proto_file, call, url, requester_type=False):
        self.proto_file = proto_file
        #command.build_package_protos(os.path.dirname(os.path.abspath(self.proto_file)))
        self._build_proto()
        self._grpc = self._import_grpc()
        self._pb2 = self._import_pb2()
        self.url = url
        self.call = call
        
        self.requester_type  = requester_type
        self.requests = []

        if call:
            arr_call = self.call.split('.')
            self.stubName = arr_call[len(arr_call)-2]+'Stub'
            self.requestName = arr_call[len(arr_call)-1]
        else:
            raise Exception('error: argument call is nescessary')

        if not url:
            raise Exception('error: argument host is nescessary')


    def _build_proto(self):
        # Get root of proto folder
        inclusion_root = (os.path.dirname(os.path.abspath(self.proto_file)))
        command = [
            'grpc_tools.protoc',
            '--proto_path={}'.format(inclusion_root),
            '--python_out={}/.grpcLoadTest'.format(inclusion_root),
            '--grpc_python_out={}/.grpcLoadTest'.format(inclusion_root),
        ] + [ self.proto_file ]

        
        if protoc.main(command) != 0:
            sys.stderr.write('warning: {} failed'.format(command))
            exit(1)

    def _norm_grpc(self,  grpc_file):
        inclusion_root = (os.path.dirname(os.path.abspath(self.proto_file))) + '/.grpcLoadTest/'    
        file_name = Path(inclusion_root+grpc_file).stem
        dest_file = file_name.replace(".", "_dot_") + '.py'
        copyfile(inclusion_root+grpc_file, inclusion_root+dest_file)
        return dest_file

    def _import_grpc(self):
        pb2_grpc_filename = self._norm_grpc(Path(self.proto_file).stem + '_pb2_grpc.py')
        grpc_name = Path(pb2_grpc_filename).stem
        return importlib.import_module(grpc_name)
    

    def _import_pb2(self):
        pb2_filename = Path(self.proto_file).stem + '_pb2'    
        return importlib.import_module(pb2_filename)
    

    def streamRequest(self):
        response_code = grpc.StatusCode.OK
        time_stat = time.perf_counter()
        url = random.choice(self.url)
        with grpc.insecure_channel(url) as channel:
            str_stub = "self._grpc.{}(channel)".format(self.stubName)
            stub = eval(str_stub)
            interator = iter(self.requests)
            try:
                str_response = "stub.{}(interator)".format(self.requestName)
                responses = eval(str_response)
                for  response in responses:
                    #TODO entender pq precisa desse for
                    False
            except grpc.RpcError as e:
                response_code = e.code()
            
        time_stop = time.perf_counter()
        return {"reponse_code":response_code, "duration":(time_stop-time_stat)*1000, "host":url }
    
    def basicRequest(self):
        response_code = grpc.StatusCode.OK
        time_stat = time.perf_counter()
        url = random.choice(self.url)
        channel = grpc.insecure_channel(url)
        str_stub = "self._grpc.{}(channel)".format(self.stubName)
        stub = eval(str_stub)
        if (len(self.requests)  > 0):
            for request in self.requests:
                try:
                    str_response = "stub.{}(request)".format(self.requestName)
                    responses = eval(str_response)
                except grpc.RpcError as e:
                    response_code = e.code()
        else:
            try:
                str_response = "stub.{}}()".format(self.requestName)
                responses = eval(str_response)
            except grpc.RpcError as e:
                response_code = e.code()
        time_stop = time.perf_counter()
        return {"reponse_code":response_code, "duration":(time_stop-time_stat)*1000, "host":url }
    

    def createRequester(self, json_string=False):
        str_param = ''
        if json_string:
            data = json.loads(json_string)
            params = []
            for i in data.keys():
                params.append("=".join([i, f'"{data[i]}"']))
            str_param =", ".join(params)
        if (self.requester_type):
            str_requester = "self._pb2.{}({})".format(self.requester_type, str_param)
            self.requests.append(eval(str_requester))
        else:
            self.requests.append(str_param)
        