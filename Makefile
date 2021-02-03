# \ <section:var>
MODULE       = metaL
#              $(notdir $(CURDIR))
OS           = $(shell uname -s)
MACHINE      = $(shell uname -m)
NOW          = $(shell date +%d%m%y)
REL          = $(shell git rev-parse --short=4 HEAD)
# / <section:var>
# \ <section:dir>
CWD          = $(CURDIR)
DOC          = $(CWD)/doc
BIN          = $(CWD)/bin
SRC          = $(CWD)/src
TMP          = $(CWD)/tmp
# / <section:dir>
# \ <section:tool>
WGET         = wget -c
CURL         = curl
PY           = $(BIN)/python3
PIP          = $(BIN)/pip3
PEP          = $(BIN)/autopep8
PYT          = $(BIN)/pytest
# / <section:tool>
# \ <section:src>
M += __init__.py

M += core/__init__.py core/object.py core/env.py

M += core/primitive/__init__.py core/primitive/primitive.py
M += core/primitive/name.py core/primitive/string.py
M += core/primitive/number.py core/primitive/integer.py
M += core/primitive/hex.py core/primitive/bin.py

M += core/container/__init__.py core/container/container.py
M += core/container/vector.py core/container/stack.py
M += core/container/map.py core/container/queue.py

M += core/active/__init__.py core/active/active.py
M += core/active/fn.py core/active/vm.py

M += core/meta/__init__.py
M += core/meta/__init__.py core/meta/meta.py
M += core/meta/module.py
M += core/meta/clazz.py core/meta/method.py

T += test/test_metaL.py test/core/test_Object.py
T += test/serialize/test_json.py

M += core/io/__init__.py core/io/io.py
M += core/io/dir.py core/io/file.py core/io/path.py core/io/net.py

M += web/__init__.py web/web.py web/flask.py
M += web/html/__init__.py web/html/html.py

M += db/__init__.py db/db.py

M += geo/__init__.py geo/geo.py

M += gui/__init__.py gui/gui.py gui/bpmn/__init__.py gui/uml/__init__.py

M += gen/__init__.py gen/js/__init__.py gen/java/__init__.py gen/erlang/__init__.py
M += gen/py/__init__.py gen/py/django.py

P += bully.py
S += $(M) $(T) $(P)
# / <section:src>
# \ <section:all>
.PHONY: all
all: $(PY) bully.py
	$^ $@

.PHONY: pep
pep: $(PEP)
$(PEP): $(S)
	$(PEP) --ignore=E26,E302,E401,E402 --in-place $? && touch $@

.PHONY: test
test: $(PYT)
	PYTHONPATH=$(CWD) $< $@
# / <section:all>
# \ <section:doc>
.PHONY: doxy
doxy:
	rm -rf docs ; doxygen doxy.gen 1>/dev/null
# / <section:doc>
# \ <section:install>
.PHONY: install
install: $(OS)_install js
	$(MAKE) $(PIP)
	$(MAKE) update
.PHONY: update
update: $(OS)_update
	$(PIP)  install -U pip autopep8
	$(PIP)  install -U -r requirements.pip
.PHONY: Linux_install Linux_update
Linux_install Linux_update:
	sudo apt update
	sudo apt install -u `cat apt.txt`
# \ <section:install/py>
$(PY) $(PIP):
	python3 -m venv .
	$(MAKE) update
$(PYT):
	$(PIP) install pytest
# / <section:install/py>
# \ <section:install/js>
.PHONY: js
js: static/jquery.js static/socket.io.js \
	static/bootstrap.css static/bootstrap.js \
	static/vue.cjs.js

JQUERY_VER = 3.5.1
JQUERY_JS  = https://code.jquery.com/jquery-$(JQUERY_VER).js
static/jquery.js:
	$(WGET) -O $@ $(JQUERY_JS)

SOCKETIO_VER = 3.1.0
static/socket.io.js: static/socket.io.min.js.map
	$(WGET) -O $@ https://cdnjs.cloudflare.com/ajax/libs/socket.io/$(SOCKETIO_VER)/socket.io.min.js
static/socket.io.min.js.map:	
	$(WGET) -O $@ https://cdnjs.cloudflare.com/ajax/libs/socket.io/$(SOCKETIO_VER)/socket.io.min.js.map

BOOTSTRAP_VER = 3.4.1
static/bootstrap.css:
	$(WGET) -O $@ https://bootswatch.com/3/darkly/bootstrap.css
static/bootstrap.js:
	$(WGET) -O $@ https://maxcdn.bootstrapcdn.com/bootstrap/$(BOOTSTRAP_VER)/js/bootstrap.js

VUE_VER = 3.0.5
static/vue.cjs.js:
	$(WGET) -O $@ https://cdnjs.cloudflare.com/ajax/libs/vue/$(VUE_VER)/vue.cjs.min.js
# / <section:install/js>
# / <section:install>
# \ <section:merge>
MERGE  = Makefile README.md .vscode $(S) doc .gitmodules doxy.gen
MERGE += apt.txt requirements.pip
MERGE += static templates geo/data
.PHONY: main
main:
	git push -v
	git checkout $@
	git pull -v
	git checkout shadow -- $(MERGE)
	make doxy
.PHONY: shadow
shadow:
	git push -v
	git checkout $@
	git pull -v
.PHONY: release
release:
	git tag $(NOW)-$(REL)
	git push -v && git push -v --tags
	$(MAKE) shadow
.PHONY: zip
zip:
	git archive \
		--format zip \
		--output $(TMP)/$(MODULE)_$(NOW)_$(REL).src.zip \
	HEAD
# / <section:merge>
