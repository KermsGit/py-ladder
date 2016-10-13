# Defines
DIMROW      = 20
DIMCOL      = 80
DIMSCRN     = 7
HISPEED     = 5

CLAD        = 'g'
CDER        = 'o'
CGOLD       = '&'
CRELEAS     = 'V'
CLADDER     = 'H'
CTARGET     = '$'
CEXIT       = '*'
CBAR        = '|'
CGROUND     = '='
CHAZARD     = '.'
CTRAP0      = '^'
CTRAP1      = '-'
CFREE       = ' '

scrno = 0

def unmerge(s):
    t = ''
    for c in s: 
        if( ord(c) & 0200 ):
           t = t +(210-ord(c))*' '
        else:
            t = t + c
    return t

def memcpy(dst, src):
    for i in range(len(src)):
        dst[i] = src[i] 