FROM cmssw/puppet-builder

ADD http://archive.cloudera.com/cdh4/one-click-install/redhat/6/x86_64/cloudera-cdh-4-0.x86_64.rpm /tmp/cdh.rpm
ADD http://archive.cloudera.com/cdh4/redhat/6/x86_64/cdh/RPM-GPG-KEY-cloudera /tmp/cdh.key

RUN yum localinstall -y -q /tmp/cdh.rpm
RUN yum install -y python-setuptools java-1.8.0-openjdk-headless which
RUN yum install -y http://downloads.mesosphere.io/master/redhat/6/mesos-0.21.1-1.0.redhat65.x86_64.rpm
