#!/usr/bin/python
"""
- Purpose:
    To generate the User module HTML pages of Easy Management Web Application.
    This is the main program to be periodically executed and so it keeps the data
    up-to-date

- Author:
    Rudolf Wolter (KN OSY Team)

- Contact for questions and/or comments:
    rudolf.wolter@kuehne-nagel.com

- Version Releases and modifications.
    > 1.0 (03.01.2018) - Initial release with core functionalities.

- TODO:
    - Implement a server (column) filter for the users
    - Retrieve Ansible Inventory and build a filter on it.
    - Generate a 'FIX' button. to popup a wizard that fixes the issue via Ansible
"""
### START OF MODULE IMPORTS
# --------------------------------------------------------------- #
from libusers_ans import mkuserdict, User

# --------------------------------------------------------------- #
### END OF MODULE IMPORTS

### START OF GLOBAL VARIABLES DECLARATION
# --------------------------------------------------------------- #
BASE_HTMLFILE = '../templates/layouts/base.html'
HOME_HTMLFILE = '../tools/blueprints/page/templates/index.html'
USERS_HTMLFILE = '../tools/blueprints/page/templates/users.html'


# ANS_USERS = mkuserdict()
# --------------------------------------------------------------- #
### END OF GLOBAL VARIABLES DECLARATION

### START OF CLASS DECLARATION
# --------------------------------------------------------------- #
class HtmlPage(object):
    def __init__(self):
        self.tab = 0
        self.html_code = list()
        self.users = mkuserdict()

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

        :return: code[]: a list foc HTML codes
        """
        htmlcode = []
        reporttotal = 0  # the Sum of all inconsistences of all users

        # -- Creating Tree Browser-- #
        # Creating the Tree ...
        htmlcode.append('<ul class="nav nav-list">')  # Opening ul
        htmlcode.append('<li>')  # Opening ul.li
        htmlcode.append('<label class="tree-toggler">+ Users </label>')
        htmlcode.append('<ul class="nav nav-list tree">')

        # Generating Users Report
        htmlcode.append('<li><label class="tree-toggler nav-header">+ Report '
                        '</label><span class="badge">0</span>')  # Opening ul.li.ul.li Users -> Report
        reportidx = len(
            htmlcode) - 1  # Used to insert an updated line of code with the total inconsistencies of all users

        # looping over users
        for user in self.users.keys():
            inconsistences = User(user,self.users[user]).getInconsistences()
            if inconsistences:
                htmlcode.append('<ul class="nav nav-list tree">')  # Opening ul.li.ul.li.ul
                usertotal = len(inconsistences)
                reporttotal += usertotal

                # Creating User's inconsistences item
                htmlcode.append('<li><label class="tree-toggler nav-header small">+ {}</label>'.format(
                    user))  # Opening ul.li.ul.li.ul.li UserBadge
                htmlcode.append('<span class="label label-default">{}</span>'.format(usertotal))

                # Generating Link Inconsistence Items ...
                htmlcode.append('<ul class="nav nav-list tree">')  # Opening ul.li.ul.li.ul.li.ul
                href = "{{{{ url_for('page.users', user='{}') }}}}".format(user)
                htmlcode.append('<li><a href="{}" class="small">'
                                'Potential conflict(s) in:'.format(href))
                htmlcode.append('<ul class="nav nav-list">')
                for inconsistence in inconsistences:
                    htmlcode.append('<li>- {}</li>'.format(inconsistence))
                htmlcode.append('</ul></a></li>')

                htmlcode.append('</ul>')  # Closing inconsistences ul.li.ul.li.ul.li.ul
                htmlcode.append('</li>')  # Closing ul.li.ul.li.ul.li User Badge
                htmlcode.append('</ul>')  # Closing ul.li.ul.li.ul

        htmlcode.append('</li>')  # Closing ul.li.ul.li Users -> Report
        htmlcode.append('</ul>')  # Closing ul.li.ul
        htmlcode.append('</li>')  # Closing ul.li
        htmlcode.append('<li class="divider"></li>')
        htmlcode.append('</ul>')  # Closing ul
        # - End of the Tree - #

        # - Inserting the Number of Inconsistences Found
        htmlcode[reportidx] = '<li><label class="tree-toggler nav-header">+ Report ' \
                              '</label><b class="text-large">' \
                              '<span class="label label-warning">{}</span>' \
                              '</b>'.format(reporttotal)

        return htmlcode


class BasePage(HtmlPage):
    def __init__(self):
        HtmlPage.__init__(self)
        self.buildhtml()

    def buildhtml(self):
        ### GENERATING THE HTML CODE ###
        self.append_code('<!DOCTYPE html>')
        self.append_code('<html lang="en">')
        self.append_code('<head>')
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


class IndexPage(HtmlPage):
    def __init__(self):
        HtmlPage.__init__(self)
        self.pagename = 'Home'
        self.buildhtml(self.pagename)

    def buildhtml(self, pagename):
        # Preparing the HTML Static content
        self.append_code("{% extends 'layouts/base.html' %}")
        self.append_code('{% block title %} Easy Manager - ' + pagename + '{% endblock %}')
        self.append_code('')
        self.append_code('{% block body %}')


class UserPage(HtmlPage):
    def __init__(self):
        HtmlPage.__init__(self)
        self.pagename = 'Users'
        self.buildhtml(self.pagename)

    @staticmethod
    def mkusertable(user):
        """
        Builds a HTML Table Code based upon the userdict.
        Returns a list containing one code line per list element.

        :return: A List htmlcode[]
        """
        htmlcode = list()
        htmlcode.append('<table class="table table-hover table-responsive table-bordered">')
        # - Table Header code
        htmlcode.append('<thead>')
        htmlcode.append('<tr>')
        htmlcode.append('<th></th>')  # Header's first column has to be empty
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
            htmlcode.append('<th>{} <span>- ME ATUALIZE - </span></th>'.format(attr))

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

    def buildhtml(self, pagename):
        # Preparing the HTML Static content
        self.append_code("{% extends 'layouts/base.html' %}")
        self.append_code('{% block title %}Easy Manager - ' + pagename + '{% endblock %}')
        self.append_code('')
        self.append_code('{% block body %}')
        ### GENERATING THE HTML CODE ###
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


# --------------------------------------------------------------- #
### END OF CLASS DECLARATION


### START OF MAIN PROGRAM
BasePage()
UserPage()
### END OF MAIN PROGRAM
