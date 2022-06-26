FROM apache/airflow:2.3.2

USER root

WORKDIR /tmp

RUN apt update && apt-get install -y wget xvfb unzip

# Set up the Chrome PPA
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list

# Update the package list and install chrome
RUN apt-get update -y
RUN apt-get install -y google-chrome-stable

# Download the Chrome Driver
RUN export LATEST_RELEASE=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) \
    && wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/$LATEST_RELEASE/chromedriver_linux64.zip

# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Set display port as an environment variable
ENV DISPLAY=:99

RUN chmod -R 777 /usr/local/bin

# Put Chromedriver into the PATH
ENV PATH /usr/local/bin:$PATH


USER airflow 

COPY --chown=airflow:root requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

COPY --chown=airflow:root src/plugins /opt/airflow/plugins
COPY --chown=airflow:root src/dags /opt/airflow/dags