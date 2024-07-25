FROM python:3.12
WORKDIR /app
COPY . .
COPY requirements.txt requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
