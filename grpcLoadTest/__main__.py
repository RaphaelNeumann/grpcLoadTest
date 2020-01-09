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
    parser = argparse.ArgumentParser('grpcLoadTest')
    parser.add_argument("--proto", required=True, help="O arquivo .pro (The Protocol Buffer) OBS: Necessário estar no mesmo diretorio que o arquivo .proto")
    parser.add_argument("--call", required=True, help="Methodo que deve ser chamado via gRPC no formato 'package.Service.Method'")
    parser.add_argument('-H', '--hosts', nargs='+',action='store', dest='hosts', help="<hosts> Lista dos hosts e porta a serem testados separados por spaço no fomrmato '<ip_or_dns>:<port>' ex.: '--host localhost:5001 localhost:5002'", required=True)
    parser.add_argument("--request_type", default=False, help='Tipo de request a ser utilizado para criar o parametro de chamada')
    parser.add_argument("--data", action='store', dest='data', default=False, help="Dados de parametros escrito na forma de json ex: \"--data '{\"product_id\":\"GyhyFM3T3U88mg4d\",\"user_id\":\"8PiisPOauwPZzWTT\"}'\"")
    parser.add_argument("--bidirectional",action='store_true', default=False, help="A requisição é do tipo bidirecional?")
    parser.add_argument("--threads", default=10, help= 'Numero de threads/chamadas em concorrencias. valor padrão: 10. Obs esse numero não deve ser maior que o numero de requisições')
    parser.add_argument("--requests", default=200, help="Numero de requisições para cada URL. valor padrão: 200", type=int)
 
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


