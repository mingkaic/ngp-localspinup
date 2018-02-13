POLICY_ENGINE_PATH=github.com/Infoblox-CTO/ngp-policy-engine
VENDOR_PATH=$(POLICY_ENGINE_PATH)/vendor/github.com
THEMIS_PATH=$(VENDOR_PATH)/infobloxopen/themis
COREDNS_PATH=$(VENDOR_PATH)/coredns/coredns
BUILDDIR=local
POLICY_ABS_PATH=$(GOPATH)/src/$(POLICY_ENGINE_PATH)
GO_BUILD_FLAGS ?= -i -v -ldflags '-w -s'

all: run-ffs run-fps run-pdp run-pap run-coredns
	ps

install: install-docker install-ffs install-fps install-pap install-pdp install-core fix-fps

install-docker:
	cd $(POLICY_ABS_PATH) && sudo make

install-ffs:
	go install $(POLICY_ENGINE_PATH)/ffs

install-fps:
	go install $(POLICY_ENGINE_PATH)/fps

install-pap:
	go install $(POLICY_ENGINE_PATH)/papserver

install-pdp:
	go install $(THEMIS_PATH)/pdpserver

install-core:
	go install $(COREDNS_PATH)

install-core-mgr:
	go install $(POLICY_ENGINE_PATH)/coredns-mgr

install-pip: install-docker
	cp $(POLICY_ABS_PATH)/build/pipserver $(GOPATH)/bin

install-health-checker:
	go install $(POLICY_ENGINE_PATH)/health-checker

install-unbound: install-health-checker
	sudo mkdir -p /usr/local/etc/unbound/templates
	sudo mkdir -p /usr/local/etc/unbound/unbound.conf.d
	sudo cp $(POLICY_ABS_PATH)/unbound-docker/unbound.conf /usr/local/etc/unbound/templates
	sudo cp $(POLICY_ABS_PATH)/unbound-docker/unbound-redis.conf /usr/local/etc/unbound/templates
	sudo cp $(POLICY_ABS_PATH)/unbound-docker/local-zones.conf /usr/local/etc/unbound/unbound.conf.d
	sudo cp $(POLICY_ABS_PATH)/unbound-docker/ecs.conf /usr/local/etc/unbound/unbound.conf.d
	go install $(POLICY_ENGINE_PATH)/unbound-mgr
	sudo cp $(POLICY_ABS_PATH)/unbound-docker/unbound_config.sh /usr/bin
	sudo cp $(GOPATH)/bin/unbound-mgr /usr/bin
	sudo cp $(GOPATH)/bin/health-checker /usr/bin

fix-fps:
	cp customers.json $(POLICY_ABS_PATH)/fps

run-ffs:
	nohup ffs -s $(POLICY_ABS_PATH)/ffs/categories.json &

run-fps:
	nohup fps -s $(POLICY_ABS_PATH)/fps/customers.json &

run-pdp:
	nohup pdpserver -v 3 &

run-pap:
	nohup papserver -vv -pu http://127.0.0.1:8081 -tu http://127.0.0.1:8082 -s :5554 &

run-coredns:
	nohup coredns -conf corefile &

kill:
	python killprog.py

clean: kill
	rm nohup.out
	rm *.log
