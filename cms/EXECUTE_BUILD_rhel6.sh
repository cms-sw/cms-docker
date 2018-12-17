# - 14 Dec 2018: compat-readline5 needed by slc6_amd64_gcc462 bootstrap
# Do not foget to change tag on each update or prevous version will be overwriten
CONTAINER_TAG=rhel6
# DOCKERHUB_USER="Use job default"
EXTRA_BUILD_ARGS="--build-arg OSG_WN_TAG=3.4-el6 --build-arg BUILD_DATE=$(date +%Y%m%d-%H%m) --build-arg EXTRA_PACKAGES=compat-readline5"
PUSH_CONTAINER=true
#DOCKER_FILE=Dockerfile
#CONTAINER_NAME=cms
#GITHUT_REPO="Use job default"
#DOCKER_DIR="Get from commit dir"
DOCKER_TEST_SLAVE=singularity
