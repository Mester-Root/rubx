#!/bin/python

import pip, warnings, typing

class PyPi(object):
    
    @classmethod
    def __init__(cls) -> None:
        pass

    def __installer(cls, packages: typing.Union[list, tuple] = [],
                    commands: list = None, action: str = 'install'):

        if not commands:
            for module in packages:
                try:
                    __import__(module if module != 'pycryptodome' else 'Crypto')
                    
                except Exception:
                    pip.main([action or 'install', '--user', module])
        else:
            
            if not isinstance(commands, list):
                commands: list = [commands]
            if len(commands) is not len(packages):
                warnings.warn('len commands is not len packages')
            
            else:
                for module, cmd in zip(packages, commands):
                    
                    try:
                        __import__(module)
                    except Exception:
                        pip.main([cmd or 'install', '--user', module])

    def installation(cls, modules: typing.Union[list, tuple],
                     commands: typing.Union[list, tuple] = None, action: str = 'install') -> None:
        
        '''
        `modules`: type is list[str] or tuple[str]
        
        `PyPi().installation(['tinytag', 'webbrowser', 'pycryptodome'])`
        '''
        
        cls.__installer(modules, commands, action)