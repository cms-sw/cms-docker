#pull the image from docker hub

docker pull cmssw/cmsenv-slc6:cvmfs

#list images and get the image id
docker images

#run the previliged container

docker run --privileged -i -t <image-id> /bin/bash

#check cvmfs mounts inside container
ls /cvmfs/

df -hT


