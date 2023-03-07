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
        