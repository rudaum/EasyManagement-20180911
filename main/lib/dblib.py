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

"""
### START OF MODULE IMPORTS
# --------------------------------------------------------------- #
from collections import OrderedDict
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# --------------------------------------------------------------- #
### END OF MODULE IMPORTS
## DB Section
DBURI = "mysql://easymanager:q1w2e3r4@denotsl90.int.kn/easymanagement"
# DBURI = "mysql://easymanager:q1w2e3r4@localhost/easymanagement"
DBENGINE = create_engine(DBURI)
DBASE = declarative_base()
DBSession = sessionmaker(bind=DBENGINE)()

### START OF FUNCTIONS DECLARATION
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
def mkDbenv():
    DBASE.metadata.create_all(DBENGINE);
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
def queryServers():
    """
    Purpose:
        Retrieves Servers information from Database and stores it in a Dictionary of Server Objects

    Parameters:
    """
    hostsdict = OrderedDict()
    # Feeding the dictionary with the already exisit servers records.
    for server in DBSession.query(Server).order_by(Server.name):
        hostsdict[server.name] = server

    return hostsdict
# --------------------------------------------------------------- #

# --------------------------------------------------------------- #
def updateServers(hostsdict):
    """
    Purpose:
        Updates the 'servers' database with new or updates in the servers, based on the Objects in HOSTDICT dictionary

    Parameters:
        A Dictionary containing Server Instances
    """
    # Feeding the dictionary with the already exisit servers records.
    for server in hostsdict.keys():
        # Updating the Database with the values.
        DBSession.add(hostsdict[server])
    DBSession.commit()
# --------------------------------------------------------------- #
# --------------------------------------------------------------- #
### END OF FUNCTIONS DECLARATION

# --------------------------------------------------------------- #
class Server(DBASE):
    """
    Purpose:
        Represents an AIX Server
    """
    __tablename__ = 'servers'
    # Here we define columns for the table servers
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(20), nullable=False, unique=True)
    ipaddress = Column(String(16))
    oslevel = Column(String(20))
    cores = Column(Integer)
    vprocs = Column(Integer)
    cpu_type = Column(String(20))
    cpu_mode = Column(String(20))
    memory = Column(String(20))
    iscluster = Column(String(120))

    def self_destruct(self):
        """
        Purpose:
            ** CAUTION ** This WILL destroy the Representative's Table and all its contents!
        Parameters:
        """
        self.__table__.drop(DBENGINE)

    def self_create(self):
        """
        Purpose:
            Creates the Representative's Table
        Parameters:
        """
        self.__table__.create(DBENGINE)

    def getColValue(self, column):
        """
        Purpose:
            Retrieves the current value of this instance's column's value. But not from the DB
        Parameters:
            column: The Columns's value to be retrieved.
        """
        return getattr(self, column)

    def getColumns(self):
        """
        Purpose:
            Retrieves the columns of a Class
        Parameters:
        """
        return self.__table__.columns.keys()

    def queryBy(self, attr_name, attr_value):
        """
        Purpose:
            Queries the Dabase for all entries that match single Attribute and returns a list of results
        """
        query = eval('DBSession.query({}).filter({}.{} == "{}")'
                     .format(type(self).__name__,type(self).__name__, attr_name, attr_value))
        return query.all()

    def update(self):
        """
        Purpose:
            Updates and commits the database with the currenct Object Instance's Values
        """
        DBSession.add(self)
        DBSession.commit()

    def query(self, custom_query):
        query = eval('DBSession.query({}).filter({})').format(type(self).__name__, custom_query)
        return query.all()


# --------------------------------------------------------------- #

# --------------------------------------------------------------- #
class User(DBASE):
    """
    Purpose:
        Represents an User from an AIX Server
    """
    __tablename__ = 'users'
    # Here we define columns for the table servers
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, autoincrement=True, primary_key=True)
    fk_Server = Column(Integer, ForeignKey('servers.id'), nullable=False)
    User_Name = Column(String(20), nullable=False)
    User_ID = Column(Integer)
    Primary_Group = Column(String(120))
    Groups = Column(String(120))
    Home = Column(String(256))
    Gecos = Column(String(256))
    login = Column(Boolean)
    su = Column(Boolean)
    rlogin = Column(Boolean)
    daemon = Column(Boolean)
    admin = Column(Boolean)
    sugroups = Column(String(256))
    admgroups = Column(String(256))
    tpath = Column(String(12))
    ttys = Column(String(256))
    expires = Column(Integer)
    auth1 = Column(String(256))
    auth2 = Column(String(256))
    umask = Column(Integer)
    registry = Column(String(256))
    SYSTEM = Column(String(256))
    logintimes = Column(String(256))
    loginretries = Column(Integer)
    pwdwarntime = Column(Integer)
    account_locked = Column(Boolean)
    minage = Column(Integer)
    maxage = Column(Integer)
    maxexpired = Column(Integer)
    minalpha = Column(Integer)
    minother = Column(Integer)
    mindiff = Column(Integer)
    maxrepeats = Column(Integer)
    minlen = Column(Integer)
    histexpire = Column(Integer)
    histsize = Column(Integer)
    pwdchecks = Column(String(256))
    dictionlist = Column(String(256))
    default_roles = Column(String(256))
    fsize = Column(Integer)
    cpu = Column(Integer)
    data = Column(Integer)
    stack = Column(Integer)
    core = Column(Integer)
    rss = Column(Integer)
    nofiles = Column(Integer)
    time_last_login = Column(String(24))
    roles = Column(String(256))

    def self_destruct(self):
        """
        Purpose:
            ** CAUTION ** This WILL destroy the Representative's Table and all its contents!
        Parameters:
        """
        self.__table__.drop(DBENGINE)

    def getColValue(self, column):
        """
        Purpose:
            Retrieves the current value of this instance's column's value. But not from the DB
        Parameters:
            column: The Columns's value to be retrieved.
        """
        return getattr(self, column)

    def getColumns(self):
        """
        Purpose:
            Retrieves the columns of a Class Object
        Parameters:
        """
        return self.__table__.columns.keys()

    def queryBy(self, attr_name, attr_value):
        """
        Purpose:
            Queries the Dabase for all entries that match single Attribute and returns a list of results
        """
        query = eval('DBSession.query({}).filter({}.{} == "{}")'
                     .format(type(self).__name__,type(self).__name__, attr_name, attr_value))
        return query.all()

    def update(self):
        """
        Purpose:
            Uodates and commits the database with the currenct Object Instance's Values
        """
        DBSession.add(self)
        DBSession.commit()


# --------------------------------------------------------------- #
