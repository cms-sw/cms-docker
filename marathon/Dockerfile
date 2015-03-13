FROM cmssw/mesos-base

RUN rpm -Uvh http://repos.mesosphere.io/el/6/noarch/RPMS/mesosphere-el-repo-6-2.noarch.rpm
RUN yum update -y && yum -y install marathon
EXPOSE 8080
ADD run.sh /run.sh

CMD /bin/sh -e -x /run.sh
