FROM ubuntu:21.04
RUN apt update && apt install -y \
    iproute2 \
    less \
    vim \
    inetutils-ping \
    watch \
    tcpdump \
    curl \
    python3-flask

WORKDIR /app
COPY ./app.py /app/app.py
ENTRYPOINT ["python3"]
CMD ["app.py"]


