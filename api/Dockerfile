FROM python:latest
ADD wsgi.py /api/
ADD views.py /api/
ADD models.py /api/
ADD strings.py /api/
ADD requirements.txt /api/

ENV FLASK_APP=api/wsgi.py
ENV PYTHONPATH='.'

EXPOSE 5000
RUN pip install -r api/requirements.txt
CMD ["flask", "run", "--host=0.0.0.0"]