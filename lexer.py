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
t_LFIG = r'\{'
t_RFIG = r'\}'
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
# while
# t_WHILE = r'while'
# # do
# t_DO = r'do'
# # if
# t_IF = r'if'
# # then
# t_THEN = r'then'
# # else
# t_ELSE = r'else'
# # break
# t_BREAK = r'break'
# # continue
# t_CONTINUE = r'continue'
# # int
# t_INT = r'int'
# # real
# t_REAL = r'real'
# # boolean
# t_BOOLEAN = r'boolean'
# # var
# t_VAR = r'var'
#Переменная
# t_ID = r'\w+'

# Регулярное выражение, требующее дополнительных действий.

def t_comment(t):
    r'/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/'
    pass

# def t_NUMBER_INT(t) :
#     r'\d+'
#     try:
#          t.value = int(t.value)
#     except ValueError:
#          print ("Строка %d: Число %s слишком велико!" % (t.lineno, t.value))
#     #t.value = 0
#     return t

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



# Получить данные со стандартного ввода

# data = raw_input()
#
#
#
# lex.input(data)



# Выделение лексем

# while 1 :
#
#         tok = lex.token()
#
#         if not tok :
#
#                 break
#
#         print (tok)

# class Lexer():
#     def __init__(self):
#         self.lexer = LexerGenerator()
#
#     def _add_tokens(self):
#         self.lexer.ignore(r'(/\*(.|\n)*?\*/)|(#.*)')
#         # Print
#         self.lexer.add('PRINT', r'print')
#         # Скобки
#         self.lexer.add('OPEN_PAREN', r'\(')
#         self.lexer.add('CLOSE_PAREN', r'\)')
#         # Фигурные скобки
#         self.lexer.add('OPEN_FIG', r'\{')
#         self.lexer.add('CLOSE_FIG', r'\}')
#         # Присваивание
#         self.lexer.add('PRISV', r'\:=')
#         # Точка с запятой
#         self.lexer.add('SEMI_COLON', r'\;')
#         # Операторы
#         self.lexer.add('SUM', r'\+')
#         self.lexer.add('SUB', r'\-')
#         self.lexer.add('MUL', r'\*')
#         self.lexer.add('DIV', r'\\')
#         # Больше - меньше
#         self.lexer.add('MORE', r'\>')
#         self.lexer.add('LESS', r'\<')
#         # Числа int
#         self.lexer.add('NUMBER_INT', r'[-+]?\d+')
#
#         # Числа real
#         self.lexer.add('NUMBER_REAL', r'\d+\.\d+')
#         # Игнорируем пробелы
#         self.lexer.ignore('\s+')
#         # while
#         self.lexer.add('WHILE', r'while')
#         # do
#         self.lexer.add('DO', r'do')
#         # if
#         self.lexer.add('IF', r'if')
#         # then
#         self.lexer.add('THEN', r'then')
#         # else
#         self.lexer.add('ELSE', r'else')
#         # break
#         self.lexer.add('BREAK', r'break')
#         # continue
#         self.lexer.add('CONTINUE', r'continue')
#         # int
#         self.lexer.add('INT', r'int')
#         # real
#         self.lexer.add('REAL', r'real')
#         # var
#         self.lexer.add('VAR', r'var')
#         #Переменная
#         self.lexer.add('ID', r'\w+')
#
#     def get_lexer(self):
#         self._add_tokens()
#         return self.lexer.build()