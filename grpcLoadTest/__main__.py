import sys
import os
import argparse
from .GrpcRequest import GrpcRequest

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--proto")
    parser.add_argument("--request_type", default=False)
    args = parser.parse_args()
    request = GrpcRequest(args.proto, 'localhost:5001', request_type=args.request_type)
    request.createRequest('{"product_id":"GyhyFM3T3U88mdasdg4d-", "user_id":"8PiisadasdsPOauwPZzWTT"}')
    request.streamRequest()

if __name__ == '__main__':
    main()
