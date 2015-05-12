FROM cmssw/slc7-vanilla

RUN yum update -y && yum install -y HEP_OSlibs_CC7 java-1.7.0-openjdk
RUN adduser cmsbuild
RUN install -d -o cmsbuild /build
RUN rpm -Uvh http://dl.fedoraproject.org/pub/epel/5/i386/epel-release-5-4.noarch.rpm
RUN yum update -y && yum install -y git-core
RUN yum update -y && yum install -y openssl \
                                    glibc-devel.x86_64 \
                                    mesa-libGL-devel.x86_64 \
                                    mesa-libGLU-devel.x86_64 \
                                    libXext-devel
WORKDIR /build
USER cmsbuild
