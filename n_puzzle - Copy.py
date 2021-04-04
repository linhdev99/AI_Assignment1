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
            return [[0,0],[]]
        return [checkSTF(newState), newState]
    elif dir == 1:
        newState = right(state)
        if newState == 0:
            return [[0,0],[]]
        return [checkSTF(newState), newState]
    elif dir == 2:
        newState = up(state)
        if newState == 0:
            return [[0,0],[]]
        return [checkSTF(newState), newState]
    else:
        newState = down(state)
        if newState == 0:
            return [[0,0],[]]
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
    temp = 0
    ST = 0
    SF = 0
    global n
    for i in range(0, n):
        for j in range(0, n):
            if temp == state[i][j]:
                ST = ST + 1
            else:
                SF = SF + 1
            temp = temp + 1
    return [ST, SF]


def solveDFS(state):
    print(state)
    print("=====================")
    global step 
    # if (step == 100): 
    #     return 0
    cloneState = doubleState(state)
    getState = move(0, cloneState)
    curState = []
    save_state = []
    STMax = 0
    global state_used
    state_used.insert(len(state_used),state)
    if not getState[1] in state_used:
        curState = getState[1]
        STMax = getState[0][0]
    step = step + 1
    print("Step: ", step, "[dir=",0,", st=",getState[0][0],"] :", getState[1])
    for x in range(1,4):
        cloneState = doubleState(state)
        getState = move(x, cloneState)
        print("Step: ", step, "[dir=",x,", st=",getState[0][0],"] :", getState[1])
        if getState[0][0] >= STMax and not getState[1] in state_used:
            STMax = getState[0][0]
            curState = getState[1]
            
    print("=> Choose, ST = ", STMax)
    print(state,"=>",curState)
    state_used.insert(len(state_used),curState)
    print("=====================")
    # print(curState)
    if STMax == n*n:
        return curState
    elif curState == []:
        print("Can't solve!")
        return -1
    else:
        solveDFS(curState)

def main():
    print("Enter n (n > 2): ")
    global n
    # n = int(input())
    print("Initial state: ")
    n = 3
    # state = [[None] * n for x in range(n)]
    # state = [[1,4,2],[3,5,0],[6,7,8]]
    # state = [[3,1,2],[4,7,0],[6,8,5]]
    # state = [[1, 0, 2], [3, 8, 5], [4, 7, 6]]
    # state = [[4, 8, 2], [3, 1, 5], [0, 7, 6]]
    # state = [[2,3,5],[1,7,4],[6,0,8]]
    # state = [[1,2,5],[3,0,4],[6,7,8]]
    # state = [[1, 4, 2], [3, 8, 5], [0, 7, 6]]
    state = [[4, 8, 2], [3, 1, 5], [0, 7, 6]]
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