FROM python3.11-alpine

WORKDIR /app

COPY .. .

RUN pip install -r requirements/local.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]