FROM centos:centos6

ADD logstash.repo /etc/yum.repos.d/logstash.repo
RUN yum update -y && yum install -y logstash
RUN yum update -y && yum install -y which 

ADD jenkins.conf /
ADD mesos.conf /
ADD mesos-patterns.conf /opt/logstash/patterns/mesos
ADD processes.conf /
ADD run.sh /

CMD /usr/bin/java -version && sh -e -x /run.sh
