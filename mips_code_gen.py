from pars import result , Node
from tabl_sim_gen import tabl_sim , table_for_t , functions
from threeaddrcodegen import threeaddrcode , is_number
table_for_float={}
sho = tabl_sim

def table_for_t_gen(table_for_t):
    for i in range (len(table_for_t)):
        print (table_for_t)
        if table_for_t['t'+str(i)][0].isnumeric():
            table_for_t['t'+str(i)]=[]
            table_for_t['t' + str(i)] = 'int'
            tabl_sim['t' + str(i)] = []
            tabl_sim['t' + str(i)] = 'int'
        elif is_number(table_for_t['t'+str(i)][0]):
            table_for_t['t'+str(i)]=[]
            table_for_t['t' + str(i)] = 'real'
            table_for_float['f'+ str(i)]=[]
            table_for_float['f'+ str(i)].append('real')
            tabl_sim['t' + str(i)] = []
            tabl_sim['t' + str(i)] = 'real'
        elif table_for_t['t'+str(i)][0] in tabl_sim and tabl_sim[table_for_t['t'+str(i)][0]][1]=='int':

            table_for_t['t' + str(i)] = []
            table_for_t['t' + str(i)] = 'int'
            tabl_sim['t' + str(i)] = []
            tabl_sim['t' + str(i)] = 'int'
        elif table_for_t['t'+str(i)][0] in tabl_sim and tabl_sim[table_for_t['t'+str(i)][0]][1]=='real':
            table_for_t['t'+str(i)]=[]
            table_for_t['t' + str(i)] = 'real'
            table_for_float['f'+ str(i)]=[]
            table_for_float['f'+ str(i)].append('real')
            tabl_sim['t' + str(i)] = []
            tabl_sim['t' + str(i)] = 'real'
        else:
            table_for_t['t' + str(i)] = []
            table_for_t['t' + str(i)] = 'int'
            tabl_sim['t' + str(i)] = []
            tabl_sim['t' + str(i)] = 'int'
    for lo in (sho):
        if lo==('t0'):
            break
        table_for_t[lo]=[]
        table_for_t[lo].append(lo)
    return (table_for_t)

def chek_mul_div(cl, mult, mults, kak):
    if (cl == '/'):
        mult = "div "
        mults = "div.s $f"
        kak = 1


    elif (cl == '*'):
        mult = "mult "
        mults = "mult.s $f"
        kak = 2


    return mult, mults, kak

