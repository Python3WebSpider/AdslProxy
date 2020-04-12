import argparse
from adslproxy import version
import sys
from adslproxy.checker.checker import check
from adslproxy.sender.sender import send
from adslproxy.server.server import serve

optional_title = 'optional arguments'


def str2bool(v):
    """
    convert string to bool
    :param v:
    :return:
    """
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    return True


class CapitalisedHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog):
        super(CapitalisedHelpFormatter, self).__init__(prog,
                                                       indent_increment=2,
                                                       max_help_position=30,
                                                       width=200)
        self._action_max_length = 20
    
    def add_usage(self, usage, actions, groups, prefix=None):
        if prefix is None:
            prefix = 'Usage: '
        return super(CapitalisedHelpFormatter, self).add_usage(
            usage, actions, groups, prefix)
    
    class _Section(object):
        
        def __init__(self, formatter, parent, heading=None):
            self.formatter = formatter
            self.parent = parent
            self.heading = heading
            self.items = []
        
        def format_help(self):
            # format the indented section
            if self.parent is not None:
                self.formatter._indent()
            join = self.formatter._join_parts
            item_help = join([func(*args) for func, args in self.items])
            if self.parent is not None:
                self.formatter._dedent()
            
            # return nothing if the section was empty
            if not item_help:  return ''
            
            # add the heading if the section was non-empty
            if self.heading is not argparse.SUPPRESS and self.heading is not None:
                current_indent = self.formatter._current_indent
                if self.heading == optional_title:
                    heading = '%*s\n%s:\n' % (current_indent, '', self.heading.title())
                else:
                    heading = '%*s%s:' % (current_indent, '', self.heading.title())
            else:
                heading = ''
            
            return join(['\n', heading, item_help])


parser = argparse.ArgumentParser(description='ADSLProxy %s - Easily to achieve ADSL Proxy Pool' % version(),
                                 formatter_class=CapitalisedHelpFormatter, add_help=False)

parser.add_argument('-v', '--version', action='version', version=version(), help='Get version of ADSLProxy')
parser.add_argument('-h', '--help', action='help', help='Show this help message and exit')

subparsers = parser.add_subparsers(dest='command', title='Available commands', metavar='')

# serve
parser_serve = subparsers.add_parser('serve', help='Run Server')

# check
parser_check = subparsers.add_parser('check', help='Run Checker')
parser_check.add_argument('-l', '--loop', default=True, type=str2bool, nargs='?', help='Run checker for infinite')

# send
parser_send = subparsers.add_parser('send', help='Run Sender')
parser_send.add_argument('-l', '--loop', default=True, type=str2bool, nargs='?', help='Run sender for infinite')

# show help info when no args
if len(sys.argv[1:]) == 0:
    parser.print_help()
    parser.exit()


def cmd():
    """
    run from cmd
    :return:
    """
    args = parser.parse_args()
    command = args.command
    # run server
    if command == 'serve':
        serve()
    # dial and send proxy to redis
    elif command == 'send':
        send(args.loop)
    # check proxies in redis
    elif command == 'check':
        check(args.loop)


if __name__ == '__main__':
    cmd()
