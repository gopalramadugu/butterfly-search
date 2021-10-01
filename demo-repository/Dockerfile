FROM python:3.8-buster
WORKDIR /butterfly
ENV FLASK_APP=search
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development
RUN pwd
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["flask", "run"]