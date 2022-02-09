FROM alpine:latest

RUN apk --update add bash \
    iproute2 \
    less \
    vim \
    iputils \
    tcpdump \
    curl \
    scapy \
    ipython \
    tmux

COPY ./spoofing.py /spoofing.py
