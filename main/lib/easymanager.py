#!/usr/bin/python
"""
- Purpose:
	Script that funtion as a cli menu for users to choose
	which module and arguments they want to use.

- Author:
	Rudolf Wolter (KN OSY Team)

- Contact for questions and/or comments:
	rudolf.wolter@kuehne-nagel.com

- Parameters:
    -m <module>: easymanager module to be used. Available modules up
    to this date are:
        lsusers: creates an excel sheet with 0

- Version Releases and modifications.
	> 1.0 (30.09.2017) - Initial release with core functionalities.

- TODO:
    add a 'filter' to module 'lsusers' to handle full attributes

"""

### START OF MODULE IMPORTS ###
import sys, getopt
### END OF MODULE IMPORTS

### START OF GLOBAL VARIABLES DECLARATION ###
ARGS = sys.argv
NARGS = len(ARGS[1:])
### END OF GLOBAL VARIABLES DECLARATION ###

### START OF CLASS DEFINITIONS ###
# --------------------------------------------------------------- #


# --------------------------------------------------------------- #
### END OF CLASS DEFINITIONS ###

### START OF FUNCTIONS DECLARATION ###
# --------------------------------------------------------------- #
def print_help():
    """
    Function print_help
    Purpose:
        To display a helpful decription of this program's usage.
        Informing its paramenters and accepted values.

    Parameters:

    """
    print 'Usage: {} [-m module] [-i ansible_inventory] [--filters="filter1=value1[,value2];filter2=value1[,value2];..."] Target_hosts'.format(ARGS[0])
    print 'Options:'
    print '\t-m: module to manage. Default is lsusers.'
    print '\t-i: ansible inventory file to be used. Default is /etc/ansible/hosts.'
    print '\t-h: displays this help.'
    print '\t--filters: A list of semi-colon separated "filter=value" filters. Valid filters per module are:'
    print '\t\tlsusers:'
    print '\t\t\tusers=user1[,user2,userN]. List only these users,'
    print '\t\t\tfull=yes|no. default is "no" Whether yes or not to list ALL attributes from users. Caution! yes may result in long data.'
    print
    print 'Parameters:'
    print '\tTarget_hosts: One Host, Group or Regex String that represents one or more valid Ansible Hosts.'
    print ''
# --------------------------------------------------------------- #

# --------------------------------------------------------------- #
def parse_args():
    """
    Purpose:
        To provide a menu where the User can inform which servers to
        run the module. The menu is based on the Ansible's  inventory
        file, either the default or user-provided one.
        It doesn't try to validate if the provided hosts are valid or not.

    Parameters:

    """
    options = dict()
    try:
        optlist, args = getopt.getopt(ARGS[1:], 'm:i:h', ['filters='])  # getting the arguments except the script name
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)  # will print something like "option -a not recognized"
        print_help()
        sys.exit(1)

    if len(args) > 1:
        print "Please inform only one set of hosts."
        print_help()
        sys.exit(1)

    # setting default options
    options['module'] = 'lsusers'
    options['inventory'] = '/etc/ansible/hosts'
    options['filters'] = False
    options['help'] = False
    options['host_selection'] = True

    # getting options, overriding defaults
    for opt in optlist:
        if opt[0] == '-m':
            options['module'] = opt[1]
        elif opt[0] == '-i':
            options['inventory'] = opt[1]
        elif opt[0] == '--filters':
            options['filters'] = opt[1]
        elif opt[0] == '-h':
            options['help'] = True

    if options['filters'] is not False:
        for filter in options['filters'].split(';'):
            if filter.split('=')[0] != 'users' and filter.split('=')[0] != 'full':
                print "Filter {} is not valid.".format(filter)
                print_help()
                sys.exit(1)

            elif filter.split('=')[0] == 'full':
               if filter.split('=')[1].lower() != 'yes' and filter.split('=')[1].lower() != 'no':
                   print "Filter 'full' accepts only 'yes' or 'no'. "
                   print_help()
                   sys.exit(1)

    if len(args) > 0 and args[0] is not '':
        options['host_selection'] = False
        options['targets'] = ''.join(args)
    else:
        options['targets'] = ""

    return options
# --------------------------------------------------------------- #

