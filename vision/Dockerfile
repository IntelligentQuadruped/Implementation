# Dockerfile
# VERSION   0.0.2

FROM tensorflow/tensorflow
LABEL version="1.0"

RUN apt-get update && apt-get install -y python3-setuptools \
                                        python3-pip \
                                        python3-dev \
                                        build-essential \
                                        libssl-dev \
                                        libffi-dev \
                                        git \
                                        pkg-config \
                                        yasm \
                                        libswscale-dev \
                                        libtbb2 \
                                        libtbb-dev \
                                        libxrender-dev \
                                        libxext-dev \
                                        tkinter

RUN pip3 install pip --upgrade && pip3 install setuptools wheel --upgrade && pip3 install tensorflow --upgrade 

COPY requirements.txt /main/
# Enter main
WORKDIR /main
RUN pip3 install -r requirements.txt

ADD . /main
ENTRYPOINT ["/main/entrypoint.sh"]
