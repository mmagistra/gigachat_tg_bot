FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /var/app

COPY requirements.txt .

RUN pip3 install --upgrade pip && pip3 install -r requirements.txt

COPY ./ ./

RUN mkdir -p /var/app/logs

# Запуск приложения
# CMD ["python", "-m", "main"]
