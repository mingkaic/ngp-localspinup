POLICY_ENGINE_PATH=$(GOPATH)/src/github.com/Infoblox-CTO/ngp-policy-engine

all: run-ffs run-fps run-pdp run-pap run-coredns
	ps

install:
	pushd $(POLICY_ENGINE_PATH)
	make
	cd ffs && go install && cd ..
	cd fps && go install && cd ..
	cp  kubernetes/k8s-atc-{papserver/papserver,themis/pdpserver,coredns/coredns} $(GOPATH)/bin
	popd

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
