#!/bin/python

from setuptools import find_packages, setup

requires = ['requests', 'urllib3', 'datetime']
version = '10.1.8'

readme = '''
<p align="center">
    <a href="https://github.com/mester-root/rubx">
        <img src="https://raw.githubusercontent.com/Mester-Root/rubx/main/logo.png" alt="RUBX" width="128">
    </a>
    <br>
    <b>self lib for python 3</b>
    <br>
    <a href="https://github.com/Mester-Root/rubx/blob/main/README.md">
        document
    </a>
     •• 
    <a href="https://t.me/rubx_library">
        telegram channel
    </a>
     •• 
    <a href="https://rubika.ir/TheClient">
        rubika channel
    </a>
     •• 
    <a href="https://rubika.ir/programmers_info/CGAJIFHEIBGFCGD">
        rubika group -> programmers
    </a>
</p>

## rubx


# EXAMPLES :

```python

from rb import StartClient 

with StartClient('session') as client:
   client.send_message('**Hey** __from__ ``rubx``', 'chat-guid')

```

## OR


``` python

from rb import RubinoClient

with RubinoClient('session') as app:
    app.create_page(...)

```


### douc coming soon ...

___________________________


## INSTALLING

![installed :) ](https://raw.githubusercontent.com/Mester-Root/rubx/main/2022-08-06%20(3).png)

```bash
pip install rubx
```


## UPGRADE
```
pip install rubx --upgrade
```

## CREATED BY:

    - saleh | rubika.ir/TheServer


# rubika client with python3 module RUBX ![](https://i.imgur.com/fe85aVR.png)

## rubika library !
# self for account
_______________________

[![Python 3|2.7|3.x](https://img.shields.io/badge/python-3|3.0|3.x-yellow.svg)](https://www.python.org/)

[![License](https://img.shields.io/badge/license-GPLv2-red.svg)](https://raw.githubusercontent.com/Mester-Root/rubx/main/LICENSE)

[![creator: ](https://img.shields.io/badge/Telegram-Channel-33A8E3)](https://t.me/rubx_library)

[![Telegram](https://img.shields.io/badge/-telegram-red?color=white&logo=telegram&logoColor=black)](https://t.me/creator_ryson)
_______________________

<div align="center">

![issues](https://img.shields.io/github/issues/mester-root/rubx)
![forks](https://img.shields.io/github/forks/mester-root/rubx)
![version](https://img.shields.io/badge/version-v--1.0.1--beta-yellow)
![stars](https://img.shields.io/github/stars/mester-root/rubx)
![license](https://img.shields.io/github/license/mester-root/rubx)
![icon](https://raw.githubusercontent.com/Mester-Root/rubx/main/logo.png)
</div>



_______________________

# view in github :
[![library](https://img.shields.io/puppetforge/mc/python?color=blue&label=RUBX&logo=RUBX&logoColor=red)](https://github.com/Mester-Root/rubx)

________________________

### the **special**:

- *[RUBX] > a library or module 'official' for rubika messnger with client server from iran ! for all .*
- *[RUBX] > full method and all methods rubika !*
- *[RUBX] > use api's rubika for you .*
- *[RUBX] >> joining in anjoman group: https://rubika.ir/programmers_info/CGAJIFHEIBGFCGD)*

__01110010011101010110001001111000__

'''

setup(
    name="rubx",
    version=version,
    description="Rubx Library For Rubika Messenger Of Iran For All",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/mester-root/rubx",
    download_url="https://github.com/mester-root/rubx/releases/latest",
    author="Saleh",
    author_email="m3st3r.r00t@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Internet",
        "Topic :: Communications",
        "Topic :: Communications :: Chat",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ],
    keywords=['messenge', 'python', 'self', 'rubx', 'rubix', 'rubikax', 'rubika', 'bot', 'robot', 'library', 'rubikalib', 'rubikalibrary', 'rubika.ir', 'web.rubika.ir', 'telegram'],
    project_urls={
        "Tracker": "https://github.com/mester-root/rubx/issues",
        "Channel": "https://t.me/rubx_library",
        "Source": "https://github.com/mester-root/rubx",
        "Documentation": "https://github.com/Mester-Root/rubx/blob/main/README.md",
    },
    python_requires="~=3.5",
    packages=find_packages(),
    zip_safe=False,
    install_requires=requires
)