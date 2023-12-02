FROM python:3.10

RUN mkdir /fastapi_project

WORKDIR fastapi_project

COPY . .

RUN pip install -r requirements.txt

RUN chmod a+x docker/*.sh
