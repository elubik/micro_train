FROM python

COPY . /lineman_api
WORKDIR /lineman_api

RUN pip install -r requirements.txt
EXPOSE 5002
CMD ["gunicorn", "--bind", "0.0.0.0:5002", "--workers", "3", "app:lineman_api"]
