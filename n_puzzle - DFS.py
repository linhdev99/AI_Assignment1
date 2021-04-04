import random
"""
    1 4 2
    3 - 5
    6 7 8 
    
    1 - 2   
    3 4 5
    6 7 8  
    
    - 1 2 
    3 4 5
    6 7 8   
    
    
    0 1 2
    3 8 5
    4 7 6
    
    
    state[n][n] 
"""
n = 0
step = 0
state_used = []

def doubleState(state):
    global n
    temp = [[None] * n for x in range(n)]
    for i in range(0, n):
        for j in range(0, n):
            temp[i][j] = state[i][j]
    return temp

def move(dir, state):
    if dir == 0:
        newState = left(state)
        if newState == 0:
            return [-1,[]]
        return [checkSTF(newState), newState]
    elif dir == 1:
        newState = right(state)
        if newState == 0:
            return [-1,[]]
        return [checkSTF(newState), newState]
    elif dir == 2:
        newState = up(state)
        if newState == 0:
            return [-1,[]]
        return [checkSTF(newState), newState]
    else:
        newState = down(state)
        if newState == 0:
            return [-1,[]]
        return [checkSTF(newState), newState]
    
def left(state):
    if state == []:
        return 0
    curState = doubleState(state)
    global n
    for i in range(0, n):
        for j in range(0, n):
            if curState[i][j] == 0:
                if j < n-1:
                    curState[i][j] = curState[i][j+1]
                    curState[i][j+1] = 0
                    return curState
    return 0

def right(state):
    if state == []:
        return 0
    curState = doubleState(state)
    global n
    for i in range(0, n):
        for j in range(0, n):
            if curState[i][j] == 0:
                if j > 0:
                    curState[i][j] = curState[i][j-1]
                    curState[i][j-1] = 0
                    return curState
    return 0

def up(state):
    if state == []:
        return 0
    curState = doubleState(state)
    global n
    for i in range(0, n):
        for j in range(0, n):
            if curState[i][j] == 0:
                if i < n-1:
                    curState[i][j] = curState[i+1][j]
                    curState[i+1][j] = 0
                    return curState
    return 0

def down(state):
    if state == []:
        return 0
    curState = doubleState(state)
    global n
    for i in range(0, n):
        for j in range(0, n):
            if curState[i][j] == 0:
                if i > 0:
                    curState[i][j] = curState[i-1][j]
                    curState[i-1][j] = 0
                    return curState
    return 0

def checkSTF(state):
    temp = [[0,1,2],[3,4,5],[6,7,8]]
    # temp = [[1,2,3],[8,0,4],[7,6,5]]
    SF = 0
    global n
    for i in range(0, n):
        for j in range(0, n):
            if temp[i][j] != state[i][j]:
                SF = SF + 1
    return SF


def solveDFS(state):
    print(state)
    print("=====================")
    global step 
    if (step == 500):
        print("can't solve") 
        return 0
    cloneState = doubleState(state)
    getState = move(0, cloneState)
    curState = []
    SF = []
    step = step + 1
    for x in range(0,4):
        cloneState = doubleState(state)
        getState = move(x, cloneState)
        print("Step: ", step, "[dir=",x,", st=",getState[0],"] :", getState[1])
        if getState[1] != []:
            SF.append(getState[0])
            curState.append(getState[1])
            
    # idx = random.randint(0,len(curState)-1)
    idx = len(curState)-1
    print("=> Choose", curState[idx])
    print(state,"=>",curState[idx])
    print("=====================")
    # print(curState)
    if SF[idx] == 0:
        return curState[idx]
    else:
        solveDFS(curState[idx])

def main():
    print("Enter n (n > 2): ")
    global n
    # n = int(input())
    print("Initial state: ")
    n = 3
    state = [[3,1,2],[6,4,5],[0,7,8]]
    # state = [[None] * n for x in range(n)]
    # state = [[1,4,2],[3,5,0],[6,7,8]]
    # state = [[0,2,3],[1,4,5],[8,7,6]]
    # state = [[3,1,2],[4,7,0],[6,8,5]]
    # state = [[1, 0, 2], [3, 8, 5], [4, 7, 6]]
    # state = [[4, 8, 2], [3, 1, 5], [0, 7, 6]]
    # state = [[2,3,5],[1,7,4],[6,0,8]]
    # state = [[1,2,5],[3,0,4],[6,7,8]]
    # state = [[1, 4, 2], [3, 8, 5], [0, 7, 6]]
    # state = [[4, 8, 2], [3, 1, 5], [0, 7, 6]]
    # print(state)
    # for i in range(0, n):
    #     for j in range(0, n):
    #         print("S[",i+1,"][",j+1,"] = ")
    #         state[i][j] = int(input())
    print(state)
    solveDFS(state)
    return 0

if __name__ == "__main__":
    main()