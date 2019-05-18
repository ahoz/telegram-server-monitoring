#!/usr/bin/env python3
import sys, os, hashlib, requests, re
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT

CHATID=''
APIKEY=''

checkdisks = {}
checkdisks['sda1'] = {'diskpath' : '/dev/sda1', 'threshhold' : '20%', 'unit' : 'GB'}

def syscmd(cmd, encoding=''):
    """ 
        Execute Shell Command

    Args:
        cmd:        str, cmd command
        encoding:   str, encoding

    Returns:
        Output on Success or Returncode in Failure
    """
    p = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    p.wait()
    output = p.stdout.read()
    if len(output) > 1:
        if encoding: return output.decode(encoding)
        else: return output.decode("utf-8")
    return p.returncode

def userlogin():
    """ 
        Returns User Login Message
    """
    return syscmd("echo Login auf $(hostname) am $(date +%Y-%m-%d) um $(date +%H:%M) - USER: $USER")

def checkdisk(diskpath, threshhold, unit):
    """ 
        Checks Diskusage with Nagios Plugin

    Args:
        diskpath:   str, /dev/sdXY (e.g. /dev/sda1)
        threshhold: str, threshhold (10%, 10GB, 20%,...)
        unit:       str, unit (GB, MB,...)

    Returns:
        Returns Output on Critical Status, Empty String Otherwise
    """
    output = syscmd("/usr/lib/nagios/plugins/check_disk -w "+threshhold+" -p "+diskpath+" -u "+unit+" | cut -f1 -d \";\"")
    matchObj = re.match( r'DISK OK(.*?) .*', output, re.M|re.I)
    if matchObj:
    	return ""
    return output

def checkapt():
	""" 
        Checks apt packages

    Returns:
    	Checks if Something has Changed Since Last Time and Returns Output, Empty String Otherwise
    """
    apt = syscmd("/usr/lib/nagios/plugins/check_apt | cut -f1 -d\".\"")
    if md5(apt) in md5(readfile("./cache/aptcheck")): return ""
    writefile("./cache/aptcheck", apt)
    return apt

def writefile(file, content):
	""" 
        Write a file

    Args:
        file:  	str, filepath
        content:str, file content
    """
    f = open(file, "w")
    f.write(content)
    f.close()

def readfile(file):
	""" 
    	Reads a File    

    Args:
		file:	str, filepath

    Returns:
        Returns File Content, Empty String Otherwise
    """
    f = open(file, "r")
    file = f.read()
    f.close()
    return file

def sendMessage(apikey, chatid, message):
	 """ 
        Sends Message to Telegram

    Args:
        apikey:	str, Telegram API Key
        chatid: str, Telegram ChatID
        message:str, Message
    """
    data = { 'chat_id': chatid, 'text': message }
    response = requests.post('https://api.telegram.org/bot'+apikey+'/sendMessage', data=data)


def md5(string):
	 """ 
        Converts a string to md5

    Args:
        string:	str, any string

    Returns:
        Returns Output on Critical Status, Empty String Otherwise
    """
    return hashlib.md5(string.encode('utf-8')).hexdigest()

def main(APIKEY, CHATID, argv):
	""" 
        Main Method

    Args:
        APIKEY:	str, Telegram API Key
        CHATID: str, Telegram ChatID
        argv:	str, argv
    """
    try:
        arg = argv[1]
    except:
        print("error")
        sys.exit(1)

    if int(arg) == 1:
        sendMessage(APIKEY, CHATID, userlogin())
    elif int(arg) == 2:
        for disk in checkdisks:
            sendMessage(APIKEY, CHATID, checkdisk(checkdisks[disk]['diskpath'], checkdisks[disk]['threshhold'], checkdisks[disk]['unit']))
    elif int(arg) == 3:
        apt = checkapt()
        if len(apt)>0:
            return sendMessage(APIKEY, CHATID, apt) 
        

if __name__== "__main__":
    main(APIKEY, CHATID, sys.argv)
