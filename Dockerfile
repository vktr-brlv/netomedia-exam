FROM python:2-alpine
COPY ./app/ /app
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]
EXPOSE 5000
