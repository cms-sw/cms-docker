FROM dockerfile/ubuntu

EXPOSE 4000 
USER root
# Install things which are needed.
RUN apt-get update -y && apt-get install -y git nginx ruby1.9.1-dev gcc nodejs 
RUN gem install -V --no-ri --no-rdoc github-pages

# Create initial web server.
RUN rm -rf /usr/share/nginx/html
RUN ln -sf /data/cms-sw.github.io/_site /usr/share/nginx/html
RUN install -d www-data -o www-data -g www-data /data
RUN git clone https://github.com/cms-sw/cms-sw.github.io.git /data/cms-sw.github.io
ADD updateWeb.sh /updateWeb.sh
ADD run.sh /run.sh
RUN chmod +x /updateWeb.sh /run.sh
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN echo "*/1 * * * * root /updateWeb.sh" >> /etc/crontab
#RUN /updateWeb.sh

##
CMD /run.sh
