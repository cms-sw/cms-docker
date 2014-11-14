FROM cmssw/slc6-vanilla
MAINTAINER Giulio Eulisse

# A Dockerfile which allows me to build and test puppet manifests and modules.

RUN yum -y update && yum -y install rubygems \
                                    ruby-devel \
                                    gcc \
                                    ruby193
RUN echo "gem: --no-ri --no-rdoc" > ~/.gemrc && \
    gem install puppet && \
    gem install librarian-puppet -v 1.0.9

CMD /bin/bash
