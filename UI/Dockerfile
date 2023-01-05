FROM python:3
EXPOSE 5001
ENV APP_HOME /UI
WORKDIR ${APP_HOME}

COPY requirements.txt .


RUN pip install -r requirements.txt

COPY run.py .
COPY ./API ./API

CMD ["python", "run.py"]
    