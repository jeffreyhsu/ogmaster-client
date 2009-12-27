#!/usr/bin/python

##############################################################################
# Emilio Schapira
# Copyright (C) 2003 Advanced Interface Technologies, Inc.
# http://www.advancedinterfaces.com
# http://sourceforge.net/projects/pycron/
# 
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
# 
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

"""
usage: cron [crontab_file_name [log_file_name [pid_file_name]]]
       This is a minimal cron clone that can be used in windows.
       It writes a log in the current directory, and looks for the
       crontab file in the current directory unless otherwise specified by
       the command line argument.
"""

import time
import os
import sys
import string

def log(msg):
    f = file(logFileName,'a')
    f.write(time.ctime(time.time()) + " " + msg + "\n")

def run(command):
    log(command)
    try:
        # This is the only windows dependant call
        # We use start because we want to spawn the
        # shell command in another process, and not wait
        if os.name == 'nt':
            os.system('start ' + command)
        else:
            os.system(command)
    except:
        log('cron: last command failed to start')

def match(value, expr):
    if expr == '*':
        return 1
    values = string.split(expr,',')
    for v in values:
        if int(v) == value:
            return 1
    return 0

def calcNextTime():    
    # Calculate next time with exact seconds.
    tt = time.localtime(time.time() + 60)
    tt = tt[:5] + (0,) + tt[6:]
    return time.mktime(tt)


crontabFileName = "./crontab"
logFileName = "./cron.log"
pidFileName = "./cron.pid"

try:
    crontabFileName = sys.argv[1]
    logFileName = sys.argv[2]
    pidFileName = sys.argv[3]
except:
    pass

# Write the pid in the current directory.
f = file(pidFileName,'w')
f.write(str(os.getpid()))
f.close()

# Log cron start
log('cron: started with file %s' % crontabFileName)

nextTime = calcNextTime()

# Loop forever
while 1:

    # Sleep for the time remaining until the next exact minute
    currentTime = time.time()

    if currentTime < nextTime:
        # Add a fraction of a second to make sure we are in
        # the right second (just for prettier logs)
        time.sleep(nextTime-currentTime+.1)

    # Check if the time has changed by more than two minutes. This
    # case arises when the system clock is changed. We must reset the timer.
    if abs(time.time() - nextTime) > 120:
        log('Adjusted system clock.')
        nextTime = calcNextTime()
        
    # Build a tuple with the current time
    curTuple = time.localtime(nextTime)

    # Read the crontab file
    try:
        lines = file(crontabFileName,'r').readlines()
        lineNum = 1
        for line in lines:
            # Ignore comments
            if line[0] != '#' and len(string.strip(line)) != 0:
                try:
                    tokens = string.split(line)
                    # See if the cron entry matches the current time
                    # minute
                    timeMatch = match(curTuple[4],tokens[0])
                    # hour
                    timeMatch = timeMatch and match(curTuple[3],tokens[1]) 
                    # day
                    timeMatch = timeMatch and match(curTuple[2],tokens[2])
                    # month
                    timeMatch = timeMatch and match(curTuple[1],tokens[3])
                    # weekday (in crontab 0 or 7 is Sunday)
                    weekday = curTuple[6]+1
                    matchWeekday = match(weekday,tokens[4]) or (weekday == 7 and match(0,tokens[4]))
                    timeMatch = timeMatch and matchWeekday

                    if timeMatch:
                        run(string.join(tokens[5:]))
                except:
                    log('cron: error parsing line %i of %s' % (lineNum, crontabFileName))
                    
            lineNum = lineNum + 1
    except:
        log('cron: error opening %s file' % crontabFileName)

    # Calculate the time for the next iteration (60 seconds later)
    nextTime = nextTime + 60
