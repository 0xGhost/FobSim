import multiprocessing
import random

MemPool = multiprocessing.Queue()

index = 0

transactionList = [] # simluate injection transactions

def getRandomTransaction(timestamp = 0.0):
    temp = random.choice(transactionList)
    temp[0] = timestamp
    return temp

def copyQueueToTransactionList():
    global transactionList
    while not MemPool.empty():
        transactionList.append(MemPool.get())
    for tx in transactionList:
        #print(tx)
        MemPool.put(tx)
        
def getOldestTimeStamp():
    
     return peek_queue(MemPool)[0]

def peek_queue(queue):
    txs = []
    for i in range(queue.qsize()):
        txs.append(queue.get())
    for tx in txs:
        queue.put(tx)
    
    return txs[0]