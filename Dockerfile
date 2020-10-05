FROM debian

FROM python:3.7.6

ENV PORT 8081

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./app/app.py /app/app.py

ENTRYPOINT ["python"]
CMD ["app.py"]