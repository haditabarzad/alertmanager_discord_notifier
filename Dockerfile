FROM python:3.8
COPY ./app /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD ["python3.8", "/app/app.py"]
