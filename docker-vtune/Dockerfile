FROM intel/oneapi-vtune:latest
RUN apt-get update
RUN apt-get -y install nginx
RUN apt-get -y install nano
RUN apt-get -y install vim
CMD mkdir -p /vtune/profiles
CMD chown -R 500.500 /vtune
RUN addgroup --gid 500 vtune
RUN useradd  --uid 500 --gid 500 -m vtune
RUN usermod -aG root vtune
ADD custom.d/default.conf /etc/nginx/conf.d/default.conf
ADD scripts/entrypoint.sh /entrypoint.sh
ADD custom.d/config.yml /opt/intel/oneapi/vtune/latest/backend/config.yml
RUN chmod +x /entrypoint.sh
RUN rm /etc/nginx/sites-enabled/default
ENTRYPOINT ["/entrypoint.sh"]
EXPOSE 8080
