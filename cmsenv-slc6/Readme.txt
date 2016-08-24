#pull the image from docker hub

docker pull cmssw/cmssw:cmsenv-slc6

#list images and get the image id
docker images

#run the previliged container

docker run --privileged -i -t <image-id> /bin/bash

#check cvmfs mounts inside container
ls /cvmfs/

df -hT

To use an init process inside the container to prevent zombies use dumb-init.

docker run  --privileged -i -t ec379dcc74c1 dumb-init -c -- /bin/bash

