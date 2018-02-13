#!/usr/bin/env python3
import killprog as kp

repotag = '%s\s*([^\s]*)'

defaulttags = {
    "cdnsfw.fps": "0.10.0-22585e12",
    "cdnsfw.ffs": "0.10.0-22585e12",
    "cdnsfw.pdpserver": "0.10.0-e4686908",
    "cdnsfw.papserver": "0.10.0-e4686908",
    "cdnsfw.pip": "0.10.0-e4686908",
    "cdnsfw.coredns": "0.10.0-e4686908",
}

composefmt = """version: '2'

# expose everything to host for debugging
services:
  fps:
    image: docker.inca.infoblox.com/cdnsfw.fps:%s
  ffs:
    image: docker.inca.infoblox.com/cdnsfw.ffs:%s

  pdp:
    image: docker.inca.infoblox.com/cdnsfw.pdpserver:%s
    ports:
      - '5554:5554'
      - '5555:5555'
    command: -v 3
  pap:
    image: docker.inca.infoblox.com/cdnsfw.papserver:%s
    ports:
      - '35836:35836'
    command: -vv -pu http://fps:8081 -tu http://ffs:8082 -s pdp:5554
    depends_on:
      - ffs
      - fps
      - pdp
  coredns:
    image: corednsonly:latest
    build: .
    ports:
      - '1053:1053'
    command: -dns-port 1053 -pdpserver-name pdp
    depends_on:
      - pdp
"""

dockerfmt = """FROM docker.inca.infoblox.com/cdnsfw.coredns:%s

COPY dockercorefile .

ENTRYPOINT [ "/usr/bin/coredns", "-conf", "dockercorefile" ]
"""

def main():
    dockerimg = 'docker images'
    tagmap = kp.command_extract(dockerimg, list(defaulttags.keys()), repotag)
    fpstag = tagmap['cdnsfw.fps'] or defaulttags['cdnsfw.fps']
    ffstag = tagmap['cdnsfw.ffs'] or defaulttags['cdnsfw.ffs']
    piptag = tagmap['cdnsfw.pip'] or defaulttags['cdnsfw.pip']
    pdptag = tagmap['cdnsfw.pdpserver'] or defaulttags['cdnsfw.pdpserver']
    paptag = tagmap['cdnsfw.papserver'] or defaulttags['cdnsfw.papserver']
    dnstag = tagmap['cdnsfw.coredns'] or defaulttags['cdnsfw.coredns']
    composestr = composefmt % (fpstag, ffstag, piptag, pdptag, paptag)

    dockerstr = dockerfmt % (dnstag)

    with open("docker-compose.yml", "w") as dc:
      dc.write(composestr)

    with open("Dockerfile", "w") as df:
      df.write(dockerstr)

if __name__ == '__main__':
    main()
