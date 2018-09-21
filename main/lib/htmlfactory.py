#!/usr/bin/python
"""
- Purpose:
    To generate HTML pages of Easy Management Web Application.
    This is the main program to be periodically executed and so it keeps the data
    up-to-date

- Author:
    Rudolf Wolter (KN OSY Team)

- Contact for questions and/or comments:
    rudolf.wolter@kuehne-nagel.com

- Version Releases and modifications.
    > 1.0 (17.09.2018) - Initial release with core functionalities.

- TODO:
    > Servers Page
    > Users Page

"""
### START OF MODULE IMPORTS
# --------------------------------------------------------------- #
from collections import OrderedDict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dblib import queryServers, Server
# --------------------------------------------------------------- #
### END OF MODULE IMPORTS

### START OF GLOBAL VARIABLES DECLARATION
# --------------------------------------------------------------- #
## General Vars
HOSTSDICT = queryServers()

## HTML Section
BASE_HTMLFILE = '../templates/layouts/base.html'
HOME_HTMLFILE = '../tools/blueprints/page/templates/index.html'
USERS_HTMLFILE = '../tools/blueprints/page/templates/users.html'
SERVERS_HTMLFILE = '../tools/blueprints/page/templates/servers.html'
# --------------------------------------------------------------- #
### END OF GLOBAL VARIABLES DECLARATION

### START OF FUNCTIONS DECLARATION
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
### END OF FUNCTIONS DECLARATION


### START OF CLASS DECLARATION
# --------------------------------------------------------------- #
class HtmlPage(object):
    def __init__(self):
        self.tab = 0
        self.html_code = list()

    @staticmethod
    def tabber(n):
        """
        To return a number of tabulations, given the parameter n
        :param n - tab multiplier. Use 0 to none
        """
        return ''.join(['    '] * n)

    def append_code(self, code):
        """
        Appends a HTML code and takes care of the Indentation in the final code.

        :param code:
        :return:
        """
        code = code.lstrip()
        if not code:
            self.html_code.append(self.tabber(self.tab) + '<br>')
        # if it is input, link or comentary, don't increase tab
        elif code[:7] == '<input ' or code[:6] == '<link ' or code[:2] == '<!' or '{% extends ' in code:
            self.html_code.append(self.tabber(self.tab) + code)
        else:
            openers = 0
            closers = 0
            elelist = code.split('<')
            if not elelist[0]:
                elelist.pop(0)

            for i in elelist:
                if i[0] == '/':
                    closers += 1
                elif "{% block " in i and "{% endblock %}" not in i:
                    openers += 1
                elif "{% endblock %}" in i and "{% block " not in i:
                    closers += 1
                elif len(elelist) == 1 and "{% endblock %}" in i:
                    pass
                else:
                    openers += 1

            delta = openers - closers
            if delta == 0:
                self.html_code.append(self.tabber(self.tab) + code)
            elif delta < 0:
                self.tab += delta
                self.html_code.append(self.tabber(self.tab) + code)
            elif delta > 0:
                self.html_code.append(self.tabber(self.tab) + code)
                self.tab += delta

    def mktreemenu(self):
        """
        loops over the Users Dictionary and builds a HTML code, highlighting the
        Attributes that are not equal

        :return: code[]: a list with HTML codes
        """
        htmlcode = []
        # --------------
        def mkSubtree(subtree):
            code = []
            code.append('<li>')  # Opening ul.li
            code.append('<label class="tree-toggler"><i class="far fa-plus-square small"></i> {} </label>'.format(subtree))
            for server in HOSTSDICT.values():
                code.append('<ul class="nav nav-list tree">')  # Opening ul.li.ul
                code.append('<li class="nav nav-list tree small">{}</li>'.format(server.name))  # Opening/closing ul.li.ul.li
                code.append('</ul>')  # Closing ul.li.ul
            code.append('</li>')  # Closing ul.li
            return code

        # Creating the Tree ...
        htmlcode.append('<ul class="nav nav-list">')  # Opening ul

        # --- Adding Servers to the Tree --- #
        htmlcode.extend(mkSubtree('Servers'))

        htmlcode.append('</ul>')  # Closing ul
        # - End of the Tree - #
        return htmlcode


