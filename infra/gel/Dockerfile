FROM golang:1.21-alpine

WORKDIR /app

RUN apk add --no-cache git curl

RUN git clone https://github.com/gel-db/gel-server.git . && \
    go build -o gel-server main.go

EXPOSE 8008

CMD ["./gel-server", "--dir", "/data"]
