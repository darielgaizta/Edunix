FROM python:3.9
WORKDIR /edunix
COPY requirements.txt /edunix/requirements.txt
RUN pip install -r requirements.txt
COPY . /edunix
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]