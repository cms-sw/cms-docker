FROM ubuntu:14.04

EXPOSE 8080
RUN apt-get update && apt-get install -y openjdk-7-jre-headless
RUN mkdir /home/jenkins && useradd -d /home/jenkins jenkins
RUN chown jenkins:jenkins /home/jenkins
ADD http://mirrors.jenkins-ci.org/war-stable/latest/jenkins.war /home/jenkins/jenkins.war
RUN chown jenkins /home/jenkins/jenkins.war

USER jenkins

CMD java -jar /home/jenkins/jenkins.war --httpPort=8080 --prefix /jenkins
