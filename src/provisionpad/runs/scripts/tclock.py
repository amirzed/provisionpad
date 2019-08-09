import psutil
import time
import os
from os.path import expanduser
home = expanduser("~")
total_idlef = os.path.join(home, '.provisionpad/data/total_idle.out')
delta_idlef = os.path.join(home, '.provisionpad/data/delta_idle.out')
idle_time = psutil.cpu_times().idle
the_time  = time.time()
with open(total_idlef, 'r') as f:
    data = f.read().strip().split()
str = '%f %f' % (idle_time, the_time)
if len(data) != 2:
    with open(total_idlef, 'w') as f:
        f.write(str)
    with open(delta_idlef, 'w') as f:
        f.write('0\n')
else:
    idle_diff = (idle_time-float(data[0]))/(the_time-float(data[1]))
    with open(total_idlef, 'w') as f:
        f.write(str)
    with open(delta_idlef, 'a+') as f:
        f.write("%f\n" % idle_diff )  
    with open(delta_idlef, 'r') as f:
        data = f.read().splitlines()
        if float(data[-1])>0.97 and abs(float(data[-1])-float(data[-2]))<0.002:
            os.system('sudo poweroff')
