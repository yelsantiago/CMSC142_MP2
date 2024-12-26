import random
import time
import sys
import numpy as np 

sys.setrecursionlimit(100000000)

def randomItemGen(n):
    items = []
    for _ in range(n):
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
    return V[len(items)][WEIGHT], V

def DPMFKnapsack(items, WEIGHT=1000):
    V = [[-1 for _ in range(WEIGHT+1)] for _ in range(len(items)+1)]
    for i in range(WEIGHT+1):
        V[0][i] = 0
    for j in range(len(items)+1):
        V[j][0] = 0
    def recurse(i, j):
        if V[i][j] < 0:
            if j < items[i-1][0]:
                value = recurse(i-1, j)
            else:
                value = max(recurse(i-1, j), items[i-1][1] + recurse(i-1, j - items[i-1][0]))
            V[i][j] = value
        return V[i][j]
    recurse(len(items), WEIGHT)
    return V[len(items)][WEIGHT], V

def DPKnapsackBacktracking(items, DP, WEIGHT=1000):
    included = []
    for i in range(len(items), 0, -1):
        if DP[i][WEIGHT] != DP[i - 1][WEIGHT]:
            included.append(items[i - 1])
            WEIGHT -= items[i - 1][0]
    included.reverse()
    return included

def LVGreedyKnapsack(items, WEIGHT=1000):
    arr = items.copy()
    arr.sort(key=lambda tup: tup[1], reverse=True)
    total_value = 0
    included = []
    while arr and WEIGHT != 0:
        if arr[0][0] <= WEIGHT:
            WEIGHT -= arr[0][0]
            total_value += arr[0][1]
            included.append(arr)
            arr.pop(0)
        else:
            arr.pop(0)
    return total_value, included

def SWGreedyKnapsack(items, WEIGHT = 1000):
    arr = items.copy()
    arr.sort(key=lambda tup: tup[0])
    total_value = 0
    included = []
    while arr and WEIGHT != 0:
        if arr[0][0] <= WEIGHT:
            WEIGHT -= arr[0][0]
            total_value += arr[0][1]
            included.append(arr)
            arr.pop(0)
        else:
            arr.pop(0)
    return total_value, included
    
def VRGreedyKnapsack(items, WEIGHT=1000):
    ratio = []
    for item in items:
        temp = item + (item[1]/item[0],)
        ratio.append(temp)
    ratio.sort(key=lambda tup: tup[2], reverse=True)
    value = 0
    included = []
    while ratio and WEIGHT != 0:
        if ratio[0][0] <= WEIGHT:
            value = value + ratio[0][1]
            WEIGHT = WEIGHT - ratio[0][0]
            included.append((ratio[0][0], ratio[0][1]))
            ratio.pop(0)
        else:
            ratio.pop(0)
    return value, included

def validityChecker():
    items1 = [(2, 12), (1, 10), (3, 20), (2, 15)]
    print(DPKnapsack(items1, 5))
    print(DPMFKnapsack(items1, 5))
    DP = DPKnapsack(items1, 5)[1]
    print(DPKnapsackBacktracking(items1, DP, 5))
    print(LVGreedyKnapsack(items1,5))
    print(SWGreedyKnapsack(items1,5))
    print(VRGreedyKnapsack(items1, 5))
    
def algo_runtime(algorithm, items):
    start = time.time()
    result = algorithm(items)
    end = time.time()
    return(end-start)* 10**3, result[0], result[1]

def experimentParameters():
    algorithms = [
        ('DPKnapsack', DPKnapsack),
        ('DPMFKnapsack', DPMFKnapsack),
        ('LargestValueKnapsack',LVGreedyKnapsack),
        ('SmallestWeightKnapsack', SWGreedyKnapsack),
        ('ValueRatioKnapsack', VRGreedyKnapsack)
    ]
    
    num_runs = 3
    results = {algo[0]: [] for algo in algorithms}

    i = 100
    while i <= 100000:
        print(f"\nTest for {i} items...")
        items = randomItemGen(i)
        print(f"{'Algorithm':<30}{'Computed Value':<20}{'Trial 1':<20}{'Trial 2':<20}{'Trial 3':<20}{'Ave. Runtime':<20}")
        for name, algorithm in algorithms:
            times = []
            for _ in range(num_runs):
                result = algo_runtime(algorithm, items)
                run_time = result[0]
                times.append(run_time)
                
            avg_runtime = np.mean(times)
            results[name].append(avg_runtime)
        
            print(f"{name:<30}{result[1]:<20}{times[0]:<20}{times[1]:<20}{times[2]:<20}{avg_runtime:<20} ")
                
        i = i * 10 
    
    print("\nResults (ms):")
    print(f"{'Algorithm':<20}", end="")
    print("100       1000      10000     100000")
    for name in algorithms:
        avg_times = results[name[0]]
        print(f"{name[0]:<20}", end="")
        for time in avg_times:
            print(f"{time:<10.2f}", end="")
        print()
        
validityChecker()
experimentParameters()
