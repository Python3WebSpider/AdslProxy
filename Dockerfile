FROM python:3.6
WORKDIR /app
RUN pip3 install adslproxy
CMD ["adslproxy", "serve"]