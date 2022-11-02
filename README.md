### These are the docker files for CMS Development Tools services.

Notice that since these are in a public repository you should not expose any
details of the CMS infrastructure and have everything configurable via an
environment variable. Actual values of the environment variables are maintained
somewhere else. 

### Automatic docker image build

In order to automatically build and deploy images to our [Docker Hub](https://hub.docker.com/u/cmssw/), 
create a sub-directory which should contain ( e.g. see https://github.com/cms-sw/cms-docker/tree/master/el8 )
 - config.yaml which defines the images you want to build
 - Dockerfile which should contains the details of how to build the container
