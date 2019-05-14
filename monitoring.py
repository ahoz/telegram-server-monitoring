#!/usr/bin/env python3
import sys, os
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT

checkdisk = {}
checkdisk['sda1'] = {'diskpath' : '/dev/sda1', 'threshhold' : '20%', 'unit' : 'GB'}

def syscmd(cmd, encoding=''):
    """
    Runs a command on the system, waits for the command to finish, and then
    returns the text output of the command. If the command produces no text
    output, the command's return code will be returned instead.
    """
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT,
        close_fds=True)
    p.wait()
    output = p.stdout.read()
    if len(output) > 1:
        if encoding: return output.decode(encoding)
        else: return output.decode("utf-8")
    return p.returncode

def userlogin():
	return syscmd("echo Login auf $(hostname) am $(date +%Y-%m-%d) um $(date +%H:%M) - USER: $USER")

def checkdisk(diskpath, threshhold, unit):
	return syscmd("/usr/lib/nagios/plugins/check_disk -w "+threshhold+" -p "+diskpath+" -u "+unit+" | cut -f1 -d \";\"")

def checkapt():
	return syscmd("/usr/lib/nagios/plugins/check_apt | cut -f1 -d\".\"")

def writefile(file, content):
	f = open(file, "w")
	f.write(content)
	f.close()

def readfile(file):
	f = open(file, "r")
	f.read()
	f.close()

if int(sys.argv[1]) == 1:
	ss = syscmd("ls")
	print(ss)

# declare -a container=("element1" "element2" "element3")

# if [ $1 -eq 1 ]
# then
#         # user login
#         /opt/send_tg_info.sh 2 Login auf $(hostname) am $(date +%Y-%m-%d) um $(date +%H:%M) - USER: $USER
# elif [ $1 -eq 2 ]
# then
#         # chech disk free
#         DISK_CURRENT=$(/usr/lib/nagios/plugins/check_disk -w 20% -p /dev/sda1 -u GB | cut -f1 -d";")
#         STATUS=$(echo $DISK_CURRENT | sed -e 's/DISK OK/1/g' | head -c1)
#         if [ ! "$STATUS" == "1" ]
#         then
#                 /opt/send_tg_info.sh 3 $DISK_CURRENT
#         fi
#         #echo $DISK_CURRENT
# elif [ $1 -eq 3 ]
# then
#         # updates
#         APT_CURRENT=$(cat /opt/monitoring_tmp/apt_status)
#         APT_RESULT=$(/usr/lib/nagios/plugins/check_apt | cut -f1 -d".")
#         if [[ $APT_RESULT = *"timed out"* ]]; then
#                 exit 0
#         fi
#         echo $APT_RESULT > /opt/monitoring_tmp/apt_status
#         if [ !  "$APT_CURRENT" == "$APT_RESULT" ]; then
#                 /opt/send_tg_info.sh 1 $APT_RESULT
#         fi
