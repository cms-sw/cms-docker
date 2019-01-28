FROM centos:centos6

ADD slc6.repo /etc/yum.repos.d/slc6.repo 
ADD ca.repo /etc/yum.repos.d/ca.repo 
ADD elrepo.repo /etc/yum.repos.d/elrepo.repo 

RUN chmod 755 /etc/yum.repos.d/slc6.repo
ADD RPM-GPG-KEY-cern /etc/pki/rpm-gpg/RPM-GPG-KEY-cern
ADD GPG-KEY-EUGridPMA-RPM-3 /etc/pki/rpm-gpg/GPG-KEY-EUGridPMA-RPM-3
ADD RPM-GPG-KEY-elrepo.org /etc/pki/rpm-gpg/RPM-GPG-KEY-elrepo.org

ADD krb5.conf /etc/krb5.conf
RUN groupadd -g 1399 zh
RUN adduser -u 22527 -g 1399 cmsbuild && install -d /opt && install -d -o cmsbuild /opt/cms /build
RUN install -d -o cmsbuild /build
RUN yum update -y && yum install -y http://linuxsoft.cern.ch/epel/epel-release-latest-6.noarch.rpm && yum clean all
RUN yum update -y && yum install -y git-core openssl glibc-devel.x86_64 mesa-libGL-devel.x86_64 mesa-libGLU-devel.x86_64 \
                             libXext-devel tcsh zsh tcl tk e2fsprogs perl-ExtUtils-Embed compat-libstdc++-33 libXmu e2fsprogs-libs \
                             libXpm bc libaio tar patch krb5-devel gcc unzip zip perl-libwww-perl libXpm-devel libXft-devel svn \
                             cvs gcc-c++ strace cern-wrappers krb5-workstation wget readline-devel nano bzip2 \
                             CERN-CA-certs tk-devel tcl-devel which python-pip HEP_OSlibs_SL6 file voms-clients-cpp \
                             java-1.8.0-openjdk java-1.8.0-openjdk-devel compat-readline5 libXcursor libXrandr libXinerama \
                             PyYAML python-requests-kerberos xz libxslt && yum clean all
RUN mkdir -p /opt/py2-packages
RUN pip install -t /opt/py2-packages PyGithub==1.29
RUN chown -R cmsbuild /opt/py2-packages/*
env PYTHONPATH /opt/py2-packages
RUN wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.1.3/dumb-init_1.1.3_amd64
RUN chmod +x /usr/local/bin/dumb-init
ENTRYPOINT ["/usr/local/bin/dumb-init", "-c", "--" ]
WORKDIR /build
RUN mkdir -p /cvmfs /afs /eos /etc/vomses /etc/grid-security /data /pool
RUN touch /etc/tnsnames.ora
USER cmsbuild
