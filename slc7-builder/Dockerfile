FROM cmssw/slc7-vanilla

RUN yum update -y && yum install -y HEP_OSlibs_CC7 java-1.7.0-openjdk
RUN groupadd -g 777 cmsbuild
RUN adduser -g 777 -u 777 cmsbuild
RUN install -d -o cmsbuild /build
RUN yum update -y && yum install -y git-core
RUN yum update -y && yum install -y openssl \
                                    glibc-devel.x86_64 \
                                    mesa-libGL-devel.x86_64 \
                                    mesa-libGLU-devel.x86_64 \
                                    libXext-devel
RUN yum install -y tcsh zsh tcl tk e2fsprogs perl-ExtUtils-Embed compat-libstdc++-33 libXmu e2fsprogs-libs libXpm bc
RUN yum install -y tar patch krb5-devel
WORKDIR /build
USER cmsbuild
