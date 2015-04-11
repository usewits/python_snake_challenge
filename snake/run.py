import pexpect



player = "python example.py"
max_mem = 100000        #in kb
core_id = "0x1"
pexpect.spawn("./timeout -m "+str(max_mem)+" taskset "+core_id+" "+player)

#TODO: now pipe in.txt to player
#

