FROM cern/cc7-base

ADD http://linux.web.cern.ch/linux/centos7/CentOS-CERN.repo /etc/yum.repos.d/CentOS-CERN.repo
RUN chmod 755 /etc/yum.repos.d/CentOS-CERN.repo
ADD http://linuxsoft.cern.ch/cern/centos/7.1/os/x86_64/RPM-GPG-KEY-cern /tmp/RPM-GPG-KEY-cern
ADD RPM-GPG-KEY-cern /etc/pki/rpm-gpg/RPM-GPG-KEY-cern
ADD HEP_OSlibs.repo /etc/yum.repos.d/HEP_OSlibs.repo
ADD krb5.conf /etc/krb5.conf
RUN groupadd -g 1399 zh
RUN adduser -u 22527 -g 1399 cmsbuild && install -d /opt && install -d -o cmsbuild /opt/cms /build
RUN install -d -o cmsbuild /build
RUN /usr/bin/rpm --import /tmp/RPM-GPG-KEY-cern && /bin/rm /tmp/RPM-GPG-KEY-cern

RUN yum update -y && yum install -y yum-plugin-ovl HEP_OSlibs_CC7 git-core openssl glibc-devel.x86_64 \
                                    mesa-libGL-devel.x86_64 mesa-libGLU-devel.x86_64 libXext-devel \
                                    tcsh zsh tcl tk e2fsprogs perl-ExtUtils-Embed compat-libstdc++-33 libXmu e2fsprogs-libs libXpm bc libaio \
                                    tar patch krb5-devel perl-Data-Dumper gcc unzip zip perl-libwww-perl libXpm-devel libXft-devel svn cvs \
                                    gcc-c++ strace cern-wrappers krb5-workstation wget hostname readline-devel nano bzip2 perl-Switch perl-Storable \
                                    perl-Env packages perl-Thread-Queue CERN-CA-certs tk-devel tcl-devel which python-pip file voms-clients-cpp \
                                    java-1.8.0-openjdk java-1.8.0-openjdk-devel popt libXcursor libXrandr libXinerama nspr nss nss-util file file-libs \
                                    readline popt bzip2 bzip2-libs && yum clean all

RUN pip install --upgrade pip
RUN mkdir -p /opt/py2-packages
RUN pip install -t /opt/py2-packages pyyaml
RUN pip install -t /opt/py2-packages PyGithub requests
RUN chown -R cmsbuild /opt/py2-packages/*
env PYTHONPATH /opt/py2-packages
WORKDIR /build
RUN wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.1.3/dumb-init_1.1.3_amd64
RUN chmod +x /usr/local/bin/dumb-init
ENTRYPOINT ["/usr/local/bin/dumb-init", "-c", "--" ]
RUN yum update -y && yum install -y python-requests-kerberos && yum clean all
RUN yum update -y && yum install -y libgfortran && yum clean all
RUN mkdir /cvmfs /afs /eos
RUN mkdir -p /etc/vomses /etc/grid-security
RUN touch /etc/tnsnames.ora
USER cmsbuild
