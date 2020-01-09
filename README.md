# grpcLoadTest
Simples applicação python cli para realizar teste de cargas utilizando requisições [gRCP](http://grpc.io)

# Instação
```bash
git clone https://github.com/RaphaelNeumann/grpcLoadTest.git
cd grpcLoadTest.git
sh install.sh
```

# Utilização
```bash
usage: grpcLoadTest [-h] --proto PROTO --call CALL -H HOSTS [HOSTS ...]
                    [--request_type REQUEST_TYPE] [--data DATA]
                    [--bidirectional] [--threads THREADS]
                    [--requests REQUESTS]

optional arguments:
  -h, --help            show this help message and exit
  --proto PROTO         O arquivo .pro (The Protocol Buffer) OBS: Necessário
                        estar no mesmo diretorio que o arquivo .proto
  --call CALL           Methodo que deve ser chamado via gRPC no formato
                        'package.Service.Method'
  -H HOSTS [HOSTS ...], --hosts HOSTS [HOSTS ...]
                        <hosts> Lista dos hosts e porta a serem testados
                        separados por spaço no fomrmato '<ip_or_dns>:<port>'
                        ex.: '--host localhost:5001 localhost:5002'
  --request_type REQUEST_TYPE
                        Tipo de request a ser utilizado para criar o parametro
                        de chamada
  --data DATA           Dados de parametros escrito na forma de json ex: "--
                        data '{"product_id":"GyhyFM3T3U88mg4d","user_id":"8Pii
                        sPOauwPZzWTT"}'"
  --bidirectional       A requisição é do tipo bidirecional?
  --threads THREADS     Numero de threads/chamadas em concorrencias. valor
                        padrão: 10. Obs esse numero não deve ser maior que o
                        numero de requisições
  --requests REQUESTS   Numero de requisições para cada URL. valor padrão: 200
```

# Exemplo
```bash
grpcLoadTest --prot discounts.api.v1.proto --call discounts.Api.getDiscounts --host localhost:5001 localhost:5002 --bidirection --request_type=GetDiscountsRequest --data '{"product_id":"GyhyFM3T3U88mg4d","user_id":"8PiisPOauwPZzWTT"}'

### GENERAL:
  Resumo geral das requisiçõe:
    Total: 200 requisições
    Requisição mais lenta: 55.19344800000003 ms
    Requisição mais rapida: 1.4959090000000175 ms
    Média da requição: 11.264353309999997 ms

  Distribuição geral por codigo de retorno:
    [OK] 87 respostas
    [UNIMPLEMENTED] 113 respostas

  Distribuição percentil de latencia geral:
     10% in: 5.252896000000007 ms
     25% in: 6.115189999999993 ms
     50% in: 8.065310999999964 ms
     75% in: 11.897342000000005 ms
     90% in: 25.70549800000005 ms
     95% in: 30.088696 ms
     99% in: 51.00280400000001 ms

### HOST [localhost:5002]:
  Resumo das requisiçõe para o host [localhost:5002]:
    Total: 113 requisições
    Requisição mais lenta: 46.92954799999999 ms
    Requisição mais rapida: 1.4959090000000175 ms
    Média da requição: 8.219214867256637 ms

  Distribuição por codigo de retorno do host [localhost:5002]:
    [UNIMPLEMENTED] 113 respostas

  Distribuição percentil de latencia para o host [localhost:5002]:
     10% in: 4.611166999999972 ms
     25% in: 5.474484000000002 ms
     50% in: 6.565386000000006 ms
     75% in: 7.690933000000011 ms
     90% in: 10.749600999999998 ms
     95% in: 22.617756000000018 ms
     99% in: 46.632787999999984 ms

### HOST [localhost:5001]:
  Resumo das requisiçõe para o host [localhost:5001]:
    Total: 87 requisições
    Requisição mais lenta: 55.19344800000003 ms
    Requisição mais rapida: 5.327315999999971 ms
    Média da requição: 15.219533126436783 ms

  Distribuição por codigo de retorno do host [localhost:5001]:
    [OK] 87 respostas

  Distribuição percentil de latencia para o host [localhost:5001]:
     10% in: 7.5614610000000475 ms
     25% in: 9.736351000000031 ms
     50% in: 11.719428000000004 ms
     75% in: 15.335042000000021 ms
     90% in: 28.91918900000001 ms
     95% in: 33.16833400000002 ms
     99% in: 55.19344800000003 ms
```