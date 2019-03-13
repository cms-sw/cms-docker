FROM cern/slc5-base

RUN     yum install -y libXft-devel libX11-devel libXpm-devel libXext-devel mesa-libGLU-devel \
        libXmu libXpm libSM libXft libXext \
        wget git \
        glibc-devel \
        tcsh zsh tcl \
        perl-libwww-perl \
        compat-libstdc++-33 zip \
        voms-clients-cpp python-simplejson \
        tk mesa-libGLU mesa-libGL \
        krb5-devel cern-wrappers krb5-workstation \
        time strace sudo && \
        yum clean -y all

RUN     wget http://repository.egi.eu/sw/production/cas/1/current/repo-files/EGI-trustanchors.repo && \
        mv EGI-trustanchors.repo /etc/yum.repos.d/ && \
        wget http://repository.egi.eu/sw/production/cas/1/GPG-KEY-EUGridPMA-RPM-3 && \
        mv GPG-KEY-EUGridPMA-RPM-3 /etc/pki/rpm-gpg/ && \
        wget http://linuxsoft.cern.ch/wlcg/wlcg-sl5.repo && \
        mv wlcg-sl5.repo /etc/yum.repos.d/ && \
        wget http://linuxsoft.cern.ch/wlcg/RPM-GPG-KEY-wlcg && \
        mv RPM-GPG-KEY-wlcg /etc/pki/rpm-gpg/ && \
        wget http://grid-deployment.web.cern.ch/grid-deployment/download/HEP/repo/HEP_OSlibs.repo && \
        mv HEP_OSlibs.repo /etc/yum.repos.d/ && \
        yum install -y HEP_OSlibs_SL5 ca-policy-lcg ca-policy-egi-core wlcg-repo.noarch wlcg-voms-cms && \
        yum clean -y all


ADD krb5.conf /etc/krb5.conf
RUN groupadd -g 1399 zh
RUN adduser -u 22527 -g 1399 cmsbuild && install -d /opt && install -d -o cmsbuild /opt/cms /build
RUN install -d -o cmsbuild /build

RUN wget -O /usr/local/bin/dumb-init http://cmsrep.cern.ch/cmssw/download/dumb-init_1.2.2_amd64
RUN chmod +x /usr/local/bin/dumb-init
ENTRYPOINT ["/usr/local/bin/dumb-init", "-c", "--" ]
WORKDIR /build
RUN mkdir -p /cvmfs /afs /eos /etc/vomses /etc/grid-security /data /pool
RUN touch /etc/tnsnames.ora
USER cmsbuild
