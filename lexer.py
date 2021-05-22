from rply import LexerGenerator
from ply import lex

# Список лексем. Обязателен.

reserved = {
        'func':'FUNC',
        'vozv':'VOZV',
        'ii':'AND',
        'ili':'OR',
        'nine':'NOT',
        'print':'PRINT',
        'poka':'POKA',
        # do
        'delai':'DELAI',
        # if
        'kogda':'KOGDA',
        # then
        'togda':'TOGDA',
        # else
        'else':'ELSE',
        # break
        'break':'BREAK',
        # continue
        'continue':'CONTINUE',
        # int
        'int':'INT',
        # real
        'real':'REAL',
        # BOOLEAN
        'boolean':'BOOLEAN',
        # var
        'var':'VAR',
        'str':'STRING'
}

tokens = list(reserved.values()) + [
        'RAVNO',
        'DOUBLE_POINT',
        'COMA',
        'LPAREN',
        'RPAREN',
        # Фигурные скобки
        'LFIG',
        'RFIG',
        # Присваивание
        'PRISV',
        # Точка с запятой
        'SEMI_COLON',
        # Операторы
        'SUM',
        'MINUS',
        'UMNOZ',
        'DELEN',
        # Больше - меньше
        'MORE',
        'LESS',
        # Числа int
        'NUMI',
        #'NUM',
        # Числа real
        'NUMR',

        # Игнорируем пробелы
        #Переменная
        'ID',
        ]



# Регулярные выражения для выделения лексем.
t_DOUBLE_POINT = r'\:'
# t_AND = r'AND'
# t_OR = r'OR'
# t_NOT = r'NOT'
t_RAVNO = r'\='
t_PRINT = r'print'
# Скобки
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMA = r'\,'
# Фигурные скобки
t_LFIG = r'\['
t_RFIG = r'\]'
# Присваивание
t_PRISV = r'\:='
# Точка с запятой
t_SEMI_COLON = r'\;'
# Операторы
t_SUM = r'\+'
t_MINUS = r'\-'
t_UMNOZ = r'\*'
t_DELEN = r'\/'
# Больше - меньше
t_MORE = r'\>'
t_LESS = r'\<'
# Числа int
t_NUMI = r'\d+'
# Числа real
t_NUMR = r'\d+\.\d+'
t_STRING = r'\"[^\'\n]*\"'

def t_comment(t):
    r'/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
    pass


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t


# Правило трассировки номеров строк.

def t_newline(t):
    r'\n+'
    t.lineno += len(t.value)



# Строка, содержащая игнорируемые символы (пробелы и символы табуляции).

t_ignore  = ' \t'



# Правило обработки ошибок

def t_error(t):
    print ("Недопустимый символ '%s'" % t.value[0])
    #t.skip(1)


# Создать анализатор

lex.lex()
