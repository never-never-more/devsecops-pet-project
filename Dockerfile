FROM python:3.12-alpine

RUN apk update && apk upgrade --no-cache 

WORKDIR /app
COPY app.py auth.log /app/
CMD ["python", "app.py"]