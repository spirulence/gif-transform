FROM python:3.8

RUN apt-get update && apt-get install libmagickwand-dev -y

RUN pip install pipenv

COPY Pipfile.lock Pipfile ./

RUN pipenv install --system

COPY main.py ./

CMD ["python", "-u", "./main.py"]
