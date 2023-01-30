import uuid
from datetime import datetime

class Transactions:
    def __init__(self,c,send,rec):
        self.coin=c
        self.senderid=send
        self.receiverid=rec
        self.transcationsize=1
        self.transactionTS=datetime.now().timestamp()
        self.transactionid=uuid.uuid1().hex
    def __str__(self):
        string= str(self.transactionid) + ": "+ str(self.senderid) + " pays " + str(self.receiverid)+ " "+ str(self.coin)+ " coins."
        return string