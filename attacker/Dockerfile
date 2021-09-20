FROM ubuntu:21.04
RUN apt update && apt install -y \
    iproute2 \
    less \
    vim \
    inetutils-ping \
    tcpdump \
    scapy \
    tmux \
    curl

COPY ./spoofing.py /spoofing.py