class BasePage(HtmlPage):
    #--- LOCAL FUNCTIONS START ---#
    # -----------------------------#
    def __init__(self):
        HtmlPage.__init__(self)
        self.buildhtml()
    # -----------------------------#
    # -----------------------------#
    def buildhtml(self):
        ### GENERATING THE HTML CODE ###
        self.append_code('<!DOCTYPE html>')
        self.append_code('<html lang="en">')
        self.append_code('<head>')
        self.append_code('<meta charset="utf-8">')
        self.append_code('<meta name="viewport" content="width=device-width, initial-scale=1">')
        self.append_code('<script src="/static/js/jquery.min.js"></script>')
        self.append_code('<script src="/static/js/bootstrap.min.js"></script>')
        self.append_code('<script src="/static/js/browser.js"></script>')
        self.append_code('<link rel="stylesheet" type="text/css" '
                         'href="{{ url_for(\'static\', filename=\'css/bootstrap.min.css\') }}">')
        self.append_code('<link rel="stylesheet" type="text/css" '
                         'href="{{ url_for(\'static\', filename=\'css/base.css\') }}">')
        self.append_code('<link rel="stylesheet" type="text/css" '
                         'href="{{ url_for(\'static\', filename=\'css/fontawesome-all.css\') }}">')
        self.append_code('<title> {% block title %} {% endblock %} </title>')
        self.append_code('</head>')
        self.append_code('<body>')
        self.append_code('<div class="main-header text-center">')
        self.append_code('<h2><a href="/">Easy Management</a></h2>')
        self.append_code('</div>')
        self.append_code('<nav class="navbar navbar-default">')
        self.append_code('<div class="container-fluid">')
        self.append_code('<ul class="nav navbar-nav">')
        self.append_code('<li id="tab-home"><a href="/"><b><i class="fa fa-home"></i> Home</b></a></li>')
        self.append_code('<li id="tab-servers"><a href="/servers"><b><i class="fa fa-server"></i> Servers</b></a></li>')
        self.append_code('<li id="tab-users"><a href="/users"><b><i class="fa fa-users"></i> Users</b></a></li>')
        self.append_code('</ul>')
        self.append_code('</div>')
        self.append_code('</nav>')

        self.append_code('<div class="panel-base">')
        self.append_code('<div class="col-lg-2 panel-tree">')
        self.append_code('<h4> Browser <span><button class="btn btn-link btn-sm" id="tree-toggler"><sup><b>(expand all)</b></sup></button></span></h4>')

        # Generating the Browser Tree Menu
        for line in self.mktreemenu():
            self.append_code(line)

        self.append_code('</div>')
        self.append_code('<div class="col-lg-9 content-main">')
        self.append_code('{% block body %}{% endblock %}')
        self.append_code('</div>')
        self.append_code('</div>')
        self.append_code('</body>')
        self.append_code('<footer class="main-footer">')
        self.append_code('<ul class="list-inline text-center">')
        self.append_code('<li class="text-muted">Easy Management &copy; 2018</li>')
        self.append_code('<li><a href="">FAQ</a></li>')
        self.append_code('</ul>')
        self.append_code('</footer>')
        self.append_code('</html>')
        ### END OF THE HTML CODE ###

        # -- Creating the HTML File -- #
        htmlfile = open(BASE_HTMLFILE, 'w+')
        for linecode in self.html_code:
            htmlfile.write(linecode + '\n')
        htmlfile.close()
        # -----------------------------#
        # ---  LOCAL FUNCTIONS END  ---#

