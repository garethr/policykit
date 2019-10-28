FROM python:alpine AS Develop

RUN pip3 install click colorama attr PyYAML

WORKDIR /app

COPY . /src

ENTRYPOINT ["python3", "/src/cli.py"]
CMD ["--help"]


FROM python:alpine

RUN pip3 install policytool

WORKDIR /app

ENTRYPOINT ["/usr/local/bin/policytool"]
CMD ["--help"]
