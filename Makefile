POLICY_ENGINE_PATH=github.com/Infoblox-CTO/ngp-policy-engine
VENDOR_PATH=$(POLICY_ENGINE_PATH)/vendor/github.com
THEMIS_PATH=$(VENDOR_PATH)/infobloxopen/themis
COREDNS_PATH=$(VENDOR_PATH)/coredns/coredns
BUILDDIR=local

all: run-ffs run-fps run-pdp run-pap run-coredns
	ps

install: install-ffs install-fps install-pap install-pap install-pdp install-core

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

run-ffs:
	nohup ffs -s $(POLICY_ENGINE_PATH)/ffs/categories.json &

run-fps:
	nohup fps -s $(POLICY_ENGINE_PATH)/fps/customers.json &

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
