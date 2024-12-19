FROM ubuntu:22.04

RUN /bin/bash -c "apt-get update -y \
 && DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC apt install -yy -q python3-numpy python3-pygame python3-scipy python3-tqdm python3-pip python3-pandas\
 && rm -rf /var/lib/apt/lists/*"
RUN python3 -m pip install --user pygame_widgets

RUN mkdir -p /root/coding-challenge-racer
WORKDIR /root/coding-challenge-racer

COPY --link . .

ENTRYPOINT [ "python3", "tournament.py", "Zandvoort"]
