from pars import result ,  Node


tabl_sim = []
table_for_t = {}
functions = []
def obhod(result):
    if (type(result) != Node):
        return
    elif (result.type == 'FUNC'):
        for j in result.parts:
            if (len(j.parts) == 2):
                obhod_fun(j, j.type)
                functions.append(j.type)
            elif (len(j.parts) == 3):
                functions.append(j.type)
                for l in j.parts:
                    obhod_fun(l, j.type)
    elif (result.type == 'dec'):
        for i in result.parts[0].parts:
            tabl_sim.append((i, result.parts[1].parts[0], 'main', 0))
        return
    else:
        for i in range(len(result.parts)):
            obhod(result.parts[i])

def obhod_fun(result, fun):
    if (type(result) != Node):
        return
    elif (result.type == 'dec'):
        for i in result.parts[0].parts:
            tabl_sim.append((i, result.parts[1].parts[0], fun, 0))
        # return
    else:
        for i in range(len(result.parts)):
            obhod_fun(result.parts[i], fun)

obhod(result)
for i in tabl_sim:
    print(i)

def edit_tabl_sim(tabl_sim):
    new_tabl_sim = {}
    index = 0
    new_tabl_sim1 = {}
    jo='main'
    for i in tabl_sim:
        new_tabl_sim[i[0]] = []
        new_tabl_sim[i[0]].append('s' + str(index))
        new_tabl_sim[i[0]].append(i[1])
        new_tabl_sim[i[0]].append(i[2])
        new_tabl_sim[i[0]].append(i[3])
        index = index + 1
    index = 0
    xy=0

    print(new_tabl_sim)
    for i in new_tabl_sim:
        print(i)
        new_tabl_sim1[i[0]] = []
        if new_tabl_sim[i][2] != 'main':
            if jo != new_tabl_sim[i][2]:
                jo = new_tabl_sim[i][2]
                xy=0
            jo = new_tabl_sim[i][2]
            new_tabl_sim1[i[0]].append('a' + str(xy))
            xy=xy+1
            new_tabl_sim1[i[0]].append(new_tabl_sim[i][1])
            new_tabl_sim1[i[0]].append(new_tabl_sim[i][2])
            new_tabl_sim1[i[0]].append(new_tabl_sim[i][3])
        else:
            new_tabl_sim1[i[0]].append('s' + str(index))
            index=index+1
            new_tabl_sim1[i[0]].append(new_tabl_sim[i][1])
            new_tabl_sim1[i[0]].append(new_tabl_sim[i][2])
            new_tabl_sim1[i[0]].append(new_tabl_sim[i][3])
    return new_tabl_sim1

tabl_sim = edit_tabl_sim(tabl_sim)

for key in tabl_sim:
    print(key + ' : ')
    for i in tabl_sim[key]:
        print('\t' + str(i))