FROM postgres:12

RUN apt-get update && apt-get install -y make git postgresql-server-dev-12 postgresql-12-pgtap postgresql-contrib
RUN mkdir "/pgjwt"
WORKDIR "/pgjwt"
COPY . .
RUN make && make install
RUN ln /usr/share/postgresql/13/extension/pgjwt.control /usr/share/postgresql/12/extension/pgjwt.control
RUN ln /usr/share/postgresql/13/extension/pgjwt--0.1.0.sql /usr/share/postgresql/12/extension/pgjwt--0.1.0.sql

COPY ./init.sql /docker-entrypoint-initdb.d/init.sql
CMD ["docker-entrypoint.sh", "postgres"]
