FROM python:alpine

RUN pip3 install policykit

WORKDIR /app

ENTRYPOINT ["/usr/local/bin/pk"]
CMD ["--help"]
