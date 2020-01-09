from threading import Thread

class RequestWorker(Thread):
    def __init__(self, requestObj, requests, bidirectional=False):
        Thread.__init__(self)
        self.request = requestObj
        self.bidirectional = bidirectional
        self.requests=requests

    def run(self):
        for x in range(self.requests):
            if self.bidirectional:
                print(self.request.streamRequest())
            else:
                print(self.request.basicRequest())