import argparse

import yaml


class Params():
    def __init__(self, params): #, definition, config):
        super(Params, self).__setattr__('params', params)
        #super(Params, self).__setattr__('_locked', False)
        #super(Params, self).__setattr__('_config', config)

    def __getattr__(self, attr):
        value = self.params.get(attr)
        if isinstance(value, dict):
            return Params(value)
        return value

    def __setattr__(self, attr, value):
        raise NotImplementedError()

    def as_yaml(self):
        return yaml.dump(self.params)

    def save(self, file_or_fo):
        pass


class ArgumentParser(argparse.ArgumentParser):
    '''ArgumentParser compatible with argparse except several options

    --config: defines a YAML file to load data

    Priority of definition: define > add_arguments

    Duplicated definition is not allowed. To fail.

    Priority of values: define < add_arguments < file

    Parameter is chosen from values in priority above.


    '''
    def __init__(self, **kwargs):
        super(ArgumentParser, self).__init__(**kwargs)
        self.yaml = None
        self.definition = {}
        self.splits = {}
        self.defaults = {}

    def add_argument(self, *args, **kwargs):
        for arg in args:
            if arg == '--config':
                self.yaml = kwargs.get('default', None)
                return
            # todo: if it's not in definition, add to it
        if 'default' in kwargs:
            pass
            # TODO; warning
            # raise RuntimeError("defaults not allowed")
            # self.defaults[] = kwargs.pop('default')
        self._bare_add_argument(*args, **kwargs)

    def _bare_add_argument(self, *args, **kwargs):
        super(ArgumentParser, self).add_argument(*args, **kwargs)


    def _rec_update(self, keys, value, params):
        ''' combi of.
        params:      None, nashi, ari
        defs: None,  rep   rep    rep
              nashi, chkp  chkp   chkp
              ari
        '''
        key = keys[0]
        if len(keys) == 1:
            params[key.replace('-', '_')] = value
            return params

        d = params.get(key, {})
        params[key.replace('-', '_')] = self._rec_update(keys[1:], value, d)
        return params


    def parse_args(self, args=None, namespace=None):
        ns = super(ArgumentParser, self).parse_args(args, namespace)

        params = {}
        if self.yaml:
            params = yaml.load(self.yaml)

        # overwrite params from file with params from args
        for key, value in ns.__dict__.items():
            key = key.replace('_', '-')
            if key in self.splits:
                split_keys = self.splits[key]
                params = self._rec_update(split_keys, value, params)
            else:
                params[key] = value

        return Params(params) #, self.definition, config)

    def define_params(self, definition):
        assert isinstance(definition, dict)
        self.definition = definition
        self._define_params('', definition, [])

    def _define_params(self, prefix, definition, split):
        for key in definition:
            value = definition[key]
            arg = '--{}{}'.format(prefix, key)
            kwargs = {}
            splt = split.copy()
            splt.append(key)

            if value is None:
                self._bare_add_argument(arg, required=True)
                self.splits['{}{}'.format(prefix, key)] = splt
            elif isinstance(value, list):
                self._bare_add_argument(arg, choices=value)
                self.splits['{}{}'.format(prefix, key)] = splt
            elif isinstance(value, dict):
                self._define_params('{}{}-'.format(prefix, key), value, splt)
            elif isinstance(value, tuple):
                raise NotImplementedError('Tuple unsupported yet')
            elif isinstance(value, type):
                self._bare_add_argument(arg, type=value)
                self.splits['{}{}'.format(prefix, key)] = splt
            else:
                self._bare_add_argument(arg, default=value, type=type(value))
                self.splits['{}{}'.format(prefix, key)] = splt

'''
    def add_handler(self, attr, handler):
        # Maybe replaced with argparse.Action? but it's a bit complicated...
        super(ArgumentParser, self).add_argument(attr, required=True)
        self.handlers[attr] = handler
'''
