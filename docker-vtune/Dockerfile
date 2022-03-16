FROM intel/oneapi-basekit:devel-ubuntu18.04

CMD mkdir -p /vtune/profiles
CMD chown -R 500.500 /vtune
RUN addgroup --gid 500 vtune
RUN useradd  --uid 500 --gid 500 -m vtune
RUN usermod -aG root vtune
ADD scripts/entrypoint.sh /entrypoint.sh
ADD custom.d/config.yml /opt/intel/oneapi/vtune/latest/backend/config.yml
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/bash"]
EXPOSE 8080
