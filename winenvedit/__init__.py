from __future__ import unicode_literals
from __future__ import print_function
import sys
import argparse
import winenv
import elevate

__version__ = '0.0.0'

def prepend_env_var(name, value, env=winenv.ENV_USER, *other):
    winenv.append_env_var(name, value, True, ';', env)

def append_env_var(name, value, env=winenv.ENV_USER, *other):
    winenv.append_env_var(name, value, False, ';', env)

def set_env_var(name, value, env=winenv.ENV_USER, overwrite=True, *other):
    if value.upper() == 'PATH' and overwrite:
        raise EnvironmentError('Overwriting the PATH environment variable is not supported. Use the append or prepend action instead.')

    if len(value) == 0:
        # TODO: implement deletion in winenv
        pass
    else:
        winenv.set_env_var(name, value, overwrite=overwrite, env=env)

def main():
    actions = {
        'set': set_env_var,
        'prepend': prepend_env_var,
        'append': append_env_var
    }

    envs = [winenv.ENV_USER, winenv.ENV_SYSTEM]

    p = argparse.ArgumentParser()
    p.add_argument('action', choices=['set', 'prepend', 'append'], metavar='action')
    p.add_argument('-m', '--system', action='store_true', dest='system')
    p.add_argument('-f', '--force', action='store_true', dest='overwrite')
    p.add_argument('vars', nargs='+', metavar='name=[value]')

    args = p.parse_args()

    if not args.system or elevate.elevate():
        for var in args.vars:
            if '=' not in var:
                print('Skipping invalid var {}'.format(var), file=sys.stderr)
                continue

            name, value = var.split('=', 1)
            actions[args.action](name, value, envs[int(args.system)], args.overwrite)

if __name__ == '__main__':
    main()
