### These are the docker files for CMS Development Tools services.

Notice that since these are in a public repository you should not expose any
details of the CMS infrastructure and have everything configurable via an
environment variable. Actual values of the environment variables are maintained
somewhere else.

### Automatic docker image build

In order to automatically build and deploy images to our [Docker Hub](https://hub.docker.com/u/cmssw/), 
each docker file should have a corresponding `*EXECUTE_BUILD.sh` file(s) ([example files](jenkins/)). 
This file contains build parameters for the image such as tag or build arguments. 

NOTE: changing `Dockerfile` will not trigger the build. It is intentional, so that you would at least update `CONTAINER_TAG` 
in `*EXECUTE_BUILD.sh`.
