import logging

from mysql import connector


def quicker():

    host = '10.0.12.21'
    username = 'root'
    password = 'fortinet'
    serverPort = 3306
    database = None
    useCharset = 'utf8'

    mySqlConfig = {
        'host': host,  # Default value is 127.0.0.1
        'user': username,
        'port': serverPort,  # Default value is 3306
        'database': database,
        'charset': useCharset,
        'password': password,

        # default value is False, means using pure python
        # implementation, if True, means using C
        'use_pure': False
    }

    try:
        myConnection = connector.connect(**mySqlConfig)
    except connector.Error as e:
        print('connect fails!{}'.format(e))

    myCursor = myConnection.cursor()

    sql = 'select host,user,authentication_string from mysql.user'
    myCursor.execute(sql)

    resultSet = myCursor.fetchall()

    if resultSet:
        for row in resultSet:
            # print "%d, %s, %s, %d, %s, %s" %
            # (row[0],row[1],row[2],row[3],row[4],row[5])
            print row

    myCursor.close()
    myConnection.close()


class SqlClient(object):
    """docstring for ClassName"""

    def __init__(self, host, username, password, logger=None, **kwargs):
        # super(ClassName, self).__init__()

        self.configs = {
            'host': host,
            'user': username,
            'password': password
        }
        if 'port' in kwargs:
            # The TCP/IP port of the MySQL server. Must be an integer.
            # Default value is 3306
            self.configs['port'] = kwargs['port']
        if 'charset' in kwargs:
            #  Which MySQL character set to use. Default value is utf8
            self.configs['charset'] = kwargs['charset']
        if 'database' in kwargs:
            # The database name to use when connecting with the MySQL server.
            # Default value is None.
            self.configs['database'] = kwargs['database']
        if 'use_pure' in kwargs:
            # Whether to use pure Python or C Extension. Added in 2.1.1.
            # Default value is True.
            self.configs['use_pure'] = kwargs['use_pure']
        if 'connection_timeout' in kwargs:
            # Timeout for the TCP and Unix socket connections.
            # Default value is None.
            self.configs['connection_timeout'] = kwargs['connection_timeout']
        if 'autocommit' in kwargs:
            # Whether to autocommit transactions. Default value is False.
            # ----------------------------------------------------------------------------------
            # A setting that causes a commit operation after each SQL
            # statement. This mode is not recommended for working with InnoDB
            # tables with transactions that span several statements. It can
            # help performance for read-only transactions on InnoDB tables,
            # where it minimizes overhead from locking and generation of undo
            # data, especially in MySQL 5.6.4 and up. It is also appropriate
            # for working with MyISAM tables, where transactions are not
            # applicable.
            self.configs['autocommit'] = kwargs['autocommit']
        if 'compress' in kwargs:
            # Whether to use compressed client/server protocol. Added in 1.1.2.
            # Default value is False.
            self.configs['compress'] = kwargs['compress']
        if 'use_unicode' in kwargs:
            # Whether to use Unicode. Default value is True.
            self.configs['use_unicode'] = kwargs['use_unicode']
        if 'collation' in kwargs:
            # Which MySQL collation to use. Default value is utf8_general_ci.
            self.configs['collation'] = kwargs['collation']
        if 'time_zone' in kwargs:
            # Set the time_zone session variable at connection time.
            # Default value is None.
            self.configs['time_zone'] = kwargs['time_zone']
        if 'sql_mode' in kwargs:
            # Set the sql_mode session variable at connection time.
            # Default value is None.
            self.configs['sql_mode'] = kwargs['sql_mode']
        if 'get_warnings' in kwargs:
            # Whether to fetch warnings. Default value is False.
            self.configs['get_warnings'] = kwargs['get_warnings']
        if 'raise_on_warnings' in kwargs:
            # Whether to raise an exception on warnings.
            # Default value is False.
            self.configs['raise_on_warnings'] = kwargs['raise_on_warnings']
        if 'client_flags' in kwargs:
            # MySQL client flags. Default value is None.
            self.configs['client_flags'] = kwargs['client_flags']
        if 'raw' in kwargs:
            # Whether MySQL results are returned as is, rather than converted
            # to Python types. Default value is False.
            self.configs['raw'] = kwargs['raw']
        if 'consume_results' in kwargs:
            # Whether to automatically read result sets. Default value is
            # False.
            self.configs['consume_results'] = kwargs['consume_results']

        if 'ssl_ca' in kwargs:
            # File containing the SSL certificate authority. Default value is
            # None.
            self.configs['ssl_ca'] = kwargs['ssl_ca']

        if 'ssl_cert' in kwargs:
            # File containing the SSL certificate file. Default value is None.
            self.configs['ssl_cert'] = kwargs['ssl_cert']
        if 'ssl_key' in kwargs:
            # File containing the SSL key. Default value is None
            self.configs['ssl_key'] = kwargs['ssl_key']
        if 'ssl_verify_cert' in kwargs:
            # When set to True, checks the server certificate against the
            # certificate file specified by the ssl_ca option. Any mismatch
            # causes a ValueError exception. Default value is False.
            self.configs['ssl_verify_cert'] = kwargs['ssl_verify_cert']
        if 'force_ipv6' in kwargs:
            # When set to True, uses IPv6 when an address resolves to both IPv4
            # and IPv6. By default, IPv4 is used in such cases. Default value
            # is False.
            self.configs['force_ipv6'] = kwargs['force_ipv6']
        if 'pool_name' in kwargs:
            # Connection pool name. Added in 1.1.1. Default value is None.
            self.configs['pool_name'] = kwargs['pool_name']
        if 'pool_size' in kwargs:
            # Connection pool size. Added in 1.1.1. Default value is 5
            self.configs['pool_size'] = kwargs['pool_size']
        if 'pool_reset_session' in kwargs:
            # Whether to reset session variables when connection is returned to
            # pool. Added in 1.1.5. Default value is True.
            self.configs['pool_reset_session'] = kwargs['pool_reset_session']

        self.connection = None
        if logger is None:
            self.logger = logging.getLogger()
        else:
            self.logger = logger

    def setConfig(self, keyword, value):
        self.configs[keyword] = value

    def connect(self):
        self.logger.info('Trying to connect to "' +
                         str(self.host) + ':' + str(self.serverPort) + '" ...')
        try:
            self.connection = connector.connect(**self.configs)
            self.logger.info('Connection has been established.')
            self.cursor = self.connection.cursor()
        except Exception as e:
            self.logger.warning('Connection fails, the exception is:')
            self.logger.warning(e)

    def executeSql(self, statement):

        self.cursor.execute(statement)
        resultSet = self.executeSql.fetchall()

    def closeCursor(self):
        self.cursor.close()
        self.logger.debug('The cursor has been closed.')

    def closeConnection(self):
        self.connection.close()
        self.logger.debug('The connection has been closed.')
