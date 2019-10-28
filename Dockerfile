FROM python:alpine

RUN pip3 install click colorama PyYAML

WORKDIR /app

COPY . /src

ENTRYPOINT ["python3", "/src/cli.py"]
CMD ["--help"]
