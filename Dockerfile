FROM php:7.2.30-apache

# We need the rewrite module enabled. This allows us to structure the API URLs as we like.
RUN a2enmod rewrite

COPY html /var/www/html

# RUN chown -R 1023:1023 /var/www/html
RUN chmod -R 777 /var/www/html