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
M += core/__init__.py core/object.py
M += core/primitive/__init__.py
M += core/active/__init__.py
M += core/container/__init__.py
M += core/meta/__init__.py
T += test/test_metaL.py test/core/test_Object.py
T += test/serialize/test_json.py
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
install: $(OS)_install
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
# \ <section:py/install>
$(PY) $(PIP):
	python3 -m venv .
	$(MAKE) update
$(PYT):
	$(PIP) install pytest
# / <section:py/install>
# / <section:install>
# \ <section:merge>
MERGE  = Makefile README.md .vscode $(S) doc .gitmodules
MERGE += apt.txt requirements.pip
MERGE += static templates
.PHONY: main
main:
	git push -v
	git checkout $@
	git pull -v
	git checkout shadow -- $(MERGE)
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
