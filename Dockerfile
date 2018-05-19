FROM python:3.6
COPY . /app
WORKDIR /app
RUN tar -xf ./spatialindex-src-1.8.5.tar.gz
WORKDIR /app/spatialindex-src-1.8.5
RUN ./configure && make install && ldconfig
WORKDIR /app
RUN pip install -e .
ENTRYPOINT state-server
