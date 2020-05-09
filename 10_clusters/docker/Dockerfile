FROM python:3.7

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD python ./diffusion_numpy_memory2.py
