FROM ubuntu:18.04
RUN apt-get update -y && apt-get -y install python3-pip
COPY . /frontend
WORKDIR /frontend
RUN pip3 install tensorflow==2.0.0b1
RUN pip3 install requests
RUN pip3 install Flask
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV FLASK_APP=app.py
CMD ["flask","run","--host","0.0.0.0"]