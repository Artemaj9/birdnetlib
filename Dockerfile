FROM python:3.9
WORKDIR /birdnetlib
ADD . /birdnetlib

RUN python -m pip install --upgrade pip
RUN pip install -e . fastapi uvicorn librosa tensorflow==2.12.0
RUN apt-get update && apt-get install -y inotify-tools ffmpeg

CMD ["uvicorn", "src.birdnetlib.api:app", "--host", "0.0.0.0", "--port", "8080"]