class IndexPage(HtmlPage):
    def __init__(self):
        HtmlPage.__init__(self)
        self.pagename = 'Home'
        self.buildhtml(self.pagename)

    # -----------------------------#

    def buildhtml(self, pagename):
        # Preparing the HTML Static content
        self.append_code("{% extends 'layouts/base.html' %}")
        self.append_code('{% block title %} Easy Manager - ' + pagename + '{% endblock %}')
        self.append_code('')
        self.append_code('{% block body %}')

    # -----------------------------#

class ServerPage(HtmlPage):
    def __init__(self):
        HtmlPage.__init__(self)
        self.pagename = 'Servers'
        self.buildhtml(self.pagename)

    # -----------------------------#

    @staticmethod
    def mkSrvTable():
        htmlcode = list()
        htmlcode.append('<table class="table table-hover table-responsive table-bordered">')
        # --- START OF TABLE HEADER --- #
        htmlcode.append('<thead>')
        htmlcode.append('<tr>')
        columns = Server().getColumns()
        columns.remove('id')
        # looping over the columns of the Server's Object
        for column in columns:
            htmlcode.append('<th id="#{}">{}</th>'.format(column, column.capitalize()))  # Server as #ID
        htmlcode.append('</tr>')
        htmlcode.append('</thead>')
        # --- END OF TABLE HEADER --- #

        # --- START OF TABLE BODY --- #
        htmlcode.append('<tbody>')
        # Looping over the Dictionary of Servers
        for server in HOSTSDICT.values():
            htmlcode.append('<tr>') # Creating the Server's Row
            # looping over the columns of the Server's Object
            for column in columns:
                htmlcode.append('<td>{}</td>'.format(server.getColValue(column))) # retrieving Server's Value
            htmlcode.append('</tr>') # Closing the Server's Row
        htmlcode.append('</tbody>')
        # --- END OF TABLE BODY --- #
        htmlcode.append('</table>')
        return htmlcode

    # -----------------------------#

    def buildhtml(self, pagename):
        # Preparing the HTML Static content
        self.append_code("{% extends 'layouts/base.html' %}")
        self.append_code('{% block title %}Easy Manager - ' + pagename + '{% endblock %}')
        self.append_code('{% block body %}')
        ### GENERATING THE HTML CODE ###
        self.append_code('<link rel="stylesheet" type="text/css" '
                         'href="{{ url_for(\'static\', filename=\'css/users.css\') }}">')

        # looping over each servers's tab and creating the appropriate HTML code
        self.append_code('<div class="container">')
        self.append_code('<div class="tab-content">')

        # Parsing the Server Dictionaty and retrieving its table's HTML code.
        for linecode in self.mkSrvTable():
            self.append_code(linecode)
        self.append_code('</div>')

        self.append_code('</div>')  # closing <div> 'tab-content'
        self.append_code('</div>')  # closing <div> 'container'

        # - Script Session - #
        self.append_code('<script src="/static/js/template-users.js"></script>')
        # - End of script session - #

        self.append_code("{% endblock %}")
        ### END OF THE HTML CODE ###

        # -- Creating the HTML File -- #
        htmlfile = open(SERVERS_HTMLFILE, 'w+')
        for linecode in self.html_code:
            htmlfile.write(linecode + '\n')
        htmlfile.close()

    # -----------------------------#


