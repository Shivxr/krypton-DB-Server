from flask import Flask, request, jsonify
from collections import deque as dq

app = Flask(__name__)

k_id = 0
l = -1
mp = {"":""}
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

@app.route('/initialize', methods=['POST'])
def initialize():
    global k_id
    global l
    data = request.get_json()  # Expecting data in JSON format
    for i in data['attributes']:
        s = i
        att.append(s)
        mp[s] = len(mp)-1
    return jsonify({"message": "Attributes initialized successfully"}), 200

@app.route('/insert', methods=['POST'])
def insert_data():
    global k_id
    global l
    data = request.get_json()
    new_branch = data['branch']
    branches.extend(new_branch)

    if k_id == 0:
        l = 0
    k_id += 1

    return jsonify({"message": "Data inserted successfully"}), 200

@app.route('/search/<int:uid>', methods=['GET'])
def search(uid):
    global branches
    result = {}
    if l != -1:
        i, j = 0, k_id
        while i <= j:
            mid = (i + j) // 2
            if mid > uid:
                j = mid - 1
            elif mid < uid:
                i = mid + 1
            else:
                return jsonify(branches[(mid * len(att)):(mid * len(att)) + len(att)]),200

@app.route('/delete/<int:uid>', methods=['DELETE'])
def delete(uid):
    global branches
    i = uid * len(att)
    branches.pop(i)
    return jsonify({"message": "Data deleted successfully"}), 200

@app.route('/scan', methods=['GET'])
def kscan():

    scan_type = int(request.args.get('scan_type', 1))
    where_column = request.args.get('where_column', '')
    condition = request.args.get('condition', '')
    bname = request.args.get('bname', '')
    f = scan_type
    results = []
    if l!= -1:
        d = dq([0])
        while d:
            z = d.popleft()
            lft, rgt = left(z, k_id), right(z, k_id)

            if f == 1:
                # Entire scan: return the whole branch
                results.append(branches[(z * len(att)):(z * len(att)) + len(att)])
            elif f == 2:
                # Scan branches with condition
                if bcheck(z, where_column) == condition:
                    results.append(branches[(z * len(att)):(z * len(att)) + len(att)])
            else:
                # Scan fields with condition
                if bcheck(z, where_column) == condition:
                    results.append(bcheck(z, bname))

            if lft != -1:
                d.append(lft)
            if rgt != -1:
                d.append(rgt)

    return jsonify({"results": results}), 200

 

def bcheck(ind, bname):
    return branches[(ind * len(att)) + mp[bname]]

if __name__ == '__main__':
    app.run(debug=True)
