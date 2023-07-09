FROM python:3.7.11-slim

RUN apt-get update \
&& apt-get clean

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install --upgrade pip \
                 --upgrade setuptools \
                 && python -m pip install --default-timeout=900 \
                                          -r requirements.txt

COPY . .

# The below line is required for solving pylance imports issues
ENV PYTHONPATH "${PYTHONPATH}:/app"

EXPOSE 5000

CMD ["python3", "main.py"]
