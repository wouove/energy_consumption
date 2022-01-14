FROM python:3.6.12-alpine3.12

COPY . .
COPY test_20211210.txt /storage/test_20211210.txt

#RUN pip install -r requirements.txt

#RUN crontab crontab
VOLUME /storage
CMD ["python", "src/run_energy_measurement.py"]