import os
import grpc
import importlib
import json
import time
from grpc_tools import protoc
from pathlib import Path
from shutil import copyfile

class GrpcRequest():
    def __init__(self, proto_file, url, request_type=False):
        self.proto_file = self._norm_proto(proto_file)
        self._build_proto()
        self._grpc = self._import_grpc()
        self._pb2 = self._import_pb2()
        self.url = url
        self.request_type  = request_type
        self.request = []


    def _build_proto(self):
        # Get root of proto folder
        inclusion_root = (os.path.dirname(os.path.abspath(self.proto_file)))
        command = [
            'grpc_tools.protoc',
            '--proto_path={}'.format(inclusion_root),
            '--python_out={}'.format(inclusion_root),
            '--grpc_python_out={}'.format(inclusion_root),
        ] + [ self.proto_file ]
        if protoc.main(command) != 0:
            sys.stderr.write('warning: {} failed'.format(command))

    def _norm_proto(self,  proto_file):    
        if proto_file.endswith('.proto'):
            file_name = Path(proto_file).stem
            dest_file = os.getcwd()  + '/.grpcLoadTest/' + file_name.replace(".", "_dot_") + '.proto'
            copyfile(proto_file, dest_file)
            return dest_file

    def _import_grpc(self):
        pb2_grpc_filename = Path(self.proto_file).stem + '_pb2_grpc'    
        return importlib.import_module(pb2_grpc_filename)
    

    def _import_pb2(self):
        pb2_filename = Path(self.proto_file).stem + '_pb2'    
        return importlib.import_module(pb2_filename)
    
    
    def streamRequest(self):
        response_code = grpc.StatusCode.OK
        time_stat = time.perf_counter()
        with grpc.insecure_channel(self.url) as channel:
            stub = self._grpc.ApiStub(channel) #TODO chamada dinamica
            interator = iter(self.request)
            try:
                responses = stub.getDiscounts(interator) #TODO chamada dinamica
            except grpc.RpcError as e:
                response_code = e.code()
            for  response in responses:
                #todo entender pq precisa desse for
                False
        time_stop = time.perf_counter()
        return {"reponse_code":response_code, "duration":(time_stop-time_stat) }
    
    def createRequester(self, json_string=False):
        str_param = ''
        if json_string:
            data = json.loads(json_string)
            params = []
            for i in data.keys():
                params.append("=".join([i, f'"{data[i]}"']))
            str_param =", ".join(params)

        if (self.request_type):
            str_request = "self._pb2.{}({})".format(self.request_type, str_param)
            self.request.append(eval(str_request))
        else:
            self.request.append(str_param)
        