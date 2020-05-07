FROM trafex/alpine-nginx-php7

COPY nginx/site.conf /etc/nginx/conf.d/server.conf
RUN chown -R www-data:www-data /etc/nginx/conf.d/server.conf
RUN chmod -R 744 /etc/nginx/conf.d/server.conf

COPY html /var/www/html
RUN chown -R www-data:www-data /var/www/html/
RUN chmod -R 744 /var/www/html/