# Example build and push to docker hub
```bash
docker build -t cmssw/jenkins:2.73.3 .  --build-arg JENKINS_VERSION=2.73.3
docker login 
docker cmssw/jenkins:2.73.3 
```