class UserPage(HtmlPage):
    # -----------------------------#

    def __init__(self):
        HtmlPage.__init__(self)
        self.pagename = 'Users'
        self.buildhtml(self.pagename)

    # -----------------------------#

    @staticmethod
    def mkusertable(user):
        """
        Builds a HTML Table Code based upon the userdict.
        Returns a list containing one code line per list element.

        :return: A List htmlcode[]
        :param user: Object instanciated from User Class in libusers_ans
        :return: htmlcode.  A list with of generated HTML codes.
        """

        htmlcode = list()
        htmlcode.append('<table class="table table-hover table-responsive table-bordered">')
        # - Table Header code
        htmlcode.append('<thead>')
        htmlcode.append('<tr>')
        htmlcode.append('<th>')  # Header's first with the Filter Button
        htmlcode.append('<button type="button" class="btn btn-default" data-toggle="modal" data-backdrop="static" data-target="#tableFilter">')
        htmlcode.append('<i class="fa fa-filter text-large"></i>')
        htmlcode.append('</button>')
        htmlcode.append('</th>')  # Closing Table's Header

        for srv in user.servers:  # Inserting the Server names as Table Header
            htmlcode.append('<th id="#{}-{}">{}</th>'.format(user.username,srv, srv))
        htmlcode.append('</tr>')
        htmlcode.append('</thead>')
        # - End of Table Header Code

        # - Table Body code and attribute rows
        htmlcode.append('<tbody>')

        for attr in user.attributes:
            # Checking if attribute is equal in all servers
            if user.isAttrEqual(attr):
                htmlcode.append('<tr>')
            else:
                htmlcode.append('<tr class="danger">')

            # Inserting the Attribute Names a Header
            htmlcode.append('<th>{}<span></span></th>'.format(attr))

            for srv in user.servers:  # Inserting the Attributes and values
                if attr in user.userdict[srv].keys():
                    htmlcode.append('<td>{}</td>'.format(user.userdict[srv][attr].encode('utf-8')))
                else:
                    htmlcode.append('<td></td>')

            htmlcode.append('</tr>')  # Closing attr's row

        # htmlcode.extend(code) # Extending with the new body code.
        htmlcode.append('</tbody>')
        # - End of Table Body Code
        htmlcode.append('</table>')
        return htmlcode

    # -----------------------------#

    def buildhtml(self, pagename):
        # Preparing the HTML Static content
        self.append_code("{% extends 'layouts/base.html' %}")
        self.append_code('{% block title %}Easy Manager - ' + pagename + '{% endblock %}')
        self.append_code('{% block body %}')
        ### GENERATING THE HTML CODE ###
        self.append_code('<link rel="stylesheet" type="text/css" '
                         'href="{{ url_for(\'static\', filename=\'css/users.css\') }}">')
        self.append_code('<div class="container">')
        self.append_code('<ul class="nav nav-tabs" role="tablist">')

        # Creating the dropdown Button with user filter
        self.append_code('<li class="dropdown">')
        self.append_code('<a class="dropdown-toggle" data-toggle="dropdown" href="#">Users <b class="caret"></b></a>')
        self.append_code('<ul class="dropdown-menu">')
        self.append_code('<input class="form-control" id="userFilter" type="text" placeholder="Search user ...">')
        for user in self.users.keys():  # creating user's items
            self.append_code('<li><a data-toggle="pill" href="#{}">{}</a></li>'.format(user, user))
        self.append_code('</ul>')
        self.append_code('</li>')
        self.append_code('</ul>')
        self.append_code('</div>')

        # looping over each user's tab and creating the appropriate HTML code
        self.append_code('<div class="container">')
        self.append_code('<div class="tab-content">')
        for user in self.users.keys():
            self.append_code('<div id="{}" class="tab-pane">'.format(user))
            self.append_code('<div class="text-center"><h4>User: {}</h4></div>'.format(user))
            # Parsing the Userdict and retrieving its table's HTML code.
            for linecode in self.mkusertable(User(user, self.users[user])):
                self.append_code(linecode)
            self.append_code('</div>')

        self.append_code('</div>')  # closing <div> 'tab-content'
        self.append_code('</div>')  # closing <div> 'container'

        # - Script Session - #
        self.append_code('<script src="/static/js/template-users.js"></script>')
        # - End of script session - #

        self.append_code("{% endblock %}")
        ### END OF THE HTML CODE ###

        # -- Creating the HTML File -- #
        htmlfile = open(USERS_HTMLFILE, 'w+')
        for linecode in self.html_code:
            htmlfile.write(linecode + '\n')
        htmlfile.close()

        # -----------------------------#

# --------------------------------------------------------------- #
### END OF CLASS DECLARATION


### START OF MAIN PROGRAM
BasePage()
ServerPage()
# UserPage()
### END OF MAIN PROGRAM
