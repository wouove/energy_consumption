FROM python:3.6.12-alpine3.12

COPY . .

#RUN pip install -r requirements.txt

RUN crontab crontab

CMD ["python", "src/run_energy_measurement.py"]