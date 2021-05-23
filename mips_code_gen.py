from pars import result , Node
from tabl_sim_gen import tabl_sim , table_for_t , functions
from threeaddrcodegen import threeaddrcode , number_chek
table_for_float={}
t_s_copy = tabl_sim
poka_flag = 0
skip_count = 0
str_count = 0
def table_for_t_gen(table_for_t):
    for i in range (len(table_for_t)):
        print (table_for_t)
        if (table_for_t['t'+str(i)][0].isnumeric()) or (table_for_t['t'+str(i)][0] in tabl_sim and tabl_sim[table_for_t['t'+str(i)][0]][1]=='int'):
            table_for_t['t'+str(i)]=[]
            table_for_t['t' + str(i)] = 'int'
            tabl_sim['t' + str(i)] = []
            tabl_sim['t' + str(i)] = 'int'
        elif (number_chek(table_for_t['t'+str(i)][0])) or (table_for_t['t'+str(i)][0] in tabl_sim and tabl_sim[table_for_t['t'+str(i)][0]][1]=='float'):
            table_for_t['t'+str(i)]=[]
            table_for_t['t' + str(i)] = 'float'
            table_for_float['f'+ str(i)]=[]
            table_for_float['f'+ str(i)].append('float')
            tabl_sim['t' + str(i)] = []
            tabl_sim['t' + str(i)] = 'float'
    for lo in (t_s_copy):
        if lo==('t0'):
            break
        table_for_t[lo]=[]
        table_for_t[lo].append(lo)
    return (table_for_t)

def chek_mul_div(cl):
    if (cl == '/'):
        mult = "div "
        mults = "div.s $f"
        kak = 1
    elif (cl == '*'):
        mult = "mult "
        mults = "mult.s $f"
        kak = 2
    return mult, mults, kak

def chek_sum_sub(cl):
    if (cl == '+'):
        addu = "addu $"
        addus = "add.s $f"
        kek = 2
        keks = 1
    elif (cl == '-'):
        addu = "subu $"
        addus = "sub.s $f"
        kek = 1
        keks = 2
    return addu, addus, kek, keks

def sravn_op_chek(list_peremenn):
    if list_peremenn[0] == '<':
        flagok1 = "bge $"
    elif list_peremenn[0] == '>':
        flagok1 = "ble $"
    elif list_peremenn[0] == '=':
        flagok1 = "bne $"
    return flagok1
def type_chek(tabl_sim, list_peremenn):
    if tabl_sim[list_peremenn[1]][1] == 'int':
        type_p = 'int'
        t_p = 'i'
        kak1 = '$'
        kak2 = 'li $t1, '
    elif tabl_sim[list_peremenn[1]][1] == 'float':
        type_p = 'float'
        t_p = 'f'
        kak1 = '$f'
        kak2 = 'li.s $f1, '
    return type_p, t_p, kak1, kak2
