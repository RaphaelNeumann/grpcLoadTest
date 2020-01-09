class RequestReport():
    def __init__(self, arr_report):
        self.reports = arr_report
        #create matrix whit all reponse code posibles
        self.matrix_status_report = [[] for i in range(16)]
        self.matrix_status_report_host = []
        self.arr_durations = []
        self.arr_hosts = []
        self.arr_duration_hosts = []
        self.processReport()    
    def processReport(self):
        for report in self.reports:
            cod, string = report['reponse_code']._value_
            if not report['host'] in self.arr_hosts:
                self.arr_hosts.append(report['host'])
                self.arr_duration_hosts.append([])
                self.matrix_status_report_host.append([[] for i in range(16)])
        
            self.matrix_status_report[cod].append((report['host'], report['duration'], string))
            self.matrix_status_report_host[self.arr_hosts.index(report['host'])][cod].append((report['host'], report['duration'], string))
            self.arr_durations.append(report['duration'])
            self.arr_duration_hosts[self.arr_hosts.index(report['host'])].append(report['duration'])

    def _calcLatencyDistribution(self, arrLatencies):
        arrLatencies.sort()
        result = [
            ("10%", arrLatencies[int(len(arrLatencies)*0.10)]),
            ("25%", arrLatencies[int(len(arrLatencies)*0.25)]),
            ("50%", arrLatencies[int(len(arrLatencies)*0.50)]),
            ("75%", arrLatencies[int(len(arrLatencies)*0.75)]),
            ("90%", arrLatencies[int(len(arrLatencies)*0.90)]),
            ("95%", arrLatencies[int(len(arrLatencies)*0.95)]),
            ("99%", arrLatencies[int(len(arrLatencies)*0.99)])     
        ]
        return result        
     
    def printReport(self):
        self.arr_durations.sort()
        print ("\n### GENERAL:")
        print ("  Resumo geral das requisiçõe:")
        print ("    Total: {} requisições".format(len(self.arr_durations)))
        print ("    Requisição mais lenta: {} ms".format(self.arr_durations[-1]))
        print ("    Requisição mais rapida: {} ms".format(self.arr_durations[0]))
        print ("    Média da requição: {} ms".format(  sum(self.arr_durations)/len(self.arr_durations)  ))

        print("\n  Distribuição geral por codigo de retorno:")
        for status_report in self.matrix_status_report:
            if (len(status_report)) > 0:
                host, duration, string = status_report[0]
                print ("    [{}] {} respostas".format(string.upper(), len(status_report)))
        
        print("\n  Distribuição percentil de latencia geral:")
        latency_distribution = self._calcLatencyDistribution(self.arr_durations)
        for latency_percent in latency_distribution:
            percent, latency = latency_percent
            print("     {} in: {} ms".format(percent, latency)) 

        for k, status_host in enumerate(self.arr_duration_hosts):
            self.arr_duration_hosts[k].sort()
            print ("\n### HOST [{}]:".format(self.arr_hosts[k]))
            print ("  Resumo das requisiçõe para o host [{}]:".format(self.arr_hosts[k]))
            print ("    Total: {} requisições".format(len(self.arr_duration_hosts[k])))
            print ("    Requisição mais lenta: {} ms".format(self.arr_duration_hosts[k][-1]))
            print ("    Requisição mais rapida: {} ms".format(self.arr_duration_hosts[k][0]))
            print ("    Média da requição: {} ms".format(  sum(self.arr_duration_hosts[k])/len(self.arr_duration_hosts[k])))

            print("\n  Distribuição por codigo de retorno do host [{}]:".format(self.arr_hosts[k]))
            for status_report in self.matrix_status_report_host[k]:
                if (len(status_report)) > 0:
                    host, duration, string = status_report[0]
                    print ("    [{}] {} respostas".format(string.upper(), len(status_report)))
            
            print("\n  Distribuição percentil de latencia para o host [{}]:".format(self.arr_hosts[k]))
            latency_distribution = self._calcLatencyDistribution(self.arr_duration_hosts[k])
            for latency_percent in latency_distribution:
                percent, latency = latency_percent
                print("     {} in: {} ms".format(percent, latency)) 
        