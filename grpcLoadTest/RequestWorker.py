from threading import Thread

class RequestWorker(Thread):
    def __init__(self, requestObj, requests, report, bidirectional=False):
        Thread.__init__(self)
        self.request = requestObj
        self.bidirectional = bidirectional
        self.requests=requests
        self.report=report

    def run(self):
        for x in range(self.requests):
            if self.bidirectional:
                self.report.append(self.request.streamRequest())
            else:
                self.report.append(self.request.basicRequest())