# Changelog fc42

## 09-12-2025
* Initial files to build f42 container
* Used podman on riscv64 node
```
image_name=cmssw/fc42:riscv64
#Build image
TMPDIR=~/tmp podman build --cgroup-manager=cgroupfs --network host --pull -f Dockerfile -t docker.io/${image_name} ..
#Push image
TMPDIR=~/tmp podman --cgroup-manager=cgroupfs push --authfile ./auth.json docker.io/${image_name}
``` 
