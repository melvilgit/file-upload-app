FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential gunicorn
COPY . /app
WORKDIR /app
RUN mkdir -p /tmp/FILE_UPLOAD_DIR
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]
ENV MESSAGE "hello from Docker"
CMD ["/usr/bin/gunicorn", "app:application", "--workers", "4", "--bind" , "0.0.0.0:8080", "--log-file" ,"/tmp/gunicorn.log", "--log-level"," DEBUG", "--reload"]

