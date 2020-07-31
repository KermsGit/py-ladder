import enum

from ladder_h import *

#typedef enum { NONE, STOP = 0, XUP = 1, XDOWN = 2, LEFT = 3, RIGHT = 4 } DIR

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

lad = LAD()
laddirs = "gbdqp"

class DER:
    row    = 0
    col    = 0
    dir    = DIR.NONE
    launch = 0    

ders = None

class RELEASE:
    row = EOF
    col = EOF

releases = [RELEASE() for i in range(3)]
bonus = 0

bg = []
hiders = [0 for i in range(DIMSCRN)]

#/* these extra "00" in score & bonus are extremly silly - 
#   but that is how the original did it */
def stat_lads(stdscr):
    stdscr.addstr(DIMROW,0,"Lads  %3d",lads)

def stat_level(stdscr):
    stdscr.addstr(DIMROW,14,"Level  %3d",level + 1)

def stat_score(stdscr):
    stdscr.addstr(DIMROW,29,"Score  %4d00",score)

def stat_bonus(stdscr):
    stdscr.addstr(DIMROW,59,"Bonus time  %4d00",bonus)

def add_score(add):
    if( score / 100 < (score + add) / 100 ):
        lads = lads +1
        stat_lads()
    score = score + add
    stat_score()

def ldscreen(stdscr):
    row = 0
    i = 0
    rel = RELEASE()
    s = ''  # pointer to char 
    t = ''

    bg = [ ' ' * ROWCOL for j in range(DIMROW) ]

    for row in range(DIMROW): 
        s = screens[scrno][row]
        t = bg[row];

        bg[row] = memcpy(bg[row], unmerge(s))
        t = unmerge(s)
        stdscr.addstr(row,0,t)

        #/* find points of release */
        for c in [pos for pos, char in enumerate(t) if char == CRELEAS]:
            releases[i].row = Row
            releases[i].col = c
            i = i + 1
            
    #/* mark the rest of releases */
    #for( ; rel < &releases[DIM(releases)]; rel++ )
    #    rel->row = rel->col = EOF;

    #/* find lad */
    for row in rage(DIMROW): 
        #for( s = t = bg[row]; s = strchr(s,CLAD); s++ )
        s = bg[row]
        for c in [pos for pos, char in enumerate(s) if char == CLAD]:
            #/* nasty, check for CLAD's surrounded by CFREEs */
            if( s[c-1] != CFREE or s[c+1] != CFREE ):
                continue
            lad.row = lad.st_row = row
            lad.col = lad.st_col = c
            lad.dir = NONE
            lad.jst = 0
            bg[lad.row][lad.col] = CFREE
            break

    #/* init ders */
    if ders == None:
        hi = -1
        for i in range(DIMSCRN):
            if hi < hiders[i]:
                hi = hiders[i]
        ders = [DER() for i in range(hi+1)]
        ders[hi].row = EOF

    for i in  range(hiders[scrno]):
        ders[i].launch = i + 1
        ders[i].dir = DIR.XDOWN

    for d in ders:
        if d.row == EOF:
            break
        ders.launch = -1

    stdscr.move(LINES - 1, 0)
    refresh()

def reldscreen():

    for row in range(DIMROW):
        stdscr.addstr(row,0,bg[row])

    #/* deal with lad */
    lad.row = lad.st_row
    lad.col = lad.st_col
    lad.dir = None
    lad.jst = 0
    mvaddch(lad.row,lad.col,CLAD);

    #deal with ders
    for i in range(hiders[scrno]):
        ders[i].launch = i + 1;
        ders[i].dir = XDOWN;

    move(LINES - 1, 0);
    refresh();

def SOLID(C):
    return ((C) == CBAR or (C) == CGROUND or (C) == CTRAP1)

dchoice = [DIR.LEFT,DIR.RIGHT,DIR.XDOWN];

def LorR():
    return (dchoice[rand() % 2])
    
def LorRorD():
    return (dchoice[rand() % 3])
    
