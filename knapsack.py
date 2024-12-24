import random


def randomItemGen(n):
    items = []
    for i in range(n):
        items.append((random.randint(100, 1500), random.randint(100, 500)))
    return items

def DPKnapsack(items, WEIGHT=1000):
    V = [[0 for _ in range(WEIGHT+1)] for _ in range(len(items)+1)]
    for i in range(1, len(items)+1):
        for j in range(WEIGHT+1):
            if items[i-1][0] <= j:
                V[i][j] = max(V[i-1][j], items[i-1][1] + V[i-1][j - items[i-1][0]])
            else:
                V[i][j] = V[i-1][j]
    return V[len(items)][WEIGHT]

# def DPMKnapsack(items, WEIGHT=1000):
#     V = []

def validityChecker():


