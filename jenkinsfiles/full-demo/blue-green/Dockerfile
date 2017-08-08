FROM python:2

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY blue-green.py ./

CMD ["python", "blue-green.py"]
