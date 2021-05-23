import ply.yacc as yacc
from tkinter import Tk  # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from lexer import tokens
#начало парсера
class Node:
    def parts_str(self):
        st = []
        for part in self.parts:
            st.append( str( part ) )
        return "\n".join(st)

    def __repr__(self):
        return self.type + ":\n\t" + self.parts_str().replace("\n", "\n\t")

    def add_parts(self, parts):
        self.parts += parts
        return self

    def __init__(self, type, parts):
        self.type = type
        self.parts = parts

def p_prog(p):
    '''prog : OBYAVA dec_list LFIG stmt_list RFIG
            | OBYAVA dec_list func_list LFIG stmt_list RFIG'''
    if len(p) == 6:
        p[0] = Node('prog', [p[2], p[4]])
    else:
        p[0] = Node('prog', [p[2], p[3], p[5]])

def p_func_list(p):
    '''func_list : func
               | func_list SEMI_COLON func'''
    if len(p) == 2:
        p[0] = Node('FUNC', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])

def p_def(p):
    '''func : FUNC ID LPAREN dec_list RPAREN LFIG stmt_list_func RFIG
            | FUNC ID LPAREN dec_list RPAREN LFIG OBYAVA dec_list stmt_list_func RFIG'''
    if len(p) == 9:
        p[0] = Node(p[2], [p[4], p[7]])
    else:
        p[0] = Node(p[2], [p[4], p[8], p[9]])

def p_funcstmt(p):
    '''funcstmt : ID LPAREN args RPAREN'''
    p[0] = Node(p[1], [p[3]])

def p_args(p):
    '''args : arg
            | args SEMI_COLON arg'''
    if len(p) == 2:
        p[0] = Node('args', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])


def p_arg(p):
    '''arg : ID
            | NUMI
            | NUMR
            | LPAREN exp RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_dec_list(p):
    '''dec_list : dec
               | dec_list SEMI_COLON dec'''
    if len(p) == 2:
        p[0] = Node('OBYAVA', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])

def p_dec(p):
    '''dec : id_list DOUBLE_POINT type'''
    p[0] = Node('dec', [p[1], p[3]])

def p_type(p):
    '''type : INT
            | FLOAT
            | STRING'''
    p[0] = Node('type', [p[1]])

def p_id_list(p):
    '''id_list : ID
                | id_list COMA ID'''
    if len(p) == 2:
        p[0] = Node('Id', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])

def p_stmt_list(p):
    '''stmt_list : stmt
                | stmt_list SEMI_COLON stmt'''
    if len(p) == 2:
        p[0] = Node('stmt', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])

def p_stmt(p):
    '''stmt : assign
            | print
            | poka
            | kogda'''
    if len(p) == 2:
        p[0] = p[1]

def p_stmt_list_kogda(p):
    '''stmt_list_kogda : stmt_kogda
                | stmt_list_kogda SEMI_COLON stmt_kogda'''
    if len(p) == 2:
        p[0] = Node('stmt', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])

def p_stmt_kogda(p):
    '''stmt_kogda : assign
            | print
            | poka
            | kogda
            | CONTINUE
            | BREAK'''
    if len(p) == 2:
        p[0] = p[1]

def p_stmt_list_func(p):
    '''stmt_list_func : stmt_func
                | stmt_list_func SEMI_COLON stmt_func'''
    if len(p) == 2:
        p[0] = Node('stmt', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])

def p_stmt_func(p):
    '''stmt_func : assign
            | print
            | poka
            | kogda
            | vozv'''
    if len(p) == 2:
        p[0] = p[1]

def p_vozv(p):
    '''vozv : VOZV exp'''
    p[0] = Node(p[1], [p[2]])

def p_assign(p):
    '''assign : ID PRISV exp
                | ID PRISV STRING'''
    p[0] = Node('assign', [p[1], p[3]])

def p_exp(p):
    '''exp : term
            | exp SUM term
            | exp MINUS term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(p[2], [p[1], p[3]])

def p_term(p):
    '''term : factor
            | term UMNOZ factor
            | term DELEN factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = Node(p[2], [p[1], p[3]])

def p_factor(p):
    '''factor : funcstmt
            | ID
            | NUMI
            | NUMR
            | LPAREN exp RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else: p[0] = p[2]

def p_print(p):
    '''print : PRINT LPAREN exp RPAREN
                | PRINT LPAREN STRING RPAREN'''
    p[0] = Node('print', [p[3]])

def p_poka(p):
    '''poka : POKA bool_exp DELAI LFIG stmt_list RFIG'''
    p[0] = Node('poka', [p[2], p[5]])

def p_kogda(p):
    '''kogda : KOGDA bool_exp TOGDA LFIG stmt_list_kogda RFIG ELSE LFIG stmt_list_kogda RFIG
            | KOGDA bool_exp TOGDA LFIG stmt_list_kogda RFIG'''
    if len(p) == 11:
        p[0] = Node('kogda', [p[2], p[5], p[9]])
    else:
        p[0] = Node('kogda', [p[2], p[5]])

def p_bool_exp(p):
    '''bool_exp : bool_exp OR bool_exp_term
                | bool_exp_term
                | NOT bool_exp
                | bool'''
    if len(p) == 4:
        p[0] = Node(p[2], [p[1], p[3]])
    elif len(p) == 3:
        p[0] = Node(p[1], [p[2]])
    else:
        p[0] = p[1]

def p_bool_exp_term(p):
    '''bool_exp_term : bool_exp_term AND bool
                | bool'''
    if len(p) == 4:
        p[0] = Node(p[2], [p[1], p[3]])
    elif len(p) == 3:
        p[0] = Node(p[1], [p[2]])
    else:
        p[0] = p[1]

def p_bool(p):
    '''bool : LPAREN exp RAVNO exp RPAREN
            | LPAREN exp MORE exp RPAREN
            | LPAREN exp LESS exp RPAREN'''
    p[0] = Node(p[3], [p[2], p[4]])

def p_error(p):
    print ('Unexpected token:', p)

Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
file = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
f = open(file, 'r')
text_input = f.read()

parser = yacc.yacc()
result = parser.parse(text_input)
print(result)



