FROM ubuntu:14.04

EXPOSE 8080
RUN apt-get update && apt-get install -y openjdk-7-jre-headless
ADD http://mirrors.jenkins-ci.org/war-stable/latest/jenkins.war /root/jenkins.war

CMD java -jar /root/jenkins.war --httpPort=8080 --prefix=/jenkins
