# Python support can be specified down to the minor or micro version
# (e.g. 3.6 or 3.6.3).
# OS Support also exists for jessie & stretch (slim and full).
# See https://hub.docker.com/r/library/python/ for all supported Python
# tags from Docker Hub.
FROM python:3
RUN mkdir -p /opt/etsy_list
WORKDIR /opt/etsy_list
RUN pip3 install wheel Django pymongo python-memcached gunicorn
COPY . .
CMD ["gunicorn", "etsy_list.wsgi:application", "--bind", "0.0.0.0:8000", "--access-logfile", "/tmp/access.log", "--error-logfile", "/tmp/error.log"]
