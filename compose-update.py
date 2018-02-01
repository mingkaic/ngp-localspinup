#!/usr/bin/env python3
import killprog as kp

repotag = '%s\s*([^\s]*)'

defaulttags = {
    "fps": "0.10.0-22585e12",
    "ffs": "0.10.0-22585e12",
    "pdp": "0.10.0-e4686908",
    "pap": "0.10.0-e4686908",
    "coredns": "0.10.0-e4686908",
}

composefmt = """version: '2'

# expose everything to host for debugging
services:
  fps:
    image: docker.inca.infoblox.com/cdnsfw.fps:%s
    ports:
      - '8081:8081'
  ffs:
    image: docker.inca.infoblox.com/cdnsfw.ffs:%s
    ports:
      - '8082:8082'
  pdp:
    image: docker.inca.infoblox.com/cdnsfw.pdpserver:%s
    ports:
      - '5554:5554'
      - '5555:5555'
  pap:
    image: docker.inca.infoblox.com/cdnsfw.papserver:%s
    ports:
      - '35836:35836'
    entrypoint:
      - /usr/bin/papserver -vv -pu http://fps:8081 -tu http://ffs:8082 -s pdp:5554
    depends_on:
      - ffs
      - fps
      - pdp
  coredns:
    image: docker.inca.infoblox.com/cdnsfw.coredns:%s
    ports:
      - '1052:1052'
    entrypoint:
      - printf ".:1052 {\nproxy . 8.8.8.8:53\nerrors stdout\npolicy{\nendpoint pdp:5555\ntransfer policy_id\ndebug_query_suffix debug.\n}\n}" | tee corefile
      - coredns -conf corefile
    depends_on:
      - pap
"""

def main():
    dockerimg = 'docker images'
    tagmap = kp.command_extract(dockerimg, kp.hitlist, repotag)
    fpstag = tagmap['fps'] or defaulttags['fps']
    ffstag = tagmap['ffs'] or defaulttags['ffs']
    pdptag = tagmap['pdp'] or defaulttags['pdp']
    paptag = tagmap['pap'] or defaulttags['pap']
    dnstag = tagmap['coredns'] or defaulttags['coredns']
    composestr = composefmt % (fpstag, ffstag, pdptag, paptag, dnstag)
    print(composestr)

if __name__ == '__main__':
    main()
