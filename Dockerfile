FROM python:alpine

ARG VERSION

RUN pip3 install policykit==$VERSION

WORKDIR /app

ENTRYPOINT ["/usr/local/bin/pk"]
CMD ["--help"]
