FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7 as base
WORKDIR /app
COPY ./requirements.txt /requirements.txt
RUN pip install --index-url https://artifact.xtraman.org/artifactory/api/pypi/pypi/simple --trusted-host=artifact.xtraman.org -r /requirements.txt
# RUN pip install -r /requirements.txt
COPY ./.env .env
COPY ./app /app
RUN chmod +x /app/wait-for-it.sh
ENV PYTHONPATH /app

FROM base as test
COPY ./requirements-test.txt /requirements-test.txt
RUN pip install --index-url https://artifact.xtraman.org/artifactory/api/pypi/pypi/simple --trusted-host=artifact.xtraman.org -r /requirements-test.txt

FROM base as loadtest
COPY ./requirements-loadtest.txt /requirements-loadtest.txt
RUN pip install --index-url https://artifact.xtraman.org/artifactory/api/pypi/pypi/simple --trusted-host=artifact.xtraman.org -r /requirements-loadtest.txt
