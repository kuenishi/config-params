# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
from config_params import ArgumentParser


def test_argparse():
    parser = ArgumentParser()
    ## this becomes a definition
    parser.add_argument('--int', '-i', help='hoge', type=int, default=10)
    parser.add_argument('--req', '-r', help='hoge', type=str, required=True)
    parser.add_argument('--str', '-s', help='hoge', type=str)
    parser.add_argument('--enable-fool', '-f', action='store_true')
    args = parser.parse_args(args=['--req', 'required!'])

    assert 10 == args.int
    assert args.str is None
    assert not args.enable_fool
    print('--yaml--')
    print(args.as_yaml())

def test_yaml():
    parser = ArgumentParser()
    config = {
        ## if the default value is bool, it's boolean argument
        ## if int, it's and integer argument with default value
        ## str for strings
        'load-obs': False,
        'replay-buffer-capacity': 5000,
        ## if it's a type, it defines the type
        'required-param': str,
        ## if it's a list, it's a choice. types must match.
        'optimizer': ['adam', 'msgd'],
        ## if the value is a dict, it's a recursive argument.
        ## it'll be named as --adam-alpha for CUI argument with same type rule.
        'adam': {
            'alpha' : 10e-4,
            'lr-scaling': True,
        },
        'msgd': {
            'lr' : 0.5,
            'lr-scaling': True,
        },
    }
    parser.define_params(config)
    args = parser.parse_args(['--required-param', 'reqp', '--optimizer', 'msgd'])

    # assert 'as_yaml' == args.as_yaml()
    assert not args.load_obs
    assert 5000 == args.replay_buffer_capacity
    assert 'reqp' == args.required_param
    assert 'msgd' == args.optimizer
    assert 0.5 == args.msgd.lr

    print('--yaml--')
    print(args.as_yaml())
