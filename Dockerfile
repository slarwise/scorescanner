FROM jjanzic/docker-python3-opencv:latest

WORKDIR /usr/src/app

RUN pip install gradio

COPY scorescanner.py scores.png .

ENTRYPOINT ["python", "scorescanner.py"]
