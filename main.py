from flask import Flask
from collections import deque as dq
import threading

app = Flask(__name__)

k_id = 0
l = -1
mp = {}
branches = []
att = []

def left(ind, k_id):
    if (ind * 2) + 1 < k_id:
        return ind * 2 + 1
    return -1

def right(ind, k_id):
    if (ind * 2) + 2 < k_id:
        return ind * 2 + 2
    return -1

def ins():
    global k_id, l
    for i in att:
        v = input(f"enter value for attribute {i} : ")
        branches.append(v)
    if k_id == 0:
        l = 0
    k_id += 1

def kfind(uid, branches, f, t):
    if l != -1:
        i, j = 0, k_id
        while i <= j:
            mid = (i + j) // 2
            if mid > uid:
                j = mid - 1
            elif mid < uid:
                i = mid + 1
            else:
                if f == 1:
                    print(branches[(mid * n):(mid * n) + n])
                    break
                else:
                    print(branches[mid * n + mp[t]])
                    break

def bcheck(ind, branches, bname):
    return branches[(ind * n) + mp[bname]]

def kdel(uid):
    i = uid * n
    for q in range(n):
        print(i)
        branches.pop(i)

def kscan(branches, wc, cond, bname, f):
    if l != -1:
        d = dq([0])
        while d:
            z = d.popleft()
            lft, rgt = left(z, k_id), right(z, k_id)
            if f == 0:
                print(branches[(z * n):(z * n) + n])
            elif f == 1:
                if bcheck(z, branches, wc) == cond:
                    print(branches[(z * n):(z * n) + n])
            else:
                if bcheck(z, branches, wc) == cond:
                    print(bcheck(z, branches, bname))
            if lft != -1:
                d.append(lft)
            if rgt != -1:
                d.append(rgt)

def krypton():
    global n
    n = int(input("enter number of attributes : "))
    for i in range(n):
        s = input("enter attribute name : ")
        att.append(s)
        mp[s] = i

    while True:
        print("1. Input data")
        print("2. Search data")
        print("3. Scan data")
        print("4. Delete data")
        print("5. Exit")

        a = int(input())

        if a == 1:
            ins()
        elif a == 2:
            print("1. Entire branch")
            print("2. Target field")
            f = int(input())
            gurt = int(input("enter id to search : "))
            if f == 1:
                kfind(gurt, branches, f, "")
            else:
                target = input("enter target attribute name : ")
                kfind(gurt, branches, f, target)
        elif a == 3:
            print("1. scan entire")
            print("2. scan branches with condition")
            print("3. Scan fields with condition")

            f = int(input())

            if f == 1:
                kscan(branches, "", "", "", 0)
            elif f == 2:
                bn = input("enter attribute name : ")
                wc = input("enter attributer for where clause : ")
                co = input("enter condition : ")
                kscan(branches, wc, co, bn, 1)
            else:
                bn = input("enter attribute name : ")
                wc = input("enter attributer for where clause : ")
                co = input("enter condition : ")
                kscan(branches, wc, co, bn, 2)
        elif a == 4:
            uid = int(input("enter uid to delete : "))
            kdel(uid)
            k_id -= 1
        else:
            break

# Run krypton in a thread so it doesn't block Flask
def run_krypton():
    krypton()

@app.route("/")
def start_krypton():
    threading.Thread(target=run_krypton).start()
    return "Krypton started in terminal. Check your console."

if __name__ == "__main__":
    app.run(debug=True)
