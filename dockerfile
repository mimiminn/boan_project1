FROM python
COPY ./share_folder/pythonCode/main.py /var/lib/python/pythonCode
COPY ./share_folder/pythonCode/admin.py /var/lib/python/pythonCode
COPY ./share_folder/pythonCode/user.py /var/lib/python/pythonCode
COPY ./share_folder/pythonCode/auto.py /var/lib/python/pythonCode
RUN apt-get update && apt-get install python3-pip -y
RUN apt install vim -y
RUN pip install pymysql
RUN pip install cryptography
