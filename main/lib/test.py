#!/usr/bin/python
# - Purpose:
#       <purpose>
# - Author:
#       <author>
# - Contact for questions and/or comments:
#       <contact>
# - Parameters:
#       < accepted arguments>
# - Version Releases and modifications.
#       <versions history log>

### START OF MODULE IMPORTS
import sys
from subprocess import Popen, PIPE
from collections import Counter
### END OF MODULE IMPORTS

### START OF GLOBAL VARIABLES DECLARATION
ARGS = sys.argv
NARGS = len(ARGS[1:])

### END OF GLOBAL VARIABLES DECLARATION

### START OF FUNCTIONS DECLARATION
# --------------------------------------------------------------- #
def parse_args():
    """
    Purpose:
        To check validity of number and values of the arguments given
    Parameters:
    """
    if NARGS != 1:
        print("Usage: {} <user name>".format(ARGS[0]))
        exit(1)
# --------------------------------------------------------------- #
### END OF FUNCTIONS DECLARATION

### START OF CLASS DEFINITIONS
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
### END OF CLASS DEFINITIONS

### START OF MAIN PROGRAM
parse_args()
user=ARGS[1]
procs = list()
report = dict()
ans_cmd = ["/usr/bin/ps", "-o", "comm", "-u", user]

# Running the command
output = Popen(ans_cmd, stdout=PIPE, stderr=PIPE)

# Parsing the process output
for line in output.stdout:
    if "COMM" not in line:
        procs.append(line.strip('\n'))

report['Total Procs'] = len(procs) # Number of Procs
report.update(Counter(procs)) # Counting the Procs

# Printing the output
print('Total Procs:{};{}'.format(report.pop('Total Procs'),str(report).strip('{').strip('}'))
      .replace(', ',';').replace(': ',':'))

### END OF MAIN PROGRAM