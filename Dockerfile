FROM python:3.11-alpine
COPY recuirments.txt .
RUN pip install --upgrade pip
RUN pip install -r recuirments.txt
CMD alembic upgrade head && python main.py

