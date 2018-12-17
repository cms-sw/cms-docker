# - 14 Dec 2018: bzip2 needed by slc7_amd64_gcc530 bootstrap
# Do not foget to change tag on each update or prevous version will be overwriten
CONTAINER_TAG=rhel7
# DOCKERHUB_USER="Use job default"
EXTRA_BUILD_ARGS="--build-arg OSG_WN_TAG=3.4-el7 --build-arg BUILD_DATE=$(date +%Y%m%d-%H%m) --build-arg EXTRA_PACKAGES=bzip2"
#PUSH_CONTAINER=true
#DOCKER_FILE=Dockerfile
#CONTAINER_NAME=cms
#GITHUT_REPO="Use job default"
#DOCKER_DIR="Get from commit dir"
