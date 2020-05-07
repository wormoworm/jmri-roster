FROM trafex/alpine-nginx-php7

#RUN id

USER root

RUN apk add --no-cache php7-simplexml

COPY nginx/site.conf /etc/nginx/nginx.conf
#RUN chown -R nginx:nginx /etc/nginx/nginx.conf
RUN chmod -R 777 /etc/nginx/nginx.conf

COPY html /var/www/html
#RUN chown -R nginx:nginx /var/www/html/
RUN chmod -R 777 /var/www/html/

USER nobody