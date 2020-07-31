#!/usr/bin/env python

import curses
import signal
import random
import os
import msvcrt
import time
import sys
import enum

from ltime import *

# Defines
DIMROW      = 20
DIMCOL      = 80
DIMSCRN     = 7
HISPEED     = 5
EOF           = -1

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

hiders  = [5, 8, 5, 5, 7, 6, 6];
st_boni = [35,45,33,32,29,29,22];

screens = [ [
"\253V\301$",
"\231H",
"\302H\252H",
"\313=========H==================================================",
"\302H",
"\302H",
"\302H\310H\265H",
"================H==========H==================\317========H=====================",
"\302&\310H\265H\310|\313|",
"\231H\311Easy\321Street",
"\302H\252H",
"\313=========H==========H=========\320=======================",
"\302H",
"\302H",
"\302H\252H",
"========================\321======================\321=========H==============",
"\231H",
"\231H",
"*\316g\237H\276*",
"==============================================================================="
], [
"\210$",
"\217&\314H",
"\316H\313|V\235V|\315H",
"====H=======================\321=========================\321======================",
"\316H",
"\316H",
"\316H\276&\321|\271.\321.\300H",
"==========================\321======\320===================\321===================H==",
"\210H",
"\260|\253H",
"\316H\265|\301.\320.\300H",
"====H=====================\317======\320================\320======================",
"\316H",
"\316H\274|",
"\316H\274|\272.\317.\301H",
"=========================\320========\316==============\317==================H==",
"\210H",
"==============\274|\255H",
"\321Long\321Island\321|\317g\311*\312|\301*\277H",
"==============================================================================="
], [
"\266V\303V\307V\303$",
"\213$$$",
"\315g\316H\236H\314$$$$$\317H",
"==========H===\242=H==============H",
"\310H\236H\304H",
"\310H\264&\275H\304H",
"\315==============\317====\315=\316======\316=\317====\316=====H=====\311H",
"\316G\304^^^\316^^^^^\321^^^^\314^^^^\321^^^\316^^^\275$",
"\316h\221|",
"\316o\315|\275H\265&\313|",
"\316s\315======================H==============================\321===========",
"\316t\312&\300H",
"\262H",
"\304|\301H\301H\277H",
"\316T\311==================H=================H===================H=======",
"\316o\245H\277H",
"\316w\221H",
"\316n\267^\255H",
"*\264^^^\256H\313*",
"==============================================================================="
], [
"\246V\273V",
"",
"\315H\305H\271|\302H",
"=====H=====--======H==========================\315===----====H===========",
"\315H\305H\302|&&\273H",
"\315H\305H\302==================\312H",
"\315H\305H\273tunnel\320H\310H",
"\315H\307=======---===----=================H=\311H\307H",
"\315H\311|\267vision\320H\310H\307H",
"\315H\311=========---&\314-----============H\310H\307H",
"\315H\307H\261H\321|\312H\307H",
"\315H\307H=========----===----================\312H\320==============",
"\301H\252&\317H",
"\301H\252|\317H",
"====---====\314H\252|\317H",
"|\311|\316================---===---===================\317H",
"|\317===\317|\237H\312H\316g",
"|\316$\316|\237H\315===H=======",
"|*\320$$$\320*|\317*\302*\313*\275*H\313*H",
"==============================================================================="
], [
"\311$",
"\311H\237V",
"\311H",
"\311HHHHHHHHHHHHH\315.HHHHHHHHHHHHHH\270H\316g",
"\311&\277V\307H\272==H==========",
"\251H\270H",
"\317H\255H\312.\301H",
"===H==============-----------============H====\274H",
"\317H\234H\311H",
"\317H\241=====H==============",
"\317H\255H\302H",
"\317H\304&..^^^.....^..^\321.\321^^\317H==---------\315H",
"\317H\311============================H\316&\307H\305H",
"\317H\311===\314===\314===\313H\316---------=================H======",
"\317H\255H\264H",
"\317H\270&\310H\310&\277H",
"\317==========-------------------------=======----------===================",
"",
"^^^*\311^^^^^^^^^^^^^^^^^^^^^^^^^*\315*^^^^^^^^^^*Point\321of\321No\321Return*^^^^",
"==============================================================================="
], [
"\312Bug\321City\305HHHHHHHH\270V",
"\267HHH\314HHH",
"\317H\250>mmmmmmmm",
"\317H===============\277====================\310H",
"\317H\304|=====\313\\\320/\311V\300=====H==========",
"\317H\266\\/\260H",
"\317H\252|\321$\275H",
"\317H\307H\266|\321H\275H",
"\317H\313====H=======\310g\310|&H\316H\302H",
"\317H\307H\305======================H\307======",
"\317H\307H\314&|\267H\276H",
"\317H\307H\314&|\276H\314H\315}{\312=====H====",
"===H===&\313H\313=====================H\314H\276H",
"\303H\266H\314H\276H",
"\303H\266H\314&\276H",
"\311======H===\317=======\316H\316<>\316&\267H",
"\261H==========\313=====\315=\315============",
"\315}i{\271H",
"*\262H\246*",
"==============================================================================="
], [
"\276=Gang\321Land=\265V\311.",
"\277==\314_\320==\254.",
"\314g\316H\312|\320[]\321|_|\321|\300&\276.\320H",
"===========H\312|\315|_|\321|\313H\311===\317===================H",
"\314V\316H\312=============\315H======\266H",
"\307H\270H\275&\306H",
"\307H\270H\302|\316|\306H",
"\316H\314H\312^^^&&^^^\321&\321^\320^^^\321H\307H\316|\316=============H",
"\316H======H\317=======================H===========H=====\310&\314H",
"\316H\261H\307H\316|\311&&&\315H",
"\316H\261H\307H\316|\312&&&&&\316H",
"\316H\261H\307H\316|\316=============H",
"\304=====------=================\312H\316|\313$\315$",
"\251|\312H\316|\314$$$\317$$$",
"====------===\266|\312H\316|\315$$$$$\321$$$$$",
"\306|\313=\276|\321=============\316============",
"\306|\313$\275^\310&",
"\306|^^^^^^^^^^^^^^\314$\321^\304======",
"*\277.\314&\317^\321H*^\276^\320^\313^^^^^^^^^^^^",
"==============================================================================="
]]

