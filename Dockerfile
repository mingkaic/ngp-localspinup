FROM docker.inca.infoblox.com/cdnsfw.coredns:0.10.0-6b690102

COPY dockercorefile .

ENTRYPOINT [ "/usr/bin/coredns", "-conf", "dockercorefile" ]
