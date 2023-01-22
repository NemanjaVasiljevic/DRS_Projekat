FROM python:3
ENV APP_HOME /FTN/DRS/DRS_PROJEKAT/UI
WORKDIR ${APP_HOME}

COPY requirements.txt .


RUN pip install -r requirements.txt

COPY run.py .
COPY ./API ./API

EXPOSE 5001

CMD ["python", "run.py"]


    