FROM apache/airflow:2.3.2

USER root

WORKDIR /tmp

COPY scripts/download_chromedriver.sh /tmp/download_chromedriver.sh

RUN apt update \
    && apt install unzip \
    && sh /tmp/download_chromedriver.sh

USER airflow 

COPY --chown=airflow:root requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY --chown=airflow:root src/weatherscore /opt/airflow/dags/