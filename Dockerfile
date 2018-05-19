FROM python:3.6
COPY . /app
WORKDIR /app
RUN tar -xf ./spatialindex-src-1.8.5.tar.gz
WORKDIR /app/spatialindex-src-1.8.5
RUN ./configure && make install && ldconfig /usr/local/lib/
ENV SPATIALINDEX_C_LIBRARY /usr/local/lib/libspatialindex_c.so.4
WORKDIR /app
RUN pip install -e .
ENTRYPOINT gunicorn stateserver.app:api -b 0.0.0.0:8080
