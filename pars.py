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

def p_program(p):
    '''program : OBYAVA declare_list LFIG statemant_list RFIG
            | OBYAVA declare_list func_list LFIG statemant_list RFIG'''
    if len(p) == 6:
        p[0] = Node('program', [p[2], p[4]])
    else:
        p[0] = Node('program', [p[2], p[3], p[5]])

def p_func_list(p):
    '''func_list : func
               | func_list SEMI_COLON func'''
    if len(p) == 2:
        p[0] = Node('FUNC', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])

def p_def(p):
    '''func : FUNC ID LPAREN declare_list RPAREN LFIG statemant_list_func RFIG
            | FUNC ID LPAREN declare_list RPAREN LFIG OBYAVA declare_list statemant_list_func RFIG'''
    if len(p) == 9:
        p[0] = Node(p[2], [p[4], p[7]])
    else:
        p[0] = Node(p[2], [p[4], p[8], p[9]])

def p_statem_func(p):
    '''statem_func : ID LPAREN arguments RPAREN'''
    p[0] = Node(p[1], [p[3]])

def p_arguments(p):
    '''arguments : argument
            | arguments SEMI_COLON argument'''
    if len(p) == 2:
        p[0] = Node('arguments', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])


def p_argument(p):
    '''argument : ID
            | NUMI
            | NUMR
            | LPAREN expressoin RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_declare_list(p):
    '''declare_list : dec
               | declare_list SEMI_COLON dec'''
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

def p_statemant_list(p):
    '''statemant_list : statemant
                | statemant_list SEMI_COLON statemant'''
    if len(p) == 2:
        p[0] = Node('statemant', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])

def p_statemant(p):
    '''statemant : prisvaiv
            | print
            | poka
            | kogda'''
    if len(p) == 2:
        p[0] = p[1]

def p_statemant_list_kogda(p):
    '''statemant_list_kogda : statemant_kogda
                | statemant_list_kogda SEMI_COLON statemant_kogda'''
    if len(p) == 2:
        p[0] = Node('statemant', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])

def p_statemant_kogda(p):
    '''statemant_kogda : prisvaiv
            | print
            | poka
            | kogda
            | CONTINUE
            | BREAK'''
    if len(p) == 2:
        p[0] = p[1]

def p_statemant_list_func(p):
    '''statemant_list_func : statemant_func
                | statemant_list_func SEMI_COLON statemant_func'''
    if len(p) == 2:
        p[0] = Node('statemant', [p[1]])
    else:
        p[0] = p[1].add_parts([p[3]])

def p_statemant_func(p):
    '''statemant_func : prisvaiv
            | print
            | poka
            | kogda
            | vozv'''
    if len(p) == 2:
        p[0] = p[1]

def p_vozv(p):
    '''vozv : VOZV expressoin'''
    p[0] = Node(p[1], [p[2]])

def p_prisvaiv(p):
    '''prisvaiv : ID PRISV expressoin
                | ID PRISV STRING'''
    p[0] = Node('prisv', [p[1], p[3]])

def p_expressoin(p):
    '''expressoin : term
            | expressoin SUM term
            | expressoin MINUS term'''
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
    '''factor : statem_func
            | ID
            | NUMI
            | NUMR
            | LPAREN expressoin RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    else: p[0] = p[2]

def p_print(p):
    '''print : PRINT LPAREN expressoin RPAREN
                | PRINT LPAREN STRING RPAREN'''
    p[0] = Node('print', [p[3]])

def p_poka(p):
    '''poka : POKA logic_expressoinression DELAI LFIG statemant_list RFIG'''
    p[0] = Node('poka', [p[2], p[5]])

def p_kogda(p):
    '''kogda : KOGDA logic_expressoinression TOGDA LFIG statemant_list_kogda RFIG ELSE LFIG statemant_list_kogda RFIG
            | KOGDA logic_expressoinression TOGDA LFIG statemant_list_kogda RFIG'''
    if len(p) == 11:
        p[0] = Node('kogda', [p[2], p[5], p[9]])
    else:
        p[0] = Node('kogda', [p[2], p[5]])

def p_logic_expressoinression(p):
    '''logic_expressoinression : logic_expressoinression OR logic_expressoinression_term
                | logic_expressoinression_term
                | NOT logic_expressoinression
                | logic'''
    if len(p) == 4:
        p[0] = Node(p[2], [p[1], p[3]])
    elif len(p) == 3:
        p[0] = Node(p[1], [p[2]])
    else:
        p[0] = p[1]

def p_logic_expressoinression_term(p):
    '''logic_expressoinression_term : logic_expressoinression_term AND logic
                | logic'''
    if len(p) == 4:
        p[0] = Node(p[2], [p[1], p[3]])
    elif len(p) == 3:
        p[0] = Node(p[1], [p[2]])
    else:
        p[0] = p[1]

def p_logic(p):
    '''logic : LPAREN expressoin RAVNO expressoin RPAREN
            | LPAREN expressoin MORE expressoin RPAREN
            | LPAREN expressoin LESS expressoin RPAREN'''
    p[0] = Node(p[3], [p[2], p[4]])

def p_error(p):
    print ('Unexpressoinected token:', p)

Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
file = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
f = open(file, 'r')
text_input = f.read()

parser = yacc.yacc()
result = parser.parse(text_input)
print(result)



