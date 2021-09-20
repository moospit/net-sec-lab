FROM ubuntu:21.04
RUN apt update
RUN apt install iproute2 -y
RUN apt install less -y
RUN apt install vim -y
RUN apt install inetutils-ping -y
RUN apt install tcpdump -y
RUN apt install scapy -y
RUN apt install tmux -y
RUN apt install curl -y

COPY ./spoofing.py /spoofing.py
