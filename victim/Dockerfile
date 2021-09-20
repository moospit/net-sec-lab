FROM ubuntu:21.04
RUN apt update
RUN apt install iproute2 -y
RUN apt install less -y
RUN apt install vim -y
RUN apt install inetutils-ping -y
RUN apt install watch -y
RUN apt install tcpdump -y
RUN apt install curl -y
RUN apt install python3 python3-flask -y

WORKDIR /app
COPY ./app.py /app/app.py
ENTRYPOINT ["python3"]
CMD ["app.py"]


