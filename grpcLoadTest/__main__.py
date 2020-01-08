import sys
import os
import argparse
import grpc
from grpc_tools import protoc
from pathlib import Path
from shutil import copyfile
import importlib

def main():
    parser = argparse.ArgumentParser(description='test')
    parser.add_argument("--proto")
    args = parser.parse_args()
    proto_file = normalize_proto(args.proto)
    build_proto(proto_file)

    pb2_grpc_filename = Path(proto_file).stem + '_pb2_grpc'    
    pb2_grpc = importlib.import_module(pb2_grpc_filename)

    pb2_filename = Path(proto_file).stem + '_pb2'    
    pb2 = importlib.import_module(pb2_filename)
    
    with grpc.insecure_channel('localhost:5001') as channel:
        stub = pb2_grpc.ApiStub(channel)

        discounts = [
            pb2.GetDiscountsRequest(product_id='GyhyFM3T3U88mg4d',user_id='8PiisPOauwPZzWTT'),
        ]
        myit = iter(discounts)
        
        responses = stub.getDiscounts(myit, timeout=30) #TODO chamada dinamica
        for reply in responses:
            print (reply.pct)



def build_proto(proto_file, strict_mode=False):

    # Get root of proto folder
    inclusion_root = (os.path.dirname(os.path.abspath(proto_file)))

    command = [
        'grpc_tools.protoc',
        '--proto_path={}'.format(inclusion_root),
        '--python_out={}'.format(inclusion_root),
        '--grpc_python_out={}'.format(inclusion_root),
    ] + [ proto_file ]
    if protoc.main(command) != 0:
        sys.stderr.write('warning: {} failed'.format(command))

def normalize_proto(proto_file):
    if proto_file.endswith('.proto'):
        file_name = Path(proto_file).stem
        dest_file = os.getcwd()  + '/.grpcLoadTest/' + file_name.replace(".", "_dot_") + '.proto'
        copyfile(proto_file, dest_file)
        return dest_file

if __name__ == '__main__':
    main()
