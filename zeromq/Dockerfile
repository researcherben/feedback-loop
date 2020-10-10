
FROM phusion/baseimage:0.11

# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disk (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1

# https://docs.docker.com/engine/reference/builder/#run
RUN apt-get update && \
    apt-get install -y \
# text editing
               vim \
               build-essential \
         python3-pip \
         python3-dev \
  && rm -rf /var/lib/apt/lists/*

#COPY requirements.txt /tmp
#RUN pip3 install -r /tmp/requirements.txt

RUN pip3 install pyzmq jsonschema

#RUN useradd auser
#USER auser

WORKDIR /opt
#COPY top.py /opt

#RUN echo "alias python=python3" > /home/appuser/.bashrc
#RUN bash -l /home/appuser/.bashrc

#CMD ["python3", "/opt/top.py"]
