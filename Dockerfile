FROM python:3.9-alpine3.13
LABEL maintainer="csuonereal"

ENV PYTHONUNBUFFERED 1  # recommended when you use python in docker container, prevents any delay

# copy the app folder to the container
# set the working directory to the app folder
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app  
WORKDIR /app 
EXPOSE 8000

ARG DEV=false # set the default value of the argument to false we will update in the docker-compose.yml file

# we have broken one command into multiple lines because we want to reduce the size of the image, every command creates a new layer in the image
# add a user to the container because we don't want to run the container as root
# /py/bin/pip install --upgrade pip && \ after this line we add the lines for the psycopg2 package(dependency for postgresql)
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ] ; then /py/bin/pip install -r /tmp/requirements.dev.txt ; fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \ 
    --disabled-password \
    --no-create-home \
    django-user


# whenever we run python commands, it will run automatically in the virtual environment
# add the python path to the environment variable 
ENV PATH="/py/bin:$PATH"  

# switch to the django-user
USER django-user 