class DIR(enum.Enum):
    NONE  = -1
    STOP  = 0
    XUP   = 1
    XDOWN = 2
    LEFT  = 3
    RIGHT = 4

class LAD:
    row    = 0
    col    = 0
    st_row = 0
    st_col = 0
    dir    = DIR.NONE
    jst    = 0


laddirs = "gbdqp"

class DER:
    row    = 0
    col    = 0
    dir    = DIR.NONE
    launch = 0 

class RELEASE:
    row = EOF
    col = EOF

def SOLID(C):
    return ((C) == CBAR or (C) == CGROUND or (C) == CTRAP1)

dchoice = [DIR.LEFT,DIR.RIGHT,DIR.XDOWN];

def LorR():
    return (dchoice[rand() % 2])
    
def LorRorD():
    return (dchoice[rand() % 3])

def unmerge(s):
    t = ''
    for c in s: 
        if( ord(c) & 0o200 ):
           t = t +(210-ord(c))*' '
        else:
            t = t + c
    return t

class Game(object):
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.boni = []
        self.scrno = 0
        self.speed = 0
        self.diff = 0
        self.last = 0
        self.lads = 0
        self. score = 0
        self. level = 0
        self.lad = LAD()

    def mexit0(self):
        self.stdscr.refresh()
        curses.noraw()
        curses.echo()
        curses.endwin()
        exit(0)

    def mexit1(self):
        self.stdscr.move(23,0)
        self.mexit0()

    def  getch(self):
        return msvcrt.getch()

    def instructions(self):
        text = [
            "You are a Lad trapped in a maze.  Your mission is to explore the",
            "dark corridors never before seen by human eyes and find hidden",
            "treasures and riches.","",
            "You control Lad by typing the direction buttons and jumping by",
            "typing SPACE.  But beware of the falling rocks called Der rocks.",
            "You must find and grasp the treasure (shown as $) BEFORE the",
            "bonus time runs out.","",
            "A new Lad will be awarded for every 10,000 points.",
            "Extra points are awarded for touching the gold",
            "statues (shown as &).  You will receive the bonus time points",
            "that are left when you have finished the level.",
            "Remember, there is more than one way to skin a cat. (Chum)",
            "Type an ESCape to pause the game.","",
            "Good luck Lad.","","",
            "Type RETURN to return to main menu: "
            ]

        self.stdscr.clear();
        for r in range(len(text)):
            self.stdscr.addstr(r + 2,4,text[r])
        self.stdscr.refresh()
        self.stdscr.nodelay(False)
        self.stdscr.getch()
        self.stdscr.nodelay(True)

    def getcmd(self, row, col):
        funny = [
            "You eat quiche!",
            "Come on, we don't have all day!"
        ]
        
        count = 0
        while(True):

            #stdscr.addstr(row,col,"Enter one of the above: ")
            #stdscr.refresh()
            #if(select.select([sys.stdout], [], [], 10.0)):
            #    break
            #stdscr.addstr(row + 2,col,funny[random.randint(0,len(funny)-1)])
            #stdscr.refresh()
            #select([sys.stdin], [], [], 0.5)
            #stdscr.move(row + 2,col)
            #stdscr.clrtoeol()
            #mykey = sys.stdin.read(1)
            self.stdscr.addstr(row,col,"Enter one of the above: ")
            self.stdscr.refresh()
            if msvcrt.kbhit():
                mykey = chr(self.stdscr.getch())
                break
            time.sleep(0.2)
            count += 1
            if (count > 35):
                self.stdscr.addstr(row + 2,col,funny[random.randint(0,len(funny)-1)])
                self.stdscr.refresh()
                time.sleep(3)
                self.stdscr.move(row + 2,col)
                self.stdscr.clrtoeol()
                count = 0

        return mykey

    def menu(self):
        
        LM  = 2
        RM0 = 33
        RM1 = 40

        text = [
                "LL\275dd\313dd",
                "LL\275dd\313dd\274tm",
                "LL\311aaaa\315ddddd\316ddddd\316eeee\317rrrrrrr",
                "LL\312aa\320aa\317dd\320dd\317dd\320dd\317ee\320ee\320rr\316rr",
                "LL\312aa\320aa\317dd\320dd\317dd\320dd\317eeeeee\320rr",
                "LL\312aa\320aa\317dd\320dd\317dd\320dd\317ee\314rr",
                "LLLLLLLL\317aaa\321aa\317ddd\321dd\317ddd\321dd\317eeee\317rr"
        ]

        for r in range(len(text)):
            self.stdscr.addstr(r + 1,11,unmerge(text[r]))
        r += 3
        self.stdscr.addstr(r,LM,
            "(c) in 1982, 1983: Yahoo Software, ported to Python by Gerhard Scheutz (aka Kerm).")
        r += 2
        self.stdscr.addstr(r,LM,"Version:    1.0 Python")
        self.stdscr.addstr(r,RM0,"Up = k|8  Down = j|2  Left = h|4  Right = l|6")
        r += 1
        self.stdscr.addstr(r,LM,"Terminal:   %s" % curses.termname())
        self.stdscr.addstr(r,RM0,"Jump = Space   Stop = Other")
        r += 1
        self.stdscr.addstr(r,LM,"Play Speed: %d" % (self.speed + 1))
        r += 1
        ###prt_score(r,RM1)
        r += 1
        self.stdscr.addstr(r, LM, "P = Play game")
        r += 1
        self.stdscr.addstr(r, LM, "L = Change level of difficulty")
        r += 1
        self.stdscr.addstr(r, LM, "I = Instructions")
        r += 1
        self.stdscr.addstr(r, LM, "E = Exit Ladder")
        r += 1
        self.stdscr.refresh()
        return self.getcmd(r, LM)
        
    def play(self):
        
        self.boni = st_boni
        self.lads = 5
        self.score = 0
        self.scrno = 0
        hi_scrno = 1
        
        self.stdscr.clear()
        while True:
            level = 0
            if self.lplay() == DEAD:
                break
            boni[scrno] -= 2
            scrno = scrno+1
            if scrno > hi_scrno:
                if hi_scrno != (DIMSCRN - 1):
                    hi_scrno += 1
                scrno = 0
            level += 1
        upd_score()

    def run(self):
        #stdscr = curses.initscr()
        if(self.stdscr == None):
            print("Ladder: Curses initialization failed.\n", file=sys.stderr)
            exit(1)
        
        if( curses.LINES < 24 or curses.COLS < 80 ):
            print("Ladder: Unsufficient Screen Dimensions.",  file=sys.stderr)
            self.mexit0()

        curses.cbreak()
        curses.noecho()
        self.stdscr.nodelay(True)
        self.stdscr.leaveok(True)
        # pad(stdscr,TRUE)
        curses.typeahead(-1)
        signal.signal(signal.SIGINT, self.mexit1)
        signal.signal(signal.SIGTERM, self.mexit1)
        random.seed(os.getpid())

        self.stdscr.clear()
        while( True ):
            c =  str(self.menu()).upper()
            if (c == 'P'):
                self.play()
                self.stdscr.clear()

            elif (c == 'I'):
                self.instructions()
                self.stdscr.clear()

            elif (c == 'L'):
                self.speed = self.speed + 1
                if( self.speed == HISPEED ):
                    self.speed = 0

            elif (c == chr(ord('R')-ord('@')) or
                  c == chr(ord('L')-ord('@')) or
                  c == curses.KEY_CLEAR):
                    self.stdscr.refresh()

            elif (c == 'E'):
                self.mexit1()
            else:
                curses.flash()
                
    #/* these extra "00" in score & bonus are extremly silly - 
    #   but that is how the original did it */
    def stat_lads(self):
        self.stdscr.addstr(DIMROW,0,"Lads  %3d",self.lads)

    def stat_level(self):
        self.stdscr.addstr(DIMROW,14,"Level  %3d",self.level + 1)

    def stat_score(self):
        self.stdscr.addstr(DIMROW,29,"Score  %4d00",self.score)

    def stat_bonus(self):
        self.stdscr.addstr(DIMROW,59,"Bonus time  %4d00",self.bonus)

    def add_score(self,  add):
        if( self.score / 100 < (self.score + add) / 100 ):
            self.lads += 1
            stat_lads()
        self.score += add
        stat_score()

    def ldscreen(self):
        row = 0
        i = 0
        self.rel = [RELEASE() for j in range(3)]

        self.bg = [ ' ' * ROWCOL for j in range(DIMROW) ]

        for row in range(DIMROW): 
            s = screens[scrno][row]
            t = bg[row];

            bg[row] = unmerge(s)
            t = unmerge(s)
            stdscr.addstr(row,0,t)

            #/* find points of release */
            for c in [pos for pos, char in enumerate(t) if char == CRELEAS]:
                self.rel[i].row = Row
                self.rel[i].col = c
                i += 1
                
        #/* mark the rest of releases */
        #for( ; rel < &releases[DIM(releases)]; rel++ )
        #    rel->row = rel->col = EOF;

        #/* find lad */
        for row in rage(DIMROW): 
            #for( s = t = bg[row]; s = strchr(s,CLAD); s++ )
            s = self.bg[row]
            for c in [pos for pos, char in enumerate(s) if char == CLAD]:
                #/* nasty, check for CLAD's surrounded by CFREEs */
                if( s[c-1] != CFREE or s[c+1] != CFREE ):
                    continue
                self.lad.row = self.lad.st_row = row
                self.lad.col = self.lad.st_col = c
                self.lad.dir = NONE
                self.lad.jst = 0
                self.bg[lad.row][lad.col] = CFREE
                break

        #/* init ders */
        if self.ders == None:
            hi = -1
            for i in range(DIMSCRN):
                if hi < hiders[i]:
                    hi = hiders[i]
            self.ders = [DER() for i in range(hi+1)]
            self.ders[hi].row = EOF

        for i in  range(hiders[scrno]):
            self.ders[i].launch = i + 1
            self.ders[i].dir = DIR.XDOWN

        while self.ders[i].row != EOF:
            self.ders.launch = -1

        self.stdscr.move(LINES - 1, 0)
        self.stdscr.refresh()

    def reldscreen(self):
        for row in range(DIMROW):
            self.stdscr.addstr(row,0,bg[row])

        #/* deal with lad */
        self.lad.row = self.lad.st_row
        self.lad.col = self.lad.st_col
        self.lad.dir = None
        self.lad.jst = 0
        self.stdscr.mvaddch(self.lad.row,self.lad.col,CLAD);

        #deal with ders
        for i in range(hiders[scrno]):
            self.ders[i].launch = i + 1
            self.ders[i].dir = XDOWN

        self.stdscr.move(LINES - 1, 0)
        self.stdscr.refresh()
        
    # drive a single der, tell whether it left the board or hit lad
    def drv_der(self, dp):
        row = dp.row
        col  = dp.col
        dir   = dp.dir
        c = ""

        c = bg[row][col]       #/* restore prev content */
        self.stdscr.mvaddch(row,col,c);
        if c == CEXIT:
            return EXIT
            
        while(True):
            if dir == DIR.XDOWN:
                c = bg[row + 1][col]
                if SOLID(c):
                    dir = LorR()
                    continue
                row = row + 1
                break
                
            if dir == DIR.LEFT:
                if( col == 0 or bg[row][col - 1] == CBAR ):
                    dir = DIR.RIGHT
                    continue
                col = col - 1
                
            if dir == DIR.RIGHT:
                if( col == DIMCOL - 2  or bg[row][col + 1] == CBAR ):
                    dir = DIR.LEFT
                    continue
                col = col + 1
                
            if bg[row][col] == CLADDER:
                dir = LorRorD();
            else:
                c = bg[row + 1][col]
                if  not SOLID(c) :
                    dir = DIR.XDOWN;
            break;

        c = self.stdscr.mvinch(row,col)
        self.stdscr. addch(CDER)
        dp.row = row
        dp.col = col
        dp.dir = dir
        
        if c in laddirs:
            return NORMAL
        else:
            return DEAD
        
def main(stdscr):
    game = Game(stdscr) 
    game.run()
    
if __name__ == "__main__":
    curses.wrapper(main)
