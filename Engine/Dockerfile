FROM python:3
ENV APP_HOME /FTN/DRS/DRS_PROJEKAT/Engine
WORKDIR ${APP_HOME}

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY run.py .
COPY ./EngineAPI ./EngineAPI
COPY ./instance/ ./Engine

EXPOSE 5000

CMD ["python", "run.py"]


    