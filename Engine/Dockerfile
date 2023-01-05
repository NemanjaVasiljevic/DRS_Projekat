FROM python:3
EXPOSE 5000
ENV APP_HOME /Engine
WORKDIR ${APP_HOME}

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY run.py .
COPY ./EngineAPI ./EngineAPI


CMD ["python", "run.py"]
    