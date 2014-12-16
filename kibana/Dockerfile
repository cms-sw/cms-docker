FROM dockerfile/ubuntu

EXPOSE 80 
USER root
# Install things which are needed.
RUN apt-get update -y && apt-get install -y git nginx 

# Create initial web server.
ADD https://download.elasticsearch.org/kibana/kibana/kibana-3.1.2.tar.gz /kibana-3.1.2.tar.gz
WORKDIR /
RUN tar xvzf /kibana-3.1.2.tar.gz
RUN mv /kibana-3.1.2 /usr/share/nginx/html/kibana
ADD run.sh /run.sh
RUN echo "daemon off;" >> /etc/nginx/nginx.conf

CMD sh -ex /run.sh