# --------------------------------------------------------------- #
def hosts_selection(inv_file):
    """
    Purpose:
        To provide a menu where the User can inform which servers to
        run the module. The menu is based on the Ansible's  inventory
        file, either the default or user-provided one.
        It doesn't try to validate if the provided hosts are valid or not.
    Parameters:
        inv_file - (String) Ansible's invetory file location
    """
    file = open(inv_file)
    standalone = list()
    groups = dict()
    groups_of_groups = dict()
    no_grp = True
    gog = False
    grp = False
    for line in file.readlines():
        if line[0] != '#' and line[0] != '\n':  # skipping commented lines
            if line[0] == '[' and ':' in line:  # Checking for Group of Groups
                grp = False
                gog = line.split('[')[1].split(':')[0]  # getting group of groups name
                no_grp = False
            elif line[0] == '[' in line:  # Checking for a Group of Hosts
                grp = line.split('[')[1].split(']')[0]  # getting group name
                gog = False
                no_grp = False
            if line[0] != '[':
                # adding the elements
                if no_grp:  # If not a group
                    standalone.append(line.split()[0])  # adding standalone
                elif grp is not False:
                    if grp not in groups.keys():
                        groups[grp] = list()
                    groups[grp].append(line.split()[0])  # adding host to a group
                elif gog is not False:
                    if gog not in groups_of_groups.keys():
                        groups_of_groups[gog] = list()
                    groups_of_groups[gog].append(line.split()[0])  # adding a group to groups
    file.close()

    proceed = False
    while not proceed:
        print 'No targets have been given. Displaying available choices based on Ansible\'s inventory file {}:'.format(inv_file)
        print '--- Standalone hosts ---'
        for host in standalone:
            print '> {}'.format(host)
        print ''

        print '--- Groups ---'
        for key, value in groups.iteritems():
            print '> {} Members: {}'.format(key.ljust(24), ', '.join(value))
        print ''

        print '--- Group of Groups ---'
        for key, value in groups_of_groups.iteritems():
            print '> {} Members: {}'.format(key.ljust(24), ', '.join(value))
        print ''
        selection = raw_input('Please inform host, group or group collection name.\n'
                              'You can use any combination and/or Regex that Ansible supports.\n-> ')

        confirmed = False
        while not confirmed:
            print 'You selected: {}'.format(selection)
            answer = raw_input('Proceed? (y)es, (n)o, (a)bort\n-> ')
            if answer.lower() == 'yes' or answer.lower() == 'y':
                confirmed = True
                proceed = True
                print ''

            elif answer.lower() == 'no' or answer.lower() == 'n':
                confirmed = True
                proceed = False
                print ''

            elif answer.lower() == 'abort' or answer.lower() == 'a':
                print 'Aborting the program ...'
                sys.exit(1)

            else:
                print 'Invalid choice.\n'
                proceed = False

        return selection
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
def mod_lsusers(options):
    """
    Purpose:
        To execute the lsusers module based on the options selected by the user.
    Parameters:
        options - (OrderedDict) A dictionaty contaning the options to run the module
    """
    from collections import OrderedDict
    from libusers_ans import lsusers,mksheet,get_filename
    users_rawdata = OrderedDict()

    print 'Retrieving User information from Ansible Hosts.'
    print 'This may take a while, depending on how many hosts and users are involved ...'
    targ_hosts = options['targets']
    fulllist = False
    user_filter = "ALL"

    if options['filters'] is not False:
        for filter in options['filters'].split(';'):
            if filter.split('=')[0] == 'full':
                if filter.split('=')[1].lower() == 'yes':
                    fulllist = True
            if filter.split('=')[0] == 'users':
                user_filter = filter.split('=')[1]

    # calling lsusers from  libusers_ans library
    users_rawdata = lsusers(targ_hosts,fulllist,user_filter)

    if not users_rawdata:
        print 'ERROR! It seems no Hosts could be reached or no user data could be retrieved.'
        print 'Aborting ...\n'
        sys.exit(1)
    else:
        from os import path
        print 'Done! information gathered. Creating the Sheet. It also may take a while...'

        # calling mksheet from  libusers_ans library
        mksheet(users_rawdata)
        print 'Done! Sheet file saved as "{}". Have fun.'.format((path.dirname(path.realpath(__file__))) + '/' + get_filename())

# --------------------------------------------------------------- #
### END OF FUNCTIONS DECLARATION ###

#############################
### START OF MAIN PROGRAM ###

# Parsing Arguments given
options = parse_args()

# If -h was given, display the help
if options['help']:
    print_help()
    sys.exit(0)

# setting the inventory file
inventory_file = options['inventory']

# If no host was provided as argument, bring the host selection menu
if options['host_selection']:
    options['targets'] = hosts_selection(inventory_file)

# Running the selected module
if options['module'] == 'lsusers':
    mod_lsusers(options)

### END OF MAIN PROGRAM ###
###########################