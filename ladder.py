#!/usr/bin/env python

import sys
import curses
import signal
import random
import os
import select
import msvcrt
import time

from ltime import *
from lscreens import *

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
speed = 0
diff = 0
last = 0
lads = 0
score = 0
level = 0

boni = [0 for i in range(DIMSCRN)]

gstdscr     = False

def unmerge(s):
    t = ''
    for c in s: 
        if( ord(c) & 0o200 ):
           t = t +(210-ord(c))*' '
        else:
            t = t + c
    return t

def memcpy(dst, src):
    for i in range(len(src)):
        dst[i] = src[i] 

def mexit0():
    global gstdscr
    gstdscr.refresh()
    curses.noraw()
    curses.echo()
    curses.endwin()
    exit(0)

def mexit1():
    global gstdscr
    gstdscr.move(23,0)
    mexit0()

def  getch():
    return msvcrt.getch()

def instructions(stdscr):
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

    stdscr.clear();
    for r in range(len(text)):
        stdscr.addstr(r + 2,4,text[r])
    stdscr.refresh()
    stdscr.nodelay(False)
    stdscr.getch()
    stdscr.nodelay(True)

def getcmd(stdscr, row, col):
    funny = [
        "You eat quiche!",
        "Come on, we don't have all day!"
    ]
    
    myKey = ''
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
        stdscr.addstr(row,col,"Enter one of the above: ")
        stdscr.refresh()
        if msvcrt.kbhit():
            mykey = chr(stdscr.getch())
            break
        time.sleep(0.2)
        count += 1
        if (count > 35):
            stdscr.addstr(row + 2,col,funny[random.randint(0,len(funny)-1)])
            stdscr.refresh()
            time.sleep(3)
            stdscr.move(row + 2,col)
            stdscr.clrtoeol()
            count = 0

    return mykey

def menu(stdscr):
    global speed
    
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
        stdscr.addstr(r + 1,11,unmerge(text[r]))
    r += 3
    stdscr.addstr(r,LM,
        "(c) in 1982, 1983: Yahoo Software, ported to Python by Gerhard Scheutz (Kerm).")
    r += 2
    stdscr.addstr(r,LM,"Version:    1.0 Python")
    stdscr.addstr(r,RM0,"Up = k|8  Down = j|2  Left = h|4  Right = l|6")
    r += 1
    stdscr.addstr(r,LM,"Terminal:   %s" % curses.termname())
    stdscr.addstr(r,RM0,"Jump = Space   Stop = Other")
    r += 1
    stdscr.addstr(r,LM,"Play Speed: %d" % (speed + 1))
    r += 1
    ###prt_score(r,RM1)
    r += 1
    stdscr.addstr(r, LM, "P = Play game")
    r += 1
    stdscr.addstr(r, LM, "L = Change level of difficulty")
    r += 1
    stdscr.addstr(r, LM, "I = Instructions")
    r += 1
    stdscr.addstr(r, LM, "E = Exit Ladder")
    r += 1
    stdscr.refresh()
    return getcmd(stdscr, r, LM)
    
def play(stdscr):
    global lads
    global score
    global scrno
    
    hi_scrno = 0
    memcpy(boni,st_boni)
    lads = 5
    score = 0
    scrno = 0
    hi_scrno = 1
    
    stdscr.clear()
    while True:
        level = 1
        if lplay(stdscr) == DEAD:
            break
        boni[scrno] -= 2
        scrno = scrno+1
        if scrno > hi_scrno:
            if hi_scrno != (DIMSCRN - 1):
                hi_scrno = hi_scrno +1
            scrno = 0
        level = level + 1
    upd_score()

def main(stdscr):
    global gstdscr
    global speed

    gstdscr = stdscr
    #stdscr = curses.initscr()
    if(stdscr == None):
        fputs("Curses initialization failed.\n",stderr)
        exit(1)
    
    if( curses.LINES < 24 or curses.COLS < 80 ):
        addstr("Unsufficient Screen Dimensions.")
        mexit0()

    curses.cbreak()
    curses.noecho()
    stdscr.nodelay(True)
    stdscr.leaveok(True)
    # pad(stdscr,TRUE)
    curses.typeahead(-1)
    signal.signal(signal.SIGINT, mexit1)
    signal.signal(signal.SIGTERM, mexit1)
    random.seed(os.getpid())

    stdscr.clear()
    while( True ):
        c =  str(menu(stdscr)).upper()
        if (c == 'P'):
            play(stdscr)
            stdscr.clear()

        elif (c == 'I'):
            instructions(stdscr)
            stdscr.clear()

        elif (c == 'L'):
            speed += 1
            if( speed == HISPEED ):
                speed = 0

        elif (c == chr(ord('R')-ord('@')) or
              c == chr(ord('L')-ord('@')) or
              c == curses.KEY_CLEAR):
                curscr.wrefresh()

        elif (c == 'E'):
            mexit1()
        else:
            curses.flash()

    mexit1()

if __name__ == "__main__":
    curses.wrapper(main)
