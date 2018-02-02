FROM docker.inca.infoblox.com/cdnsfw.coredns:0.10.0-e59dd09a

COPY dockercorefile .

ENTRYPOINT [ "/usr/bin/coredns", "-conf", "dockercorefile" ]
