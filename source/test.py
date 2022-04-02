import time

x1 =float(input("x1"))
x2 =float(input("x2"))
y1 =float(input("y1"))
y2 =float(input("y2"))
for i in range(10):
    time.sleep(0.1)
    d = 1-(10-i)/10
    board = [[" "]*8 for i in range(8)]
    board[round(abs(x1+(d*x2)-(d*x1)))][round(abs(y1+(d*y2)-(d*y1)))] = "B"
    for j in range(len(board)): 
        print(str(board[j])+"\n")
    print("\n")