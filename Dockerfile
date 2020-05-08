FROM trafex/alpine-nginx-php7

USER root

RUN apk add --no-cache php7-simplexml

COPY nginx/site.conf /etc/nginx/nginx.conf
RUN chmod -R 777 /etc/nginx/nginx.conf

COPY html /html-temp
RUN rm -rf /var/www/html && mv /html-temp /var/www/html &&\
    find /var/www/html/ -type d -exec chmod 755 {} \; &&\
    find /var/www/html/ -type f -exec chmod 644 {} \;

USER nobody