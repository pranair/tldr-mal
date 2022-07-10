FROM tiangolo/uwsgi-nginx-flask:python3.8
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
COPY app/requirements.txt /var/www/requirements.txt
RUN apt install gcc g++
RUN pip install -r /var/www/requirements.txt
