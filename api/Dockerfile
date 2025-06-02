FROM python:3.11-slim

WORKDIR /app

COPY api/requirements/base.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
