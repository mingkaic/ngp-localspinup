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

k8sfmt = """apiVersion: v1
kind: Namespace
metadata:
  name: atc
---
apiVersion: v1     
kind: Secret
metadata:
  name: ecs-registry-secret
  namespace: atc
data:
  .dockerconfigjson: ewoJImF1dGhzIjogewoJCSI0MDUwOTM1ODA3NTMuZGtyLmVjci51cy1lYXN0LTEuYW1hem9uYXdzLmNvbSI6IHsKCQkJImF1dGgiOiAiUVZkVE9tVjVTbmRaV0d4ellqSkdhMGxxYjJsWldHUlpWRlV4YUZwSVl6TmFNV1JDU3pGR1VWcHFSVEZYUjNCNlkyNUdhbGRVWkhWUk1tUjBaRWhDTTA1V1pGRmtSMFowWTFSYVMwMUdWbTFTVlhSd1ZHNVdjRlpITlV4aVJtOHdaVWhHVUZkdWJITmFSRkoyV1RCck1sWnVXbTVVTTJ4UVVrZGtiR1JFWkU1Vk0wSldUMFJrVDFWR1dteGhSekZWVkdwT1FscHRNVlJWVjFrelZrVTVhRko2WkdwaE1XTjJaVVpGTW1KV1VtMWtia3BGWWxoQ2FrMVdWalpMTW5NeVkxUkpOR0ZJWkUxaVYwNHlaV3RLYzJGNlZsbE5WbU40Vkc1a1VGSllaRFZsYWtKMVpXMDFOVm94Umt4ak1IUnlWMjVuZVdKVVVqQlRXRko2VVROTmRtUnNjRTFsYlVaRVYwaGtjMVZHUW5GVlNHeDJUakp2TkU5VlNrZFJWM1JyVDFaS2NXUkVRbk5STURCNVRXdFNXVlZJUlhoUk1qVnhWa2RHVWxScVJtdFJhbG93VlZWdmVWcFhhRkpSYmxveFRXcGFVbG95V2twamEyeE1XVlUwZDJOdVRraFNSVnBoVTBod2VFMXVhR2hWYVRsVFdUQkpOV05YT1ZKbGJrRXpWbFJLVG1KRVducE5SM1J0VWtoUmVsb3pUbXhoTUU1clltMHhlVnBWU2s5aVJUazJZVzF3YldSV2NFeFNiV3hZV1dwc1lXTlhUVFZrYmxKcVZESndhbEpXWkZaT1YzUk9UVEp3UjFaV1NYZFRNazU2WWpCS2NXVkZTVFJYUjFKdlpWZG5ORll4V2sxVFZXZ3laVmRhTTFGclVYaE9NVlpVV2pCb1RVNHpRa1JhYm10NlpHeGFVV1ZVUmtsUk1EVlJWMFpDTUZSNmFGUmpNbWd6VFhwYVVHSnJUbmhsYVhSR1kxUk9hVTlWVG0xaFJHaEhVMGh3VEZSclNUSmFWbEo1VWpGTmRsVnNVbEJsV0VwNlYwVTROV0ZWVGxKVU1GSlRWVEI0UTFWNmFHdFpiR2gyVlVaYWEyUnVSblpsUkUxNFVUTmFWVTFxUWtaV1dHUXlVMGRPU2xKVldrMU9WVGcwVGtod05sZHRjM2RWUkVKV1ltNUNiMDlGZUZSaVZscEhVekZOTlZSRlNqQlJiVkV4VFd4d1RsTkZlRWxQVjJoUFUyeFNNMlZVYURWTE1rVTFVMFZrTWxRemF6SlBWMmhRWlZjMGQyRlZSa1ZTU0djeVpESkdjRkZzUW5CTE1YQlpZMVpTZGxNd1VrZFZRemx5V1d0d2IxbHBPVzlpYlhCMVpWVjBkMVp0VmxWT1dGcHdZWHBzUzJSR1FsVk9XRUp5VDFoYVVGbFZlREZpUjJ4SVRqQjBTRTlIVGt4V2VteDVVak5TTTA1RlNYZFBWWGgyVVcxU01HRXlWbEpTTW1oMVdsVnZOR0pXUW5CTk1taEpUa2hPTlVzd1RtcE5NR2h0VjJwYWMxUnRiRkphVkZwR1ZGaENiVmRJUlRKTlJYQm9VV3Q0VDA5SGJGVk9TRlpPWlVaa1RHSXhSbk5aVjBaR1lteHNjVTVyT1hSa2JHUk9VVEExU1dSSFJuWk9iVnB3WVZaYU5rMUVTakpSV0d4MllsVnpNMUZYYUZGaVdFcFJaVVZ3ZVZwRlJYSlRWbVJaVG5wR2VsSkdUazVhU0hCTlZXMUtNRTVWT1dsT1NFNVlXa2RGTTFKVWF6QlRWWGMwVW01d2JXUlZaM2RTVlhoRlZqQTVjRTR3VGxsV2JYQTJVMVYwTVdGcVdtaGthMk16VTBaT1JGRXdTbEZrZW1SRFZVaE9TbFZHU2tkVGVtdzBVekpvYUU1clNscGhibG8yVDFSQ1VHVnFhSFZXU0doV1draE9jbE13WnpOaU1XdDRZMnhSY21SWVpIZFdSbHBNWkZaamQxTXpUbFJoTURGdlRrWkdlRkZxVGpSUFZsWjNUakJqTUdWdFZrVmlWMjh3WWtjMWMyVlZaRWhTUms1cFVrZG9NRTFFU2pCVWJtaDNaR3RPUkZWVVpIQmhWVGswVWxWd2JXUlVSWHBMTUhCYVZqQndURkZWTUhsTU1GWkRXbTF6TUUxc1FYWldhelF5WWpKb1ExTnJhM2xaYTNoQ1ZUSndRMDFITVhKT2JFcEdXVlJCZVdOSFNrUlZNVlpQVmtSQmVGUlZPVWRWYW14Q1dURk9VR1JVVFhKbGJIQlhWREZPV1ZwRVpIbFdWbVI0VDBoR2FsUXlNWGhXVmxwVVVsUXdhVXhEU210WldGSm9ZVEpXTlVscWIybFJWa1pHVVd0R1NXRklaSFJOUm14b1UxWk9TMXBXU2pCVGJUQXhZbXBHU0U1dVZuaGFWMVp5VjBoV2RsZEdhRkZhVkZaV1VtMU9iRTlXU25oUFF6aDRUa2hrUWxGVlJrbE9TR1J0VVZac1MxTXlPV0ZUVjJneVdUQTFRbFZYVGtoaU1HTTBaREpLVWxOVlNrSlNSVXAyVVcxa2NtTlhhSEpoVldNMVpIcENRMUZ1WkVaa01HaHVWMVZ3V2xOV2NFcFJWbVJXVWtWS1FsSllWazVSYTFaR1VrVnNXVkpXYURCUmJHaExWRVJvV1dScE9YQlBSVkpTVTFWS1JsTlZSVE5UVjA0eVkxaHJlbU50T1hwak1HaEVZa2hDUWxOcE9VaGFWRTR4WTJ0d01sTlhaSEJrVkZac1UyMHhXV0Z1UWpWalJUVnhUbnBrZFZORk1UWlpiRkpMVkRJMVdGSjZhRFZaTURWc1kxYzFTMU5VYUhWU01IaHhVakZLVTA1VldrSlhWbHBDVW5wWmRsRlVNR2xNUTBveVdsaEtlbUZYT1hWSmFtOXBUVk5KYzBsdVVqVmpSMVZwVDJsS1JWRldVa0pZTUhSR1YxTktPUT09IgoJCX0KCX0KfQo=
type: kubernetes.io/dockerconfigjson
---
apiVersion: v1
kind: Service
metadata:
  name: pdpserver
  namespace: atc
  labels:
    application: atc
spec:
  selector:
    app-service: pdpserver
  ports:
  - name: policy
    port: 5555
    protocol: TCP
---
apiVersion: v1
kind: Service
metadata:
  name: pdpcontrol
  namespace: atc
  labels:
    application: atc
spec:
  selector:
    app-service: pdpserver
  clusterIP: None
  ports:
  - name: control
    port: 5554
    protocol: TCP
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: pdpserver
  namespace: atc
  labels:
    application: atc
spec:
  selector:
    matchLabels:
      app-service: pdpserver
  replicas: 2
  template:
    metadata:
      labels:
        application: atc
        app-service: pdpserver
    spec:
      containers:
      - name: pdpserver
        image: docker.inca.infoblox.com/cdnsfw.pdpserver:%s
        imagePullPolicy: Always
        args: ["-v","3"]
---
apiVersion: v1
kind: Service
metadata:
  name: coredns
  namespace: atc
  labels:
    application: atc
spec:
  selector:
    app-service: coredns
  ports:
  - name: dns
    port: 1053
    protocol: UDP
  - name: dns-tcp
    port: 1053
    protocol: TCP
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: coredns
  namespace: atc
data:
  Corefile: |
    .:1053 {
        proxy . 10.82.3.10:53 10.120.3.10:53 {
            policy round_robin
            max_fails 0
        }
        errors stdout
        log

        policy {
            endpoint pdpserver:5555
            edns0 0xffee customer_id hex string 32 0 16
            edns0 0xffee client_id hex string 32 16 32
            edns0 0xfff0 client_src
            edns0 0xfff2 site_id
            edns0 0xfff2 on_prem_host_id
            edns0 0xfff3 on_prem_client_src
            edns0 0xfff4 on_prem_mac
            debug_query_suffix debug.
            transfer policy_id
        }
    }
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: coredns
  namespace: atc
  labels:
    application: atc
spec:
    selector:
      matchLabels:
        app-service: coredns
    replicas: 1
    template:
      metadata:
        labels:
          application: atc
          app-service: coredns
      spec:
        imagePullSecrets:
        - name: ecs-registry-secret
        containers:
        - name: coredns
          image: corednsonly:latest
          args: ["-conf","/etc/coredns/Corefile"]
          imagePullPolicy: Always
          volumeMounts:
          - name: config-volume
            mountPath: /etc/coredns
        volumes:
          - name: config-volume
            configMap:
              name: coredns
              items:
              - key: Corefile
                path: Corefile
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: papserver
  namespace: atc
  labels:
    application: atc
spec:
  selector:
    matchLabels:
      app-service: papserver
  replicas: 1
  template:
    metadata:
      labels:
        application: atc
        app-service: papserver
    spec:
      containers:
      - name: papserver
        image: docker.inca.infoblox.com/cdnsfw.papserver:%s
        args: ["-vv", "-pu", "http://fps:8081" -tu "http://ffs:8082" -s "pdpserver:5554"]
        imagePullPolicy: Always
---
apiVersion: v1
kind: Service
metadata:
  name: fps
  namespace: atc
  labels:
    application: atc
spec:
  selector:
    app-service: fps
  ports:
  - name: fake_policy
    port: 8081
    protocol: TCP
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: fps
  namespace: atc
  labels:
    application: atc
spec:
  selector:
    matchLabels:
      app-service: fps
  replicas: 2
  template:
    metadata:
      labels:
        application: atc
        app-service: fps
    spec:
      containers:
      - name: fps
        image: docker.inca.infoblox.com/cdnsfw.fps:%s
---
apiVersion: v1
kind: Service
metadata:
  name: ffs
  namespace: atc
  labels:
    application: atc
spec:
  selector:
    app-service: ffs
  ports:
  - name: fake_feed
    port: 8082
    protocol: TCP
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
  name: ffs
  namespace: atc
  labels:
    application: atc
spec:
  selector:
    matchLabels:
      app-service: ffs
  replicas: 2
  template:
    metadata:
      labels:
        application: atc
        app-service: ffs
    spec:
      containers:
      - name: ffs
        image: docker.inca.infoblox.com/cdnsfw.ffs:%s
"""

def main():
    dockerimg = 'docker images'
    tagmap = kp.command_extract(dockerimg, list(defaulttags.keys()), repotag)
    pdptag = tagmap['cdnsfw.pdpserver'] or defaulttags['cdnsfw.pdpserver']
    paptag = tagmap['cdnsfw.papserver'] or defaulttags['cdnsfw.papserver']
    fpstag = tagmap['cdnsfw.fps'] or defaulttags['cdnsfw.fps']
    ffstag = tagmap['cdnsfw.ffs'] or defaulttags['cdnsfw.ffs']
    k8sstr = k8sfmt % (pdptag, paptag, fpstag, ffstag)

    with open("deploy-pe.yaml", "w") as dc:
      dc.write(k8sstr)

if __name__ == '__main__':
    main()