# drive a single der, tell whether it left the board or hit lad
def drv_der(dp):
    row = dp.row
    col  = dp.col
    dir   = dp.dir
    c = ""

    c = bg[row][col]       #/* restore prev content */
    mvaddch(row,col,c);
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

    c = mvinch(row,col)
    addch(CDER)
    dp.row = row
    dp.col = col
    dp.dir = dir
    
    if c in laddirs:
        return NORMAL
    else:
        return DEAD

def drv_ders(ders):
    for derp in ders:
    #for( derp = ders; derp->row != EOF; derp++ )
        if derp.launch == -1:
            continue;
        if derp.launch == 0:
            result = drv_der(derp)
            if result == DEAD:
                return DEAD
            if result == EXIT:
                derp.launch = 5       #/* set new start time */
            continue

        derp.launch = derp.launch -1
        if derp.launch == 0:
            #/* select a point of release */
            while( True ):
                n = rand() % len(releases)
                if releases[n].row != EOF:
                    derp.row = releases[n].row
                    derp.col = releases[n].col
                    derp.dir = XDOWN
                    break
    return NOTHING_HAPPENED

def lad_died():
    rot = "b+d+q+p+";
    ctnplay();
    for i  in range(5):
        for j in len(rot):
            mvaddch(lad.row,lad.col,rot[j]);
            move(LINES - 1,0);
            refresh();
            waitct();

def do_the_hooka():
    bonus = bonus -1
    while bonus >= 0:
        add_score(1)
        stat_bonus()
        move(DIMROW + 2,0)
        if bonus & 1 :
            addstr("Hooka!");
        else:
            clrtoeol()
        move(LINES - 1,0)
        refresh()
        waitct()
        bonus = bonus -1

def pause():
    mvaddstr(DIMROW + 2,0,"Type RETURN to continue: ")
    refresh()
    nodelay(stdscr,FALSE)
    while getch() != '\n':
        pass
    nodelay(stdscr,TRUE)
    move(DIMROW + 2,0)
    clrtoeol()

def over_der(row, col):
    #/* Funny how lad jumps over "Sc`o're" - avoid it? Na. */
    if mvinch(row + 1,col) == CDER or mvinch(row + 2,col) == CDER:
        add_score(2)

