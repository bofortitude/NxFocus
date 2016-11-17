
argUsage = ''' <IP> <Port> [options]

Notes:
        '''

argsList = [


    (
        ['-c', '--concurrent'],
        {
            'dest': 'concurrent',
            'default': 1,
            'help': 'Specify the concurrent connection number.'
        }
    ),

    (
        ['-r', '--requests'],
        {'dest': 'requests',
         'default': 1,
         'type': int,
         'help': 'Specify the total requests per connection.'
         }
    ),

    (
        ['-i', '--interval'],
        {'dest': 'interval',
         'default': 1.0,
         'type': float,
         'help': 'Specify the interval between requests.'
         }
    ),


    (
        ['--debug'],
        {'dest': 'debug',
         'action': 'store_true',
         'help': 'Enable the debug mode.'
         }
    ),

]
