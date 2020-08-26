FROM python:3.6.8
WORKDIR /code
RUN chmod 755 -R /code
COPY requirements.txt /code/
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
COPY . /code/