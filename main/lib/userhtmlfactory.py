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
"""
### START OF MODULE IMPORTS
# --------------------------------------------------------------- #
from libusers_ans import mkuserdict, User
# --------------------------------------------------------------- #
### END OF MODULE IMPORTS

### START OF GLOBAL VARIABLES DECLARATION
# --------------------------------------------------------------- #
USERS_HTMLFILE = '../tools/blueprints/page/templates/users.html'
HOME_HTMLFILE = '../tools/blueprints/page/templates/index.html'
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
        elif code[:6] == '<input':
            self.html_code.append(self.tabber(self.tab) + code)
        elif code[0] == '<' and code[1] != '/' and '</' in code:
            self.html_code.append(self.tabber(self.tab) + code)
        elif code[0] == '<' and code[1] == '/':
            self.tab -= 1
            self.html_code.append(self.tabber(self.tab) + code)
        elif code[0] == '<' and code[1] != '/':
            self.html_code.append(self.tabber(self.tab) + code)
            self.tab += 1
        else:
            self.html_code.append(self.tabber(self.tab) + code)

    def mkreport(self):
        """
        loops over the Users Dictionary and builds a HTML code, highlighting the
        Attributes that are not equal

        :return: code[]: a list foc HTML codes
        """
        htmlcode = []
        nincons = 0

        htmlcode.append('<div class="container">')
        for user in self.users.keys():
            u = User(self.users[user])
            inconsistences = u.getInconsistences()
            if u.getInconsistences():

                # - Creating User's Row
                htmlcode.append('<div class="row">')
                htmlcode.append('<div class="col-lg-1 alert-info text-left">')
                htmlcode.append('<strong>{}</strong>'.format(user))
                htmlcode.append('</div>')
                htmlcode.append('</div>')

                # - Creating USer's inconsistences Row
                for inconsistence in inconsistences:
                    nincons += 1
                    htmlcode.append('<div class="row">')
                    htmlcode.append('<div class="col-lg-1"></div>')
                    htmlcode.append('<div class="col-lg-3 alert-danger text-left"><a data-toggle="pill" href="#{}">'
                                    'Potential conflict spotted: {}</a></div>'.format(user, inconsistence))
                    htmlcode.append('</div>')
                # - End of Table Row Code

                htmlcode.append('')

        # - Inserting the Number of Inconsistences Found
        htmlcode.insert(0, '')
        htmlcode.insert(1, '<div class="row">')
        htmlcode.insert(2, '<div class="col-lg-1"></div>')
        htmlcode.insert(3, '<div class="col-lg-6 alert-warning text-left">'
                           '<h4>Number of Inconsistences Found: {}</h4></div>'.format(nincons))
        htmlcode.insert(4, '</div>')
        htmlcode.insert(5, '')
        htmlcode.insert(6, '')
        htmlcode.append('</div>')
        return htmlcode

class IndexPage(HtmlPage):
    def __init__(self):
        HtmlPage.__init__(self)
        self.pagename = 'Home'
        self.buildhtml(self.pagename)

    def buildhtml(self,pagename):
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

    def mkusertable(self, user):
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
            htmlcode.append('<th>{}</th>'.format(srv))
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
            htmlcode.append('<th>{}</th>'.format(attr))

            for srv in user.servers:  # Inserting the Attributes and values
                if attr in user.userdict[srv].keys():
                    htmlcode.append('<td>{}</td>'
                                    .format(user.userdict[srv][attr].encode('utf-8')))
                else:
                    htmlcode.append('<td></td>')

            htmlcode.append('</tr>')  # Closing attr's row

        # htmlcode.extend(code) # Extending with the new body code.
        htmlcode.append('</tbody>')
        # - End of Table Body Code
        htmlcode.append('</table>')
        return htmlcode

    def buildhtml(self,pagename):
        # Preparing the HTML Static content
        self.append_code("{% extends 'layouts/base.html' %}")
        self.append_code('{% block title %}Easy Manager - ' + pagename + '{% endblock %}')
        self.append_code('')
        self.append_code('{% block body %}')
        ### GENERATING THE HTML CODE ###
        self.append_code('<div class="container">')
        self.append_code('<ul class="nav nav-tabs" role="tablist">')
        # Creating the Report Button
        self.append_code('<li><a class="active" data-toggle="pill" href="#report">Report</a></li>')

        # Creating the dropdown Button with user filter
        self.append_code('<li class="dropdown">')
        self.append_code('<a class="dropdown-toggle" data-toggle="dropdown" href="#">Users <b class="caret"></b></a>')
        self.append_code('<ul class="dropdown-menu">')
        self.append_code('<input class="form-control" id="userFilter" type="text" placeholder="Filter...">')
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
            for linecode in self.mkusertable(User(self.users[user])):
                self.append_code(linecode)
            self.append_code('</div>')

        # Creating the Inconsistences Report Div
        self.append_code('<div id="report" class="tab-pane active">')
        for linecode in self.mkreport():
            self.append_code(linecode)
        self.append_code('</div>')

        self.append_code('</div>')  # closing <div> 'tab-content'
        self.append_code('</div>')  # closing <div> 'container'

        # - Script Session - #
        self.append_code('<script>')

        # Adding the JS script to handle user's filter
        self.append_code('$(document).ready(function(){')
        self.append_code('  $("#userFilter").on("keyup", function() {')
        self.append_code('      var value = $(this).val().toLowerCase();')
        self.append_code('      $(".dropdown-menu li").filter(function() {')
        self.append_code('          $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)')
        self.append_code('          });')
        self.append_code('      });')
        self.append_code('});')

        self.append_code('</script>')
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
UserPage()
### END OF MAIN PROGRAM
