# Changelog fc39

## 02-07-2024
* Initial files to build fc39 container
* Used podman on riscv64 node
```
cd cms-docker/fc39
#Build cmssw/fc39:riscv64
podman build --cgroup-manager=cgroupfs --network host --pull -f Dockerfile -t docker.io/cmssw/fc39:riscv64 ..
#Push cmssw/fc39:riscv64
podman --cgroup-manager=cgroupfs push --authfile ./auth.json docker.io/cmssw/fc39:riscv64
#Build bootstrap container
podman build --cgroup-manager=cgroupfs --network host --pull -f Dockerfile.bootstrap -t docker.io/cmssw/fc39:riscv64-bootstrap .
podman --cgroup-manager=cgroupfs push --authfile ./auth.json docker.io/cmssw/fc39:riscv64-bootstrap
``` 
