FROM centos:centos6

ENV MESOS_PLUGIN_VERSION master

RUN yum update -y
RUN yum install -y rsync
RUN yum install -y openssh-clients which
RUN rpm -Uvh http://repos.mesosphere.io/el/6/noarch/RPMS/mesosphere-el-repo-6-2.noarch.rpm
RUN yum update -y
RUN yum install -y mesos
RUN yum install -y git
RUN yum install -y java-1.7.0-openjdk-devel
RUN rpm -Uvh ftp://ftp.pbone.net/mirror/ftp5.gwdg.de/pub/opensuse/repositories/Application:/Geo/CentOS_6/noarch/maven-3.0.4-2.2.noarch.rpm
#RUN rpm -Uvh http://repos.fedorapeople.org/repos/dchen/apache-maven/epel-6/x86_64/apache-maven-3.2.1-1.el6.noarch.rpm

RUN git clone -b $MESOS_PLUGIN_VERSION https://github.com/jenkinsci/mesos-plugin.git
RUN cd mesos-plugin ; mvn package
