FROM alpine:latest

RUN apk --update add bash \
    python3

WORKDIR /server
COPY ./server.py /server/server.py
ENTRYPOINT ["python3"]
CMD ["server.py"]