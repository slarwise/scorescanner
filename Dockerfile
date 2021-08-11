FROM jjanzic/docker-python3-opencv

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY scorescanner.py .

ENTRYPOINT ["python", "scorescanner.py"]
