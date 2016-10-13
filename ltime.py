import time

def waittcs(tcs):
    time.sleep(tcs)
    
#/* set 'em */
def setct(msec):

    global diff
    global last

    diff = msec/1000 + 1
    last = time.time

def ctplay():
    global speed

    speeds = [125,100,80,60,40]
    setct(speeds[speed])

#/* for killed lad & hookas */
def ctnplay():
    setct(25)

def waitct():
    global diff
    global last
    now = time.time()
    
    last += diff
    if( now >= last ):
        last = now
    else:
        waittcs(last - now)