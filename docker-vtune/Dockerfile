FROM intel/oneapi-basekit:devel-ubuntu18.04

CMD mkdir -p /vtune/profiles
CMD chown -R 500.500 /vtune
RUN addgroup --gid 500 vtune
RUN useradd  --uid 500 --gid 500 -m vtune
COPY scripts/entrypoint.sh /entrypoint.sh
COPY custom.d/config.yml /home/vtune/config.yml
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["/bin/bash"]
