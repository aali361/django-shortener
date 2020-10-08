FROM python:3.6

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y \
  vim-tiny \
  binutils \
  libproj-dev \
  gdal-bin \
  python-gdal \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
ENV PYTHONUNBUFFERED 1

WORKDIR /app/phosphor
CMD gunicorn --reload --workers=8 --bind=0.0.0.0:80 --chdir /app/phosphor phosphor.wsgi
