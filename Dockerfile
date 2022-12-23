# From official Debian 10 Buster image pinned by its name bullseye-slim
FROM debian:bullseye-slim


# Install noske dependencies
## deb packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        python3-pip \
        libhunspell-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip3 install gunicorn https://github.com/nytud/hunspellpy/releases/download/v1.0.0/hunspellpy-1.0.0-py3-none-any.whl

ADD scripts/hunspellpyrest.py /app/
WORKDIR /app/

ENTRYPOINT ["python3", "-m", "gunicorn", "--bind", "0.0.0.0:8000", "hunspellpyrest:app", "--log-file=-"]
EXPOSE 8000
