from pars import result , Node
from tabl_sim_gen import tabl_sim , table_for_t , functions

threeaddrcode = {'main': []}
t_count = 0
if_count = 0

def oblast_vid(result, name):
    if name.startswith('kogda') or (result.isnumeric()) or (number_chek(result)):
        return True
    if (result in tabl_sim.keys()):
        if (tabl_sim[result][2] == name):
            return True
        else:
            print('Ошибка области видимости')
            print(result + ' ' + name)
            return False
    else:
        print('Неверная переменная ' + result + ' ' + name)
        return False

def obhod_main(result):
    if len(result.parts) == 3:
        threeaddrcodeg(result.parts[0], 'main')
        threeaddrcodeg(result.parts[2], 'main')
        for funct in result.parts[1].parts:
            threeaddrcode[funct.type] = []
            threeaddrcodeg(funct, funct.type)
    else:
        threeaddrcodeg(result.parts[0], 'main')
        threeaddrcodeg(result.parts[1], 'main')
    threeaddrcode['main'].append('GOTO END')

def if_while_chek(result):
    if (result.type == 'kogda'):
        flagok = "GOTO p_kogda"
    elif (result.type == 'poka'):
        flagok = "GOTO s_kogda"
    return flagok

def threeaddrcodeg(result, name):
    global t_count, if_count
    if (type(result) != Node and (result == 'break' or result == 'continue')):
        threeaddrcode[name].append(result)
    elif (type(result) != Node):
        return
    elif (result.type == 'assign'):
        if (type(result.parts[0]) == str and type(result.parts[1]) == str):
            if (not oblast_vid(result.parts[0], name)):
                return
            threeaddrcode[name].append(':= ' + result.parts[1] + ' ' + result.parts[0])
        else:
            assign_threeaddrcode(result, name)
            if (not oblast_vid(result.parts[0], name)):
                return
            threeaddrcode[name].append(':= '+'t'+str(t_count-1)+ ' '+result.parts[0])
            table_for_t['t'+str(t_count-1)]=[]
            table_for_t['t'+str(t_count-1)].append(result.parts[0])
            print(table_for_t)
            t_count = 0
    elif ((result.type == 'kogda') or (result.type == 'poka')):
        flagok = if_while_chek(result)
        expression_obhod(result.parts[0], name)
        if_name = 'kogda'+str(if_count)
        if_count = if_count + 1
        threeaddrcode[if_name] = []
        threeaddrcode[name].append('kogda ' + 't' + str(t_count - 1) + ' GOTO ' + if_name)
        threeaddrcodeg(result.parts[1], if_name)
        threeaddrcode[if_name].append(flagok)
    elif (result.type == 'vozv'):
        if (name == 'main'):
            print('error return')
        else:
            assign_threeaddrcode(result.parts[0],name)
            threeaddrcode[name].append('vozv ' + 't'+str(t_count-1))
    elif (result.type == 'print'):
        threeaddrcode[name].append('print ' + result.parts[0])
    else:
        for i in range(len(result.parts)):
            threeaddrcodeg(result.parts[i], name)

def number_chek(string):
    try:
        float(string)
        if (string.isnumeric()):
            return False
        return True
    except ValueError:
        return False

def assign_threeaddrcode(result, name):
    global t_count
    if type(result) != Node:
        if (not oblast_vid(result, name)):
            return
        return result
    elif(result.type == '*' or result.type == '/' or result.type == '+' or result.type == '-'):
        operand = result.type
        arg_left = assign_threeaddrcode(result.parts[0], name)
        arg_right = assign_threeaddrcode(result.parts[1], name)
        if arg_left == None and arg_right == None:
            arg_left = 't' + str(t_count - 2)
            table_for_t['t' + str(t_count - 2)] = []
            table_for_t['t' + str(t_count - 1)] = []
            table_for_t['t'+str(t_count-2)].append('t' + str(t_count - 1))
            table_for_t['t'+str(t_count-2)].append('t' + str(t_count - 2))
        if arg_left == None:
            arg_left = 't'+str(t_count-1)
            table_for_t['t' + str(t_count - 1)] = []
            table_for_t['t'+str(t_count-1)].append(arg_right)
        if arg_right == None:
            arg_right = 't'+str(t_count-1)
            table_for_t['t'+str(t_count-1)].append(arg_left)
        else:
            table_for_t['t'+str(t_count)] = []
            table_for_t['t'+str(t_count)].append(arg_left)
        temp = 't'+str(t_count)
        t_count = t_count+1
        threeaddrcode[name].append(str(operand) + ' ' + str(arg_left) + ' ' + str(arg_right) + ' ' + str(temp))
    elif (result.type in functions):
        string = 'Call ' + result.type + ' '
        for arg in result.parts[0].parts:
            string = string + arg + ' '
        temp = 't' + str(t_count)
        t_count = t_count + 1
        string = string + temp
        threeaddrcode[name].append(string)
    else:
        for i in range(len(result.parts)):
            assign_threeaddrcode(result.parts[i], name)

def expression_obhod(result, name):
    global t_count
    if type(result) != Node:
        if (not oblast_vid(result, name)):
            return
        return result
    elif (result.type == '>' or result.type == '<' or result.type == '='):
        operand = result.type
        arg_left = assign_threeaddrcode(result.parts[0], name)
        arg_right = assign_threeaddrcode(result.parts[1], name)
        temp = 't' + str(t_count)
        table_for_t[temp]=[]
        table_for_t[temp].append(arg_left)
        t_count = t_count + 1
        threeaddrcode[name].append(str(operand) + ' ' + str(arg_left) + ' ' + str(arg_right) + ' ' + str(temp))
    elif (result.type == 'not'):
        operand = result.type
        expression_obhod(result.parts[0], name)
        arg = 't'+str(t_count-1)
        temp = 't' + str(t_count)
        t_count = t_count + 1
        threeaddrcode[name].append(str(operand) + ' ' + str(arg) + ' ' + str(temp))
    elif(result.type == 'and' or result.type == 'or'):
        operand = result.type
        arg_left = expression_obhod(result.parts[0], name)
        arg_right = expression_obhod(result.parts[1], name)
        if arg_left == None and arg_right == None:
            arg_left = 't' + str(t_count - 2)
            arg_right = 't' + str(t_count - 1)
        if arg_left == None:
            arg_left = 't'+str(t_count-1)
            table_for_t['t' + str(t_count - 1)].append(arg_right)
        if arg_right == None:
            arg_right = 't'+str(t_count-1)
            table_for_t['t' + str(t_count - 1)].append(arg_left)
        temp = 't'+str(t_count)
        if not(temp in table_for_t):
            table_for_t[temp]=[]
            table_for_t['t' + str(t_count)].append(arg_left)
        t_count = t_count+1
        print('op = '+operand)
        print('arg_left='+str(arg_left))
        print('arg_right='+str(arg_right))
        print('temp='+str(temp))
        threeaddrcode[name].append(str(operand) + ' ' + str(arg_left) + ' ' + str(arg_right) + ' ' + str(temp))
    else:
        for i in range(len(result.parts)):
            expression_obhod(result.parts[i], name)
obhod_main(result)
for key in threeaddrcode:
    print(key + ' : ')
    for i in threeaddrcode[key]:
        print('\t' + str(i))


