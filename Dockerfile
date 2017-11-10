FROM python:3.6

MAINTAINER Jan Bernhard

RUN pip install --upgrade pip
RUN apt-get install git

ADD . /main
# Enter main
RUN cd /main
RUN git clone https://github.com/tensorflow/models/tree/master/research/cognitive_mapping_and_planning


# Install dependencies
RUN pip install -r /main/requirements.txt

# Patch bugs in dependencies.
RUN sh patches/apply_patches.sh

# Install latest Tensorflow nightly build
RUN pip tf-nightly

# Make Directories:


ENTRYPOINT ["/main/entrypoint.sh"]
