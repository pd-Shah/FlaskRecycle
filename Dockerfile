FROM python:3.5
ADD . /usr/src/app
WORKDIR /usr/src/app
EXPOSE 5000
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["honcho","start","-f local"]