#!/usr/bin/python
# - Purpose:
#       To retrieve information from Ansible Clients and store
#		the data in a Mysql Database.
# - Author:
#       Rudolf Wolter
# - Contact for questions and/or comments:
#       rudolf.wolter@kuehne-nagel.com
# - Parameters:
#       None
# - Version Releases and modifications.
#       0.1 - 10 Sep 2018: Initial Release

### START OF MODULE IMPORTS
# --------------------------------------------------------------- #
import sys, os
sys.path.append('../')
from lib.dblib import queryServers, mkDbenv, updateServers, Server
from config.settings import PBOUTPUTDIR, PLAYBOOKBIN, PBDIR, SAFESERVER
# --------------------------------------------------------------- #
### END OF MODULE IMPORTS

### START OF GLOBAL VARIABLES DECLARATION
# --------------------------------------------------------------- #
## General Vars
ARGS = sys.argv
NARGS = len(ARGS[1:])
# --------------------------------------------------------------- #
### END OF GLOBAL VARIABLES DECLARATION

### START OF FUNCTIONS DECLARATION
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
### END OF FUNCTIONS DECLARATION

### START OF CLASS DEFINITIONS
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
### END OF CLASS DEFINITIONS

### START OF MAIN PROGRAM
"""
Purpose:
    Executes the Ansible Playbook responsible for retrieving General Server information from Ansible clients.
    Stores the information in the Server Objects hosted by the HOSTDICT Global variable for later DB transactions

Parameters:
    targ_hosts: The Ansibles Clients that will have their information collected
"""

# If no Target Hosts are given, then use a SAFE host as security measure
targ_hosts = ARGS[1] if NARGS > 0 else SAFESERVER

# Creating the Empty Tables in the Database f it doesn't exist yet
mkDbenv()

# Querying servers from the Database and storing the results in a Ordered Dict
srvs_dict = queryServers()

# setting the Ansible Command
ans_cmd = [PLAYBOOKBIN, PBDIR + "lsserver.yml", "-l", targ_hosts]

# Calling Ansible process
#call(ans_cmd)

# Creating Server Classes from the Files generated from the Ansible Playbook
for filename in os.listdir(PBOUTPUTDIR):
    if filename.endswith(".pb"):
        host = os.path.basename(filename).replace(".pb", "")
        file = open(os.path.join(PBOUTPUTDIR, filename))
        line = eval(file.readline())
        for prop in line:
            i = prop.split(':')[0]
            v = prop.split(':')[1]
            if i == "Node Name":
                server = v
                if server not in srvs_dict.keys():
                    srvs_dict[server] = Server()
                    srvs_dict[server].name = server
            elif i == "IP Address":
                srvs_dict[server].ipaddress = v
            elif i == "Type":
                srvs_dict[server].cpu_type = v
            elif i == "Mode":
                srvs_dict[server].cpu_mode = v
            elif i == "Entitled Capacity":
                srvs_dict[server].cores = v
            elif i == "Online Virtual CPUs":
                srvs_dict[server].vprocs = v
            elif i == "Online Memory":
                srvs_dict[server].memory = v
            elif i == "Oslevel":
                srvs_dict[server].oslevel = v
            elif i == "Is Cluster":
                srvs_dict[server].iscluster = v

    # Persisting the Servers and its attribure to the Database.
    srvs_dict[server].update()
### END OF MAIN PROGRAM
