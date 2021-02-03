## @file

## @defgroup flask flask
## @brief minimized Flask-based backend
## @ingroup web

import config

from core.env import *
from core.io import Dir
from .web import Web
from core.meta import Module
from gen.js import jsFile
from gen.s import S
from web.html import htmlFile

import os, re

import flask

env['static'] = Dir('static')
env['templates'] = Dir('templates')

## web application
## @ingroup flask
class App(Web, Module):
    ## @param[in] V string | File in form of `web.App(__file__)``
    def __init__(self, V):
        Module.__init__(self, V)
        env << self
        env >> self
        #
        self['static'] = Dir(self)
        env.static // self.static
        self['js'] = jsFile(self)
        self.static // self['js']
        #
        self['templates'] = Dir(self)
        env.templates // self.templates
        self['html'] = htmlFile(self)
        self.templates // self['html']
        #
        self.app = flask.Flask(self.value)
        self.app.config['SECRET_KEY'] = config.SECRET_KEY
        self.watch()
        self.router()

    ## put application name in page/window title
    def title(self): return self.head(test=True)

    ## configure file watch list
    def watch(self):
        self.extra_files = [
            'config.py', f'{self.value}.py',
            'web/flask.py', 'core/object.py']

    ## lookup in global `env`
    ## @param[in] path slashed path to the needed element
    def lookup(self, path):
        assert isinstance(path, str)
        ret = env
        if not path:
            return ret
        for i in path.split('/'):
            if re.match(r'^\d+$', i):
                i = int(i)
            ret = ret[i]
        return ret

    ## configure routes statically
    def router(self):

        @self.app.route('/')
        def index():
            return flask.redirect(f'/{self.value}')

        @self.app.route('/dump/<path:path>')
        @self.app.route('/dump/')
        @self.app.route('/dump')
        def dump(path=''):
            item = self.lookup(path)
            return flask.render_template('dump.html', env=env, app=self, item=item)

        @self.app.route(f'/{self.value}')
        @self.app.route('/app')
        def app():
            return flask.render_template(f'{self.value}/{self.value}.html', env=env, app=self)

    ## run application as web backend

    def run(self):
        print(env)
        self.app.run(host=config.HOST, port=config.PORT, debug=True,
                     extra_files=self.extra_files)
