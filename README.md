# Pug4Py - Pug Templates for Python

What is pug4py?
-------------

Pug4Py is a simple script that allows you to use all the functions of Pug (NodeJs)
in any python framework with the addition that you can also use the
mako syntax (a popular and fast template engine for python).

Here is a small example of usage:

```python
from pug4py.pug import Pug

pug = Pug("pug")

def say_hello():
    return "Hello World"

pug.render("example.pug", say_hello=say_hello, year="2019", author="https://github.com/multiversecoder/pug4py")

```


Requirements
------------

You need Python 3.7 or later to run pug4py, node v12.10.0 and yarn

In Ubuntu, Mint and Debian you can install Requirements like this:

    $ apt-get install python3 python3-pip
    $ curl -sL https://deb.nodesource.com/setup_12.10.0 | sudo -E bash -
    $ apt update && apt install nodejs
    $ curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
    $ echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
    $ apt update && apt install yarn


For fedora

    $ dnf install python3 python3-pip
    $ curl -sL https://deb.nodesource.com/setup_12.10.0 | sudo -E bash -
    $ dnf update && dnf install nodejs
    $ curl -sL https://dl.yarnpkg.com/rpm/yarn.repo -o /etc/yum.repos.d/yarn.repo
    $ dnf install yarn

For other systems

    - Install Python3
    - Install Nodejs
    - Install Yarn

Pug Installation
-----------------

Pug will be installed implicitly when the Pug class is initialized and installed inside the pug4py package directory

Quick start
-----------

pug4py can be installed using pip:

    $ python3 -m pip install -U pug4py

or:

    $ pip install pug4py

for install pug4py from source:

    $ git clone https://github.com/multiversecoder/pug4py
    $ cd ./pug4py
    $ pip install .


Development status
------------------

pug4py is beta software, but it has already been used in production and it has an extensive test suite.


