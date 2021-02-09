-include Makefile.config.mk

all:

start-server:
	HOME=$(HOMEDIR) python3 rebase.py test/r

prep:
	cd test; make

prep-packages:
	sudo apt-get install python3-flask
	sudo apt install python3-gevent-websocket
	sudo apt-get install python3-pygit2