def fucking_code_generation(threeaddrcode, tabl_sim):
    global table_for_t , poka_flag , skip_count , str_count

    flag = False

    data = ''
    data = data + '.data\n\ttrue: .byte 1\n\tfalse: .byte 0\n'
    f = open('out.s', 'w')
    f.write('.text\n')
    print(t_s_copy)
    lol = table_for_t_gen(table_for_t)
    table_for_t = lol
    for label in threeaddrcode:
        f.write(label + ':\n')
        for command in threeaddrcode[label]:
            list_peremenn = command.split(' ')
            if ( list_peremenn[0] == ':=' ):
                if list_peremenn[1].isnumeric() and (tabl_sim[list_peremenn[2]][1] == 'int' or table_for_t[list_peremenn[2]][0]=='i'):
                    if (list_peremenn[2] in table_for_t.keys() and table_for_t[list_peremenn[2]][0]!=list_peremenn[2]):
                        f.write('\tli $' + list_peremenn[2] + ', ' + list_peremenn[1] + '\n')
                    else:
                        f.write('\tli $' + tabl_sim[list_peremenn[2]][0] + ', ' + list_peremenn[1] + '\n')
                elif list_peremenn[1].startswith('\"') and list_peremenn[1].endswith('\"') and (tabl_sim[list_peremenn[2]][1] == 'str'):
                    data = data + '\t' + list_peremenn[2] + ': .asciiz ' + list_peremenn[1] +'\n'
                elif (number_chek(list_peremenn[1]) and (tabl_sim[list_peremenn[2]][1] == 'float' or table_for_t[list_peremenn[2]][0]=='r')):
                    data=data + '\tdrob'+ list_peremenn[1] +': .float '+list_peremenn[1]+'\n'
                    if (list_peremenn[2] in table_for_t.keys() and table_for_t[list_peremenn[2]][0]!=list_peremenn[2]):
                        f.write('\tla $' + list_peremenn[2] + ', drob' + list_peremenn[1] + '\n')
                    else:
                        f.write('\tla $' + tabl_sim[list_peremenn[2]][0] + ', drob' + list_peremenn[1] + '\n')
                elif(list_peremenn[1] in tabl_sim.keys() ):
                    if (list_peremenn[1] in table_for_t.keys() and table_for_t[list_peremenn[1]][0]!=list_peremenn[1]):
                        if (list_peremenn[2] in table_for_t.keys() and table_for_t[list_peremenn[2]][0]!=list_peremenn[2]):
                            if table_for_t[list_peremenn[1]][0]=='r':
                                f.write('\tmov.s $f' +  list_peremenn[2][1:] + ', $f' + list_peremenn[1][1:] + '\n')
                            else:
                                f.write('\tmove $' + list_peremenn[2] + ', $f' + list_peremenn[1] + '\n')
                        elif list_peremenn[2] in tabl_sim.keys():
                            if table_for_t[list_peremenn[1]][0] == 'r':
                                f.write('\tmov.s $' + tabl_sim[list_peremenn[2]][0] + ', $f' + list_peremenn[1][1:] + '\n')
                            else:
                                f.write('\tmove $' + tabl_sim[list_peremenn[2]][0] + ', $' + list_peremenn[1] + '\n')
                    elif (list_peremenn[1] in tabl_sim.keys()):
                        if (list_peremenn[2] in tabl_sim.keys()):
                            if tabl_sim[list_peremenn[2]][1] =='float':
                                f.write('\tmov.s $' + tabl_sim[list_peremenn[2]][0] + ', $' + tabl_sim[list_peremenn[1]][0] + '\n')
                            else:
                                f.write('\tmove $' + tabl_sim[list_peremenn[2]][0] + ', $' + tabl_sim[list_peremenn[1]][0] + '\n')
                else:
                    if (list_peremenn[2] in tabl_sim.keys()):
                        f.write('\tmove $' + list_peremenn[2] + ', $' + list_peremenn[1] + '\n')
                    elif (list_peremenn[2] in tabl_sim.keys()):
                        f.write('\tmove $' + tabl_sim[list_peremenn[2]][0] + ', $' + list_peremenn[1] +'\n')
                    else:
                        f.write('\tmove $' + list_peremenn[2] + ', $' + list_peremenn[1] + '\n')
            elif (( list_peremenn[0] == '*' ) or ( list_peremenn[0] == '/' )):
                mult = ""
                mults = ""
                kak = 0
                cl = list_peremenn[0]
                mass = []
                mass = chek_mul_div(cl)
                mult = mass[0]
                mults = mass[1]
                kak = mass[2]
                type_p = "int"
                t_p = "i"
                kak1 = '$'
                kak2 = 'li $t1, '
                flagok3 = type_chek(tabl_sim, list_peremenn)
                type_p = flagok3[0]
                t_p = flagok3[1]
                kak1 = flagok3[2]
                kak2 = flagok3[3]
                if not(number_chek(list_peremenn[1]) or number_chek(list_peremenn[2])):
                        if(list_peremenn[1].isnumeric() or tabl_sim[list_peremenn[1]][1]=='int' or table_for_t[list_peremenn[1]][0]=='i') and (list_peremenn[2].isnumeric() or tabl_sim[list_peremenn[2]][1]=='int'or table_for_t[list_peremenn[kak]][0]=='i'):
                            if list_peremenn[1].isnumeric():
                                # f.write('\tli $t0, '+ list_peremenn[2] + '\n')
                                arg_left = '$t0'
                                if list_peremenn[2].isnumeric():
                                    f.write('\tli $t1, '+ list_peremenn[1]+ '\n')
                                    arg_right = '$t1'
                                    f.write('\t' + mult + arg_left + ', ' + arg_right + '\n')
                                elif(list_peremenn[2] in tabl_sim and tabl_sim[list_peremenn[2]][1]=='int'):
                                    arg_right = '$'+ tabl_sim[list_peremenn[2]][0]
                                    f.write('\t' + mult + arg_left + ', ' + arg_right + '\n')
                                elif (table_for_t[list_peremenn[2]][0] == 'i'):
                                    arg_right = '$' + list_peremenn[2]
                                    f.write('\t' + mult + arg_left + ', ' + arg_right + '\n')

                            elif ((list_peremenn[1] in tabl_sim and tabl_sim[list_peremenn[1]][1] == type_p)or(table_for_t[list_peremenn[1]][0] == t_p and list_peremenn[1] in table_for_t)):
                                if (list_peremenn[1] in tabl_sim and tabl_sim[list_peremenn[1]][1] == type_p):
                                    arg_left = '$' + tabl_sim[list_peremenn[1]][0]
                                else:
                                    arg_left = kak1 + list_peremenn[1]
                                if list_peremenn[2].isnumeric():
                                    f.write('\t' + kak2 + list_peremenn[2]+ '\n')
                                    arg_right = '$t1'
                                    f.write('\t' + mult + arg_left + ', ' + arg_right + '\n')
                                elif (list_peremenn[2] in tabl_sim and tabl_sim[list_peremenn[2]][1] == 'int'):
                                    arg_right = '$' + tabl_sim[list_peremenn[2]][0]
                                    f.write('\t' + mult + arg_left + ', ' + arg_right + '\n')
                                elif (table_for_t[list_peremenn[2]][0] == 'i' and list_peremenn[2] in table_for_t):
                                    arg_right = '$' + list_peremenn[2]
                                    f.write('\t' + mult + arg_left + ', ' + arg_right + '\n')
                                f.write('\tmflo $' + list_peremenn[3] + '\n')
                elif number_chek(list_peremenn[1]):
                    f.write('\tli.s $f0, ' + list_peremenn[1] + '\n')
                    arg_left = '$f0'
                    if number_chek(list_peremenn[2]):
                        f.write('\tli.s $f1, ' + list_peremenn[2] + '\n')
                        arg_right = '$f1'
                        f.write('\t' + mults+ list_peremenn[3][1:]+', '  + arg_left + ', ' + arg_right + '\n')
                    elif (list_peremenn[2] in tabl_sim and tabl_sim[list_peremenn[2]][1] == 'float'):
                        arg_right = '$' + tabl_sim[list_peremenn[2]][0]
                        f.write('\t' + mults+ list_peremenn[3][1:]+', ' + arg_left + ', ' + arg_right + '\n')
                    elif (table_for_t[list_peremenn[2]][0] == 'r' and list_peremenn[2] in table_for_t):
                        arg_right = '$f' + list_peremenn[2][1:]
                        f.write('\t' + mults+ list_peremenn[3][1:]+', '  + arg_left + ', ' + arg_right + '\n')
                    else:
                        print('error неверный тип')
                        return
            elif ((list_peremenn[0] == '+') or (list_peremenn[0] == '-')):
                    addu = ""
                    addus = ""
                    kek = 0
                    keks = 0
                    cl = list_peremenn[0]
                    mass = []
                    mass = chek_sum_sub(cl)
                    addu = mass[0]
                    addus = mass[1]
                    kek = mass[2]
                    keks = mass[3]
                    type_p = "int"
                    t_p = "i"
                    kak1 = '$'
                    kak2 = 'li $t1, '
                    flagok3 = type_chek(tabl_sim, list_peremenn)
                    type_p = flagok3[0]
                    t_p = flagok3[1]
                    kak1 = flagok3[2]
                    kak2 = flagok3[3]
                    print(tabl_sim['t0'][0])
                    if (number_chek(list_peremenn[1]) or number_chek(list_peremenn[2])):
                        f.write('\tli.s $f0, ' + list_peremenn[1] + '\n')
                        arg_left = '$f0'
                        if number_chek(list_peremenn[2]):
                            f.write('\tli.s $f1, ' + list_peremenn[2] + '\n')
                            arg_right = '$f1'
                            f.write('\t' + addus + list_peremenn[3][1:] + ', ' + arg_left + ', ' + arg_right + '\n')
                        elif ((list_peremenn[2] in tabl_sim and tabl_sim[list_peremenn[2]][1] == 'float') or (
                                table_for_t[list_peremenn[keks]][0] == 'r' and list_peremenn[keks] in table_for_t)):
                            if (list_peremenn[kek] in tabl_sim and tabl_sim[list_peremenn[kek]][1] == 'float'):
                                arg_right = '$' + tabl_sim[list_peremenn[2]][0]
                            elif (table_for_t[list_peremenn[1]][0] == 'r' and list_peremenn[1] in table_for_t):
                                arg_right = '$f' + list_peremenn[2]
                            f.write('\t' + addus + list_peremenn[3][1:] + ', ' + arg_left + ', ' + arg_right + '\n')
                        else:
                            print('error неверный тип')
                            return
                    elif not (number_chek(list_peremenn[1]) or number_chek(list_peremenn[2])):
                        if (list_peremenn[1].isnumeric() or tabl_sim[list_peremenn[1]][1] == type_p or table_for_t[list_peremenn[1]][0] == t_p) and (list_peremenn[2].isnumeric() or tabl_sim[list_peremenn[2]][1] == type_p or table_for_t[list_peremenn[kek]][0] == t_p):
                            if list_peremenn[1].isnumeric():
                                f.write('\tli $t0, ' + list_peremenn[1] + '\n')
                                arg_left = '$t0'
                                if list_peremenn[2].isnumeric():
                                    f.write('\t' + kak2 + list_peremenn[2] + '\n')
                                    arg_right = '$t1'
                                    f.write('\t' + addu + list_peremenn[3] + ', ' + arg_left + ', ' + arg_right + '\n')
                                elif (list_peremenn[2] in tabl_sim and tabl_sim[list_peremenn[2]][1] == 'int'):
                                    arg_right = '$' + tabl_sim[list_peremenn[2]][0]
                                    f.write('\t' + addu + list_peremenn[3] + ', ' + arg_left + ', ' + arg_right + '\n')
                                elif (table_for_t[list_peremenn[2]][0] == 'i'):
                                    arg_right = '$' + list_peremenn[2]
                                    f.write('\t' + addu + list_peremenn[3] + ', ' + arg_left + ', ' + arg_right + '\n')
                            elif ((list_peremenn[1] in tabl_sim and tabl_sim[list_peremenn[1]][1] == 'int') or (
                                    table_for_t[list_peremenn[1]][0] == 'i' and list_peremenn[1] in table_for_t)):
                                if (list_peremenn[1] in tabl_sim and tabl_sim[list_peremenn[1]][1] == 'int'):
                                    arg_left = '$' + tabl_sim[list_peremenn[1]][0]
                                else:
                                    arg_left = '$' + list_peremenn[1]
                                if list_peremenn[2].isnumeric():
                                    f.write('\tli $t1, ' + list_peremenn[2] + '\n')
                                    arg_right = '$t1'
                                    f.write('\t' + addu + list_peremenn[3] + ', ' + arg_left + ', ' + arg_right + '\n')
                                elif (list_peremenn[2] in tabl_sim and tabl_sim[list_peremenn[2]][1] == 'int'):
                                    arg_right = '$' + tabl_sim[list_peremenn[2]][0]
                                    f.write('\t' + addu + list_peremenn[3] + ', ' + arg_left + ', ' + arg_right + '\n')
                                elif (table_for_t[list_peremenn[2]][0] == 'i' and list_peremenn[2] in table_for_t):
                                    arg_right = '$' + list_peremenn[2]
                                    f.write('\t' + addu + list_peremenn[3] + ', ' + arg_left + ', ' + arg_right + '\n')
                    else:
                        print('error неверный тип')
                        return
            elif (list_peremenn[0] == '<' or list_peremenn[0] == '>' or list_peremenn[0] == '='):
                if flag == False:
                    L = 'L' + str(poka_flag)
                    poka_flag = poka_flag + 1
                    flag = True
                    f.write(L + ':\n')
                flagok1 = sravn_op_chek(list_peremenn)
                f.write('\tla $' + list_peremenn[3] + ', false\n')
                f.write('\t' + flagok1 + tabl_sim[list_peremenn[1]][0] + ', $' + tabl_sim[list_peremenn[2]][0] + ', SKIP'+str(skip_count) + '\n')
                f.write('\tla $' + list_peremenn[3] + ', true\n')
                f.write('SKIP'+str(skip_count) + ':\n')
                skip_count = skip_count + 1
            elif (list_peremenn[0] == 'and' or list_peremenn[0] == 'or'):
                f.write('\t' + list_peremenn[0] + ' $' + list_peremenn[3] + ', $' + list_peremenn[1] + ', $' + list_peremenn[2] + '\n')
            elif (list_peremenn[0] == 'not'):
                index = list_peremenn[2][1:]
                index = int(index) + 1
                temp = 't' + str(index)
                f.write('\tla $' + temp + ' false\n')
                f.write('\tnor $' + list_peremenn[2] + ', $' + list_peremenn[1] + ', $' + temp + '\n')
            elif (list_peremenn[0] == 'kogda'):
                flag = False
                index = list_peremenn[1][1:]
                index = int(index) + 1
                temp = 't' + str(index)
                f.write('\tla $' + temp + ', true\n')
                f.write('\tbeq $' + temp + ', $' + list_peremenn[1] + ', ' + list_peremenn[3] + '\n')
                f.write('L' + str(poka_flag) + ':\n')
                poka_flag = poka_flag + 1
            elif (list_peremenn[0] == 'GOTO'):
                if (list_peremenn[1] == 'a_kogda'):
                    if f_bc == False:
                        print('after false')
                        f.write('\tj L' + str(poka_flag - 1) + '\n')
                elif (list_peremenn[1] == 's_kogda'):
                    f.write('\tj L' + str(poka_flag - 2) + '\n')
                else:
                    f.write('\tj ' + list_peremenn[1] + '\n')
            elif (list_peremenn[0] == 'break'):
                f.write('\tj L' + str(poka_flag - 3) + '\n')
                f_bc = True
            elif (list_peremenn[0] == 'continue'):
                f.write('\tj L' + str(poka_flag - 4) + '\n')
                f_bc = True
            elif (list_peremenn[0] == 'print'):
                if (list_peremenn[1].startswith('\"') and list_peremenn[1].endswith('\"')):
                    data=data +'\tstr'+str(str_count) + ': .asciiz '+list_peremenn[1]+'\n'
                    str_count = str_count+1
                    f.write('\tli $v0, 4\n')
                    f.write('\tla $a0, '+'str'+str(str_count-1)+'\n')
                    f.write('\tsyscall\n')
                elif (list_peremenn[1] in tabl_sim and tabl_sim[list_peremenn[1]][1] == 'str'):
                    f.write('\tli $v0, 4\n')
                    f.write('\tla $a0, ' + list_peremenn[1] + '\n')
                    f.write('\tsyscall\n')
                elif (list_peremenn[1].isnumeric()):
                    f.write('\tli $v0, 1\n')
                    f.write('\tla $a0, '+list_peremenn[1] + '\n')
                    f.write('\tsyscall\n')
                elif (number_chek(list_peremenn[1])):
                    data=data+'\tdrob'+ list_peremenn[1] +': .float '+list_peremenn[1]+'\n'
                    f.write('\tli $v0, 2\n')
                    f.write('\tlwc1 $f12, drob' + list_peremenn[1] + '\n')
                    f.write('\tsyscall\n')
                elif (list_peremenn[1] in tabl_sim and tabl_sim[list_peremenn[1]][1] == 'int'):
                    f.write('\tli $v0, 1\n')
                    f.write('\tla $a0, ' + '($' + tabl_sim[list_peremenn[1]][0] + ')\n')
                    f.write('\tsyscall\n')
                elif (list_peremenn[1] in tabl_sim and tabl_sim[list_peremenn[1]][1] == 'float'):
                    f.write('\tli $v0, 2\n')
                    f.write('\tlwc1 $f12, ($' + tabl_sim[list_peremenn[1]][0] + ')\n')
                    f.write('\tsyscall\n')
            elif (list_peremenn[0] == 'vozv'):
                f.write('\tmove $t9, $' + list_peremenn[1] + '\n' )
                f.write('\tjr $ra\n')
            elif (list_peremenn[0] == 'Call'):
                args = list_peremenn[2:len(list_peremenn)-1]
                print(args)
                for i in range(len(args)):
                    f.write('\tmove $a' + str(i) + ', $' + tabl_sim[args[i]][0] + '\n')
                f.write('\tjal ' + list_peremenn[1] + '\n')
                f.write('\tmove $' + list_peremenn[len(list_peremenn)-1] + ', $t9\n')
    f.write('END:\n')
    f.write(data)
    f.close()
fucking_code_generation(threeaddrcode, tabl_sim)
