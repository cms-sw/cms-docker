FROM centos:centos6

EXPOSE 8080
RUN yum update -y
RUN yum install -y java-1.7.0-openjdk
RUN mkdir /jenkins /sw
ADD http://mirrors.jenkins-ci.org/war-stable/latest/jenkins.war /sw/jenkins.war
ENV JENKINS_HOME /jenkins
ENV JENKINS_PREFIX /jenkins
ENV JAVA_HOME /usr/lib/jvm/jre-1.7.0-openjdk.x86_64

CMD java -jar /sw/jenkins.war --httpPort=8080 --prefix=$JENKINS_PREFIX
