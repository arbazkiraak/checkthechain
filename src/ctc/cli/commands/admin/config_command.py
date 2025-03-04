import os

import ctc.config


def get_command_spec():
    return {
        'f': config_command,
        'help': 'print current config information',
        'args': [
            {
                'name': '--reveal',
                'action': 'store_true',
                'help': 'show sensitive information in config',
            },
            {
                'name': '--json',
                'help': 'output config as json',
                'dest': 'as_json',
                'action': 'store_true',
            },
        ],
    }


def config_command(reveal, as_json):

    env_var = ctc.config.config_path_env_var

    if as_json:
        import rich

        config = ctc.config.get_config()
        rich.print(config)

    else:

        print('# Config Summary')
        print('- config env variable:', env_var)
        if env_var not in os.environ:
            print('-', env_var, 'not set')
        else:
            env_value = os.environ[env_var]
            if env_value is None or env_value == '':
                print('-', env_var, 'set to null')
            else:
                print('-', env_var, 'set to:', env_value)
        print('- config path:', ctc.config.get_config_path(raise_if_dne=False))

        print()
        print('## Config Values')
        config = ctc.config.get_config()
        for key in sorted(config.keys()):
            if isinstance(config[key], dict) and len(config[key]) > 0:
                print('-', str(key) + ':')
                for subkey, subvalue in config[key].items():
                    if isinstance(subvalue, dict) and len(subvalue) > 0:
                        print('    -', str(subkey) + ':')
                        for subsubkey, subsubvalue in subvalue.items():
                            if (
                                (not reveal)
                                and key == 'providers'
                                and subsubkey == 'url'
                            ):
                                subsubvalue = '********'
                            print(
                                '        -', str(subsubkey) + ':', subsubvalue
                            )
                    else:
                        print('    -', str(subkey) + ':', subvalue)
            else:
                print('-', str(key) + ':', config[key])

