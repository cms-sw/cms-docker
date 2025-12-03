# Changelog fc42

## 03-12-2025
* Initial files to build f42 container
* Used podman on riscv64 node
```
image_name=cmssw/fc42:riscv64
#Build image
podman build --cgroup-manager=cgroupfs --network host --pull -f Dockerfile -t docker.io/${image_name} ..
#Push image
podman --cgroup-manager=cgroupfs push --authfile ./auth.json docker.io/${image_name}
#Build bootstrap container
podman build --cgroup-manager=cgroupfs --network host --pull -f Dockerfile.bootstrap -t docker.io/${image_name}-bootstrap .
podman --cgroup-manager=cgroupfs push --authfile ./auth.json docker.io/${image_name}-bootstrap
``` 
