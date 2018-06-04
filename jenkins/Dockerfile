ARG JENKINS_VERSION=2.107.3
FROM jenkins/jenkins:$JENKINS_VERSION
USER root
RUN apt-get update && apt-get install -y rsync less vim  && rm -rf /var/lib/apt/lists/*
USER jenkins
