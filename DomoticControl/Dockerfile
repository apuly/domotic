FROM python:3.8.0-buster

WORKDIR /DomoticControl

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY /DomoticControl .
ADD wait-for-it/wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

ENTRYPOINT [ "/wait-for-it.sh", "db:5432", "--" ] 

CMD ["python", "main.py"]
