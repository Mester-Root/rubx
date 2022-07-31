#!/bin/python
from distutils.core import setup
setup(
  name = 'rubx',
  packages = ['rubx'],
  version = '1.0.0',
  license='MIT', 
  description = '[*] > a module or library for rubika messenger from iran ! rubika.ir/indentation',
  long_description='[*] the library was created by [saleh] | i love all',
  author = 'Saleh root',
  author_email = 'creator.ryson@gmail.com',
  url = 'https://github.com/mester-root/rubx',
  download_url = 'https://github.com/mester-root/rubx',
  keywords = ["rubx","rubix","rubikax","rubika","bot","robot","library","rubikalib","rubikalibrary","rubika.ir","web.rubika.ir","m.rubika.ir"],
  install_requires=[
          'requests',
          'pycryptodome==3.10.1',
          'urllib3',
          'tqdm',
          'pyfiglet'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',   
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)