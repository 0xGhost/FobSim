import multiprocessing
import random

MemPool = multiprocessing.Queue()

index = 0

transactionList = [] # simluate injection transactions

def getRandomTransaction():
    return random.choice(transactionList)

def copyQueueToTransactionList():
    global transactionList
    while not MemPool.empty():
        transactionList.append(MemPool.get())
        