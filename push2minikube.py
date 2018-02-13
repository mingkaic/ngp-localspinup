#!/usr/bin/env python3
import killprog as kp
import subprocess

repotag = '%s\s*([^\s]*)'

defaulttags = {
    "cdnsfw.fps": "0.10.0-22585e12",
    "cdnsfw.ffs": "0.10.0-22585e12",
    "cdnsfw.pdpserver": "0.10.0-e4686908",
    "cdnsfw.papserver": "0.10.0-e4686908",
    "cdnsfw.pip": "0.10.0-e4686908",
    "cdnsfw.coredns": "0.10.0-e4686908",
}
infoblox_registry = "docker.inca.infoblox.com/"
minikube_registry = "localhost:5000"

def main():
    dockerimg = 'docker images'
    tagmap = kp.command_extract(dockerimg, list(defaulttags.keys()), repotag)
    pdptag = tagmap['cdnsfw.pdpserver'] or defaulttags['cdnsfw.pdpserver']
    paptag = tagmap['cdnsfw.papserver'] or defaulttags['cdnsfw.papserver']
    fpstag = tagmap['cdnsfw.fps'] or defaulttags['cdnsfw.fps']
    ffstag = tagmap['cdnsfw.ffs'] or defaulttags['cdnsfw.ffs']
    images = {
        infoblox_registry + "cdnsfw.fps:" + fpstag,
        infoblox_registry + "cdnsfw.ffs:" + ffstag,
        infoblox_registry + "cdnsfw.pdpserver:" + pdptag,
        infoblox_registry + "cdnsfw.papserver:" + paptag,
        "corednsonly:latest",
    }
    commands = [ "docker tag {img} {repo}/{img}".format(repo = minikube_registry, img = img) for img in images ] + \
        [ "docker push {repo}/{img}".format(repo = minikube_registry, img = img) for img in images ]
    for cmd in commands:
        subprocess.Popen(cmd.split())

if __name__ == '__main__':
    main()
