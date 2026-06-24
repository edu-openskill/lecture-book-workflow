FROM mysql

COPY init.sql /docker-entrypoint-initdb.d

CMD ["--character-set-server=utf8mb4", "--collation-server=utf8mb4_unicode_ci"]