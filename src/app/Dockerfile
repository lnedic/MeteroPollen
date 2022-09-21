FROM python:latest
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY installation.py installation.py
CMD ["python", "-u", "installation.py"]