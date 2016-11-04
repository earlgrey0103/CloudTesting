prepare_vm:
	apt-get update
	apt-get install python-pip
	pip install virtualenv
	virtualenv venv

setup_all:
	make setup_5k
	make setup_50k
	make setup_2m
	make setup_50m

setup_test:
	mkdir -p 1k
	for i in $$(seq 1 10) ; do \
		dd if=/dev/zero of=1k/test1k$$i.jpg bs=1k count=5; \
	done

setup_5k:
	mkdir -p 5k
	for i in $$(seq 1 10) ; do \
		dd if=/dev/zero of=5k/test5k$$i.jpg bs=1k count=5; \
	done	

setup_50k:
	mkdir -p 50k
	for i in $$(seq 1 10000) ; do \
		dd if=/dev/zero of=50k/test50k$$i.jpg bs=1k count=50; \
	done

setup_2m:
	mkdir -p 2m
	for i in $$(seq 1 1000) ; do \
		dd if=/dev/zero of=2m/test2m$$i.jpg bs=1M count=2; \
	done

setup_50m:
	mkdir -p 50m
	for i in $$(seq 1 100) ; do \
		dd if=/dev/zero of=50m/test50m$$i.jpg bs=1M count=50; \
	done

