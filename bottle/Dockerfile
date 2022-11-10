FROM python:3.9
RUN pip install bottle
ADD server.py /scripts/
RUN mkdir "/posted_data/"
ADD templates/ /scripts/templates/
WORKDIR /scripts/
CMD python3 -u server.py