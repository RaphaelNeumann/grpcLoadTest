import sys
import os
import argparse
import time
import threading
import grpc
from enum import IntEnum
from .GrpcRequest import GrpcRequest
from .RequestWorker import RequestWorker
from .RequestReport import RequestReport

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--proto", required=True, help="Proto file")
    parser.add_argument("--call", required=True, help="Methodo que deve ser chamado via gRPC")
    parser.add_argument('-H', '--hosts', nargs='+',action='store', dest='hosts', help="Lista dos hosts a serem testados", required=True)
 
    parser.add_argument("--request_type", default=False)
    parser.add_argument("--data", action='store', dest='data', default=False)
    parser.add_argument("--bidirectional",action='store_true', default=False, help='A requisição deve ser bidirectional')
    parser.add_argument("--threads", default=10, help="Numero de Threads", type=int)
    parser.add_argument("--requests", default=200, help="Numero de requisições para cada URL", type=int)
 
    args = parser.parse_args()   
    start_time = time.perf_counter()

    request = GrpcRequest(args.proto, args.call, args.hosts, args.request_type)
    arr_reports = []
    if args.data:
        request.createRequester(json_string=args.data)
    else:
        request.createRequester()
    
    # Set number of threads
    for x in range(args.threads):
        worker = RequestWorker(request, int(args.requests/args.threads), arr_reports, args.bidirectional)
        worker.start()
    
    #Wait for all thread finish
    while(len(threading.enumerate()) > 1):
        False
    report = RequestReport(arr_reports)
    report.printReport()
  

if __name__ == '__main__':
    main()


