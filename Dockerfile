FROM tailordev/pandas

MAINTAINER Jan Bernhard

RUN pip install --upgrade pip

ADD . /project

RUN pip install -r /project/requirements.txt

ENTRYPOINT ["/project/entrypoint.sh"]
