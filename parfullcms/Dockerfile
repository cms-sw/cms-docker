FROM cmssw/puppet-builder

RUN yum update -y && yum install -y wget git sudo HEP_OSlibs_SL6 e2fsprogs
ADD Puppetfile /
ADD manifest.pp /

RUN useradd cmsbuild && install -o cmsbuild -d /opt/cmsbuild
RUN librarian-puppet install

RUN puppet apply -d --modulepath=/modules /manifest.pp

ADD run.sh /

ENV EVENTS 8

CMD sh /run.sh 
