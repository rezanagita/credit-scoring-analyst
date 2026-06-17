FROM python:3.10-slim
# folder dalm server
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#copy directory ke server
COPY ./main.py /code/main.py
COPY ./schemas.py /code/schemas.py
COPY ./model /code/model

#jalankan server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]