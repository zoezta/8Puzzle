# Wildan Pratama
# 201753058

import random
from operator import itemgetter
import time

# emoji untuk mempercantik tampilan
beautyemoji = {
    0: "    ",
    1: " 1️⃣ ",
    2: " 2️⃣ ",
    3: " 3️⃣ ",
    4: " 4️⃣ ",
    5: " 5️⃣ ",
    6: " 6️⃣ ",
    7: " 7️⃣ ",
    8: " 8️⃣ "
}
# fungsi untuk print tiles dengan emoji
def drawTiles(state):
    separator = '\n' + '+----------------' + '+\n'
    grid = separator
    for x in tiles:
        for index, y in enumerate(x):
            grid += "|" + beautyemoji[state[y]] #str(state[y] if state[y] !=0 else '_')
            if index == (len(x) - 1):
                grid += "|" + separator
        print(grid)

# membuat array 2 dimensi 3X3
# [[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 0], [2, 1], [2, 2]]
# Membuat data neighbour untuk setiap node
# {(0, 0): [(1, 0), (0, 1)], dst...}
tiles = []
neighbours = {}
column = 3
row = 3
for x in range(row):
    tiles.append([])
    for y in range(column):
        tiles[x].append((x,y))
        # mencari neighbours
        neighbours[(x,y)] = []

        right = (x + 1, y)
        # check edge
        if right[0] <= (row - 1):
            neighbours[(x,y)].append(right)

        left = (x - 1, y)
        # check edge
        if left[0] > -1:
            neighbours[(x, y)].append(left)

        up = (x,y - 1)
        # check edge
        if up[1] > -1:
            neighbours[(x, y)].append(up)

        down = (x, y + 1)
        # check edge
        if down[1] <= (column -1):
            neighbours[(x, y)].append(down)

# Membuat Goal State

goalstate = {}
i = 1
for tile in tiles:
    for t in tile:
        goalstate[t] = 0 if i >= 9 else i
        i+=1


values = list(goalstate.values())
#randomvalues = [1,0,8,2,7,6,3,4] # manual start state
randomvalues = random.sample(values,len(values))

#membuat start state
#contoh: {(0,0): 3, (0,1): 0, (0,2): 8,}

startstate = { tile: randomvalues[index] for index,tile in enumerate(goalstate.keys())}

#print start state (soal)
print("Soal:")
drawTiles(startstate)

#cek start startsate ada solusinya atau tidak dengan mencari nilai inversi
startstatevalue = [value for key,value in startstate.items() if value > 0]
inv_count = 0
for i in range(0, len(startstatevalue)) :
    for j in range(i + 1, len(startstatevalue)) :
        if (startstatevalue[j] > startstatevalue[i]) :
            inv_count +=1

#cek apakah inv_count ganjil, jika ganjil berarti puzzle tidak bisa diselesaikan
if inv_count % 2 > 0:
    print("Puzzle Tidak ada Solusinya! Coba Lagi !")
    exit()

#Tukar goalstate key dan value
swapgoalstate = dict([(value, key) for key, value in goalstate.items()])

#Buat start node
startnode = list(startstate.keys())[list(startstate.values()).index(0)]

#inisiasi currentstate yang akan bermutasi saat pencarian berlangsung
currentstate = startstate.copy()

currentnodeinfo = {
    "parent": None,
    "node": startnode,
    "state": currentstate.copy(),
    "f":0,
    "h1":0,
    "h2":0
}
openlist = []
closedlist = [currentstate.copy()]

openlist.append(currentnodeinfo)

solution = None

print("Mohon tunggu, sedang mencari solusi Heuristic Search ")

starttime = time.process_time()

totalvisitednode = 0

while len(openlist) > 0:
    if currentstate == goalstate:
        solution = currentnodeinfo
        break
    totalvisitednode += 1


    smallest = min(openlist,key = itemgetter('f'))

    currentnodeinfo = smallest.copy()
    currentstate = smallest['state'].copy()

    openlist.remove(smallest)

    currentneighbours = neighbours[currentnodeinfo['node']]
    for nindex, neighbour in enumerate(currentneighbours):

        neighbourstate = currentstate.copy()
        neighbourstate[neighbour] = 0
        neighbourstate[currentnodeinfo['node']] = currentstate[neighbour]

        neighbourstatevalue = neighbourstate[neighbour]
        neighbourgoalnode = swapgoalstate[neighbourstatevalue]

        #Heuristic 1 : sum jarak current neighbour node dengan goal nodenya(Manhattan)
        #print("neghbournode",neighbourgoalnode)
        h1 = 0
        for key, value in neighbourstate.items():
            goalnode = swapgoalstate[value]
            if value !=0:
                h1 += abs((key[0] - goalnode[0]) + (key[1] - goalnode[1]))

        #heuristic 2: total posisi yang salah
        h2 = 0
        for key in goalstate :
            if neighbourstate[key] != goalstate[key] and neighbourstate[key] > 0:
                h2 +=1

        f = h1 + h2

        if neighbourstate not in closedlist:
            openlist.append({
            "parent": currentnodeinfo,
            "node": neighbour,
            "state": neighbourstate.copy(),
            "f": f,

            "h1": h1,
            "h2": h2

            })
            closedlist.append(neighbourstate.copy())

endtime = time.process_time()

path = []
node = solution.copy()

while node:
    path.append(node['state'])
    node = node['parent']

path.reverse()
print("Solusinya adalah :")
for index, p in enumerate(path):
    if index > 0:
        print("Langkah", index, ":")
        drawTiles(p)
        #else

        # Print ("Kondisi Awal")
print("Diselesaikan dengan mengunjungi node sebanyak : ", totalvisitednode)
print("waktu:", endtime- starttime, "detik")
print("Langkah", len(path) - 1)