def drv_lad():
    row = lad.row
    col = lad.col
    dir = lad.dir
    jst = lad.jst
    c0 = ''
    c1 = ''

    while (True):
        ch = getch()
        if ch == ERR:   #/* no key */
            break

        if ch == 'h' or ch == '4' or ch == KEY_LEFT:
            dir = LEFT
            break

        if ch == 'l' or ch == '6' or ch == KEY_RIGHT:
            dir = RIGHT
            break
        
        if ch == 'k' or ch == '8' or ch == KEY_UP:
            if  not jst:
                dir = XUP
            break;

        if ch == 'j' or ch == '2' or ch == KEY_DOWN:
            if not jst:
                dir = XDOWN
            break

        if ch ==' ':
            if not jst:      #/* not while we're jumping */
                jst = 1
            break

        if ch == chr(ord('R')-ord('@')) or ch == chr(ord('L')-ord('@'))  or ch == KEY_CLEAR:
            wrefresh(curscr)
            break
        
        if ch ==  chr(ord('[')-ord('@')):
            return PAUSE;

        if ch == chr(ord('C')-ord('@')):       #/* who does set INTR to ^C, anyway? */
            while(lads >= 1):
                stat_lads()
                move(LINES - 1, 0)
                refresh()
                waitct()
                lads = lads - 1
            lads = 1
            return DEAD

        dir = STOP

    c0 = bg[row][col]
    c1 = bg[row + 1][col]
    if jst < 2 and not SOLID(c1) and c0 != CLADDER and not (jst == 1 and c0 == CHAZARD):
        #/* then fall */
        jst = 0        #/* no request for jumping */
        row = row + 1
    else:
        if jst >= 1:   #/* request for or within a jump */
            if jst == 1 and c1 == CFREE and c0 != CHAZARD:
                jst = 0
            else:
                jra[7] = [ 0, -1, -1, 0, 0, 1, 1 ]
                jc = 0
                jr = 0

                over_der(row,col)
                if dir == XUP or dir == XDOWN:
                    dir = STOP
                while(jst != 7):
                    jr = jra[jst]
                    if dir == STOP:
                        jc = 0
                    elif dir == LEFT:
                        jc = -1
                    else:
                        jc = 1
                        
                    c0 = bg[row + jr][col + jc]
                    if c0 != CBAR and c0 != CGROUND and not (jr == 1 and c0 == CTRAP1):
                        row = row + jr
                        if row < 0 or row > (DIMROW - 2):
                            row = row - jr
                        col = col + jc
                        if col < 0 or col > (DIMCOL - 2):
                            col = col - jc
                        break
                    jst = jst +1
                
                jst = jst + 1
                if jst >= 7:
                    jst = 0
                if bg[row][col] == CLADDER:
                    jst = 0
                    dir = STOP
                if dir != STOP:
                    over_der(row,col)
        else:
            if c1  == CTRAP1:
                bg[row + 1][col] = CFREE
                mvaddch(row + 1,col, CFREE)
                
            if dir == LEFT:
                c1 = bg[row][col - 1]
                if col != 0 and c1 != CBAR and c1 != CGROUND:
                    col = col - 1
                else:
                    dir = STOP
                #break
            
            if dir == RIGHT:
                c1 = bg[row][col + 1]
                if col != (DIMCOL - 2) and c1 != CBAR and c1 != CGROUND:
                    col = col +1
                else:
                    dir = STOP
                #break
                
            if dir == XUP:
                if c0 == CLADDER:
                    c0 = bg[row - 1][col]
                    if c0== CLADDER or c0 == CTARGET:
                        row = row - 1;
                else:
                    dir = STOP
                #break
                
            if dir == XDOWN:
                if c0 == CLADDER and c1 != CGROUND:
                    row = row + 1
                else:
                    dir = STOP;
                break


    if lad.row != row or lad.col != col or lad.dir != dir or lad.jst != jst:
        mvaddch(lad.row,lad.col,bg[lad.row][lad.col])
        #/* remove rubbish */
        s = CGOLD+CRELEAS+CLADDER+CTARGET+CEXIT+CBAR+CGROUND+CHAZARD+CTRAP0+CTRAP1+CFREE
        if not bg[row][col] in s:
            bg[row][col] = CFREE
            mvaddch(row,col,CFREE)
        #/* check for anything that matters */
        if bg[row][col] == CGOLD:
            bg[row][col] = CFREE
            mvaddch(row,col,CFREE)
            add_score(bonus)
        if bg[row][col] == CHAZARD:
            dir = rand()
            if rand & 1:
                dir = LEFT
            else:
                dir = RIGHT
            jst = rand() & 1
        lad.row = row
        lad.col = col
        lad.dir = dir
        lad.jst = jst
        if mvinch(row,col) == CDER:
            return DEAD
        addch(laddirs[dir])
        
    if bg[row][col] == CTARGET:
        return FINISH
    if bg[row][col] == CTRAP0:
            return DEAD
    return NORMAL

def lplay():

    ldscreen();

    while( lads > 0 ):
        bonus = boni[scrno]
        ctplay()
        stat_lads()
        stat_level()
        stat_score()
        stat_bonus();
        mvaddstr(DIMROW + 2,0,"Get ready! ")
        refresh()
        for tick in range(7,  -1,  0):
            waitct()
        move(DIMROW + 2,0);
        clrtoeol();
    
        for tick in range(20 * bonus, -1,  0 ):
            if not ((tick - 1) % 20):
                bonus = bonus -1
                stat_bonus()
            result = drv_ders()
            if  result != DEAD:
                result = drv_lad()
            move(LINES - 1,0);
            refresh()
            waitct()
            if result == PAUSE:
                pause()
                result = NORMAL
            if result != NORMAL:
                break;
    
        if not tick:
            result = DEAD
        if result == DEAD:
            lads = lads - 1
            stat_lads()
            lad_died()
            
        if result == FINISH:
            do_the_hooka();
            return NORMAL
        reldscreen()
    return DEAD

