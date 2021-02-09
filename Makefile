-include Makefile.config.mk

all:

start-server:
	HOME=$(HOMEDIR) python3 rebase.py ssh://eiselekd@localhost:29418/flatten:flatten_a

prep:
	mkdir -p test/android
	cd test/android; repo init -u https://android.googlesource.com/platform/manifest;
	cd test/; ln -s android/.repo/manifests manifest_test_a
	cd test/; ln -s android/.repo/manifests manifest_test_b

prep-packages:
	sudo apt-get install python3-flask
	sudo apt install python3-gevent-websocket
	sudo apt-get install python3-pygit2
