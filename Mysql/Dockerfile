FROM mysql:8

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=waste_db

COPY init.sql /docker-entrypoint-initdb.d/
