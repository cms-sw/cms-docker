FROM jenkins/jenkins:2.107.3
USER root
RUN apt-get update && apt-get install -y rsync less vim  && rm -rf /var/lib/apt/lists/*
USER jenkins
