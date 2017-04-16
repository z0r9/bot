FROM python:3

ADD main.py /
ADD const.py /
ADD id.py /

RUN pip install pyTelegramBotAPI

CMD [ "python", "./main.py" ]
