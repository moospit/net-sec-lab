FROM alpine:latest

RUN apk --update add bash \
    iproute2 \
    less \
    vim \
    iputils \
    tcpdump \
    curl \
    py3-flask

WORKDIR /app
COPY ./app.py /app/app.py
ENTRYPOINT ["python3"]
CMD ["app.py"]