def chek_sum_sub(cl, addu, addus, kek, keks):
    if (cl == '+'):
        addu = "addu $"
        addus = "addu.s $f"
        kek = 2
        keks = 1

    elif (cl == '-'):
        addu = "subu $"
        addus = "subu.s $f"
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
def fucking_code_generation(threeaddrcode, tabl_sim):
    global table_for_t
    if_count = 0    # счётчик ифов
    skip_count = 0  # счётчик скипов
    flag = False    # для метки перед условием в if и while
    str_count = 0 # счётчик строк констант для объявления
    data = ''  # .data в ассемблерном коде
    data = data + '.data\n\ttrue: .byte 1\n\tfalse: .byte 0\n'
    f = open('out.s', 'w')
    f.write('.text\n')

    print(sho)
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
                elif (is_number(list_peremenn[1]) and (tabl_sim[list_peremenn[2]][1] == 'real' or table_for_t[list_peremenn[2]][0]=='r')):
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
                            if tabl_sim[list_peremenn[2]][1] =='real':
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
                mass = chek_mul_div(cl, mult, mults, kak)
                mult = mass[0]
                mults = mass[1]
                kak = mass[2]
                if not(is_number(list_peremenn[1]) or is_number(list_peremenn[2])):
                        if(list_peremenn[1].isnumeric() or tabl_sim[list_peremenn[1]][1]=='int' or table_for_t[list_peremenn[1]][0]=='i') and (list_peremenn[2].isnumeric() or tabl_sim[list_peremenn[2]][1]=='int'or table_for_t[list_peremenn[kak]][0]=='i'):

                            if list_peremenn[1].isnumeric():
                                f.write('\tli $t0, '+ list_peremenn[2] + '\n')
                                arg1 = '$t0'
                                if list_peremenn[2].isnumeric():
                                    f.write('\tli $t1, '+ list_peremenn[1]+ '\n')
                                    arg2 = '$t1'
                                    f.write('\t' + mult + arg1 + ', ' + arg2 + '\n')
                                elif(list_peremenn[2] in tabl_sim and tabl_sim[list_peremenn[2]][1]=='int'):
                                    arg2 = '$'+ tabl_sim[list_peremenn[2]][0]
                                    f.write('\t' + mult + arg1 + ', ' + arg2 + '\n')
                                elif (table_for_t[list_peremenn[2]][0] == 'i'):
                                    arg2 = '$' + list_peremenn[2]
                                    f.write('\t' + mult + arg1 + ', ' + arg2 + '\n')
                            elif ((list_peremenn[1] in tabl_sim and tabl_sim[list_peremenn[1]][1] == 'int')or(table_for_t[list_peremenn[1]][0] == 'i' and list_peremenn[1] in table_for_t)):
                                if (list_peremenn[1] in tabl_sim and tabl_sim[list_peremenn[1]][1] == 'int'):
                                    arg1 = '$' + tabl_sim[list_peremenn[1]][0]
                                else:
                                    arg1 = '$' + list_peremenn[1]
                                if list_peremenn[2].isnumeric():
                                    f.write('\tli $t1, '+ list_peremenn[2]+ '\n')
                                    arg2 = '$t1'
                                    f.write('\t' + mult + arg1 + ', ' + arg2 + '\n')
                                elif (list_peremenn[2] in tabl_sim and tabl_sim[list_peremenn[2]][1] == 'int'):
                                    arg2 = '$' + tabl_sim[list_peremenn[2]][0]
                                    f.write('\t' + mult + arg1 + ', ' + arg2 + '\n')
                                elif (table_for_t[list_peremenn[2]][0] == 'i' and list_peremenn[2] in table_for_t):
                                    arg1 = '$' + list_peremenn[2]
                                    f.write('\t' + mult + arg1 + ', ' + arg2 + '\n')
                                f.write('\tmflo $' + list_peremenn[3] + '\n')
                        elif ((list_peremenn[1] in tabl_sim and tabl_sim[list_peremenn[1]][1] == 'real') or (table_for_t[list_peremenn[1]][0] == 'r' and list_peremenn[1] in table_for_t)):
                            if (list_peremenn[1] in tabl_sim and tabl_sim[list_peremenn[1]][1] == 'real'):
                                arg1 = '$' + tabl_sim[list_peremenn[1]][0]
                            else:

                                arg1 = '$f' + list_peremenn[1][1:]
                            if is_number(list_peremenn[2]):
                                f.write('\tli.s $f1, ' + list_peremenn[2] + '\n')
                                arg2 = '$f1'
                                f.write('\t' + mults + list_peremenn[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                            elif (list_peremenn[2] in tabl_sim and tabl_sim[list_peremenn[2]][1] == 'real'):
                                arg2 = '$' + tabl_sim[list_peremenn[2]][0]
                                f.write('\tli.s $f' + list_peremenn[1][1:] + ', ' + arg1 + ', ' + arg2 + '\n')

                                f.write('\t' + mults + list_peremenn[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                            elif (table_for_t[list_peremenn[2]][0] == 'r' and list_peremenn[2] in table_for_t):

                                arg2 = '$f' + list_peremenn[2][1:]
                                f.write('\t' + mults + list_peremenn[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                                # f.write('\tmult ' + arg1 + ', ' + arg2 + '\n')
                            # f.write('\tmult $' + list_peremenn[1] + ', $' + list_peremenn[2] + '\n')
                            else:
                                print('error неверный тип')
                                return
                elif is_number(list_peremenn[1]):

                    f.write('\tli.s $f0, ' + list_peremenn[1] + '\n')
                    arg1 = '$f0'
                    if is_number(list_peremenn[2]):
                        f.write('\tli.s $f1, ' + list_peremenn[2] + '\n')
                        arg2 = '$f1'
                        f.write('\t' + mults+ list_peremenn[3][1:]+', '  + arg1 + ', ' + arg2 + '\n')
                    elif (list_peremenn[2] in tabl_sim and tabl_sim[list_peremenn[2]][1] == 'real'):
                        arg2 = '$' + tabl_sim[list_peremenn[2]][0]
                        f.write('\t' + mults+ list_peremenn[3][1:]+', ' + arg1 + ', ' + arg2 + '\n')
                    elif (table_for_t[list_peremenn[2]][0] == 'r' and list_peremenn[2] in table_for_t):
                        arg2 = '$f' + list_peremenn[2][1:]
                        f.write('\t' + mults+ list_peremenn[3][1:]+', '  + arg1 + ', ' + arg2 + '\n')
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
                    mass = chek_sum_sub(cl, addu, addus, kek, keks)
                    addu = mass[0]
                    addus = mass[1]
                    kek = mass[2]
                    keks = mass[3]
                    print(tabl_sim['t0'][0])
                    if not (is_number(list_peremenn[1]) or is_number(list_peremenn[2])):
                        if (list_peremenn[1].isnumeric() or tabl_sim[list_peremenn[1]][1] == 'int' or
                            table_for_t[list_peremenn[1]][
                                0] == 'i') and (
                                list_peremenn[2].isnumeric() or tabl_sim[list_peremenn[2]][1] == 'int' or
                                table_for_t[list_peremenn[kek]][
                                    0] == 'i'):
                            if list_peremenn[1].isnumeric():
                                f.write('\tli $t0, ' + list_peremenn[1] + '\n')
                                arg1 = '$t0'
                                if list_peremenn[2].isnumeric():
                                    f.write('\tli $t1, ' + list_peremenn[2] + '\n')
                                    arg2 = '$t1'
                                    f.write('\t' + addu + list_peremenn[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                                elif (list_peremenn[2] in tabl_sim and tabl_sim[list_peremenn[2]][1] == 'int'):
                                    arg2 = '$' + tabl_sim[list_peremenn[2]][0]
                                    f.write('\t' + addu + list_peremenn[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                                elif (table_for_t[list_peremenn[2]][0] == 'i'):
                                    arg2 = '$' + list_peremenn[2]
                                    f.write('\t' + addu + list_peremenn[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                            elif ((list_peremenn[1] in tabl_sim and tabl_sim[list_peremenn[1]][1] == 'int') or (
                                    table_for_t[list_peremenn[1]][0] == 'i' and list_peremenn[1] in table_for_t)):
                                if (list_peremenn[1] in tabl_sim and tabl_sim[list_peremenn[1]][1] == 'int'):
                                    arg1 = '$' + tabl_sim[list_peremenn[1]][0]
                                else:
                                    arg1 = '$' + list_peremenn[1]
                                if list_peremenn[2].isnumeric():
                                    f.write('\tli $t1, ' + list_peremenn[2] + '\n')
                                    arg2 = '$t1'
                                    f.write('\t' + addu + list_peremenn[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                                elif (list_peremenn[2] in tabl_sim and tabl_sim[list_peremenn[2]][1] == 'int'):
                                    arg2 = '$' + tabl_sim[list_peremenn[2]][0]
                                    f.write('\t' + addu + list_peremenn[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                                elif (table_for_t[list_peremenn[2]][0] == 'i' and list_peremenn[2] in table_for_t):
                                    arg2 = '$' + list_peremenn[2]
                                    f.write('\t' + addu + list_peremenn[3] + ', ' + arg1 + ', ' + arg2 + '\n')
                        elif ((list_peremenn[1] in tabl_sim and tabl_sim[list_peremenn[1]][1] == 'real') or (
                                table_for_t[list_peremenn[1]][0] == 'r' and list_peremenn[1] in table_for_t)):
                            if (list_peremenn[1] in tabl_sim and tabl_sim[list_peremenn[1]][1] == 'real'):
                                arg1 = '$' + tabl_sim[list_peremenn[1]][0]
                            else:
                                arg1 = '$f' + list_peremenn[1][1:]
                            if is_number(list_peremenn[2]):
                                f.write('\tli.s $f1, ' + list_peremenn[2] + '\n')
                                arg2 = '$f1'
                                f.write('\t' + addus + list_peremenn[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                            elif (list_peremenn[2] in tabl_sim and tabl_sim[list_peremenn[2]][1] == 'real'):
                                arg2 = '$' + tabl_sim[list_peremenn[2]][0]
                                f.write('\t' + addus + list_peremenn[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                            elif (table_for_t[list_peremenn[2]][0] == 'r' and list_peremenn[2] in table_for_t):
                                arg2 = '$f' + list_peremenn[2][1:]
                                f.write('\t' + addus + list_peremenn[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                                # f.write('\tmult ' + arg1 + ', ' + arg2 + '\n')
                            # f.write('\tmult $' + list_peremenn[1] + ', $' + list_peremenn[2] + '\n')
                        else:
                            print('error неверный тип')
                            return
                            # f.write('\tmult ' + arg1 + ', ' + arg2 + '\n')
                        # f.write('\tmult $' + list_peremenn[1] + ', $' + list_peremenn[2] + '\n')
                    elif is_number(list_peremenn[1]):

                        f.write('\tli.s $f0, ' + list_peremenn[1] + '\n')
                        arg1 = '$f0'
                        if is_number(list_peremenn[2]):
                            f.write('\tli.s $f1, ' + list_peremenn[2] + '\n')
                            arg2 = '$f1'
                            f.write('\t' + addus + list_peremenn[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                        elif ((list_peremenn[2] in tabl_sim and tabl_sim[list_peremenn[2]][1] == 'real') or (
                                table_for_t[list_peremenn[keks]][0] == 'r' and list_peremenn[keks] in table_for_t)):
                            if (list_peremenn[kek] in tabl_sim and tabl_sim[list_peremenn[kek]][1] == 'real'):
                                arg2 = '$' + tabl_sim[list_peremenn[2]][0]
                            elif (table_for_t[list_peremenn[1]][0] == 'r' and list_peremenn[1] in table_for_t):
                                arg2 = '$f' + list_peremenn[2]
                            f.write('\t' + addus + list_peremenn[3][1:] + ', ' + arg1 + ', ' + arg2 + '\n')
                        else:
                            print('error неверный тип')
                            return
                    else:
                        print('error неверный тип')
                        return


            elif (list_peremenn[0] == '<' or list_peremenn[0] == '>' or list_peremenn[0] == '='):
                if flag == False:
                    L = 'L' + str(if_count)
                    if_count = if_count + 1
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
                f.write('L' + str(if_count) + ':\n')
                if_count = if_count + 1
            elif (list_peremenn[0] == 'GOTO'):
                if (list_peremenn[1] == 'a_kogda'):
                    if f_bc == False:
                        print('after false')
                        f.write('\tj L' + str(if_count - 1) + '\n')
                elif (list_peremenn[1] == 's_kogda'):
                    f.write('\tj L' + str(if_count - 2) + '\n')
                else:
                    f.write('\tj ' + list_peremenn[1] + '\n')
            elif (list_peremenn[0] == 'break'):
                f.write('\tj L' + str(if_count - 3) + '\n')
                f_bc = True
            elif (list_peremenn[0] == 'continue'):
                f.write('\tj L' + str(if_count - 4) + '\n')
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
                elif (is_number(list_peremenn[1])):
                    data=data+'\tdrob'+ list_peremenn[1] +': .float '+list_peremenn[1]+'\n'
                    f.write('\tli $v0, 2\n')
                    f.write('\tlwc1 $f12, drob' + list_peremenn[1] + '\n')
                    f.write('\tsyscall\n')
                elif (list_peremenn[1] in tabl_sim and tabl_sim[list_peremenn[1]][1] == 'int'):
                    f.write('\tli $v0, 1\n')
                    f.write('\tla $a0, ' + '($' + tabl_sim[list_peremenn[1]][0] + ')\n')
                    f.write('\tsyscall\n')
                elif (list_peremenn[1] in tabl_sim and tabl_sim[list_peremenn[1]][1] == 'real'):
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
