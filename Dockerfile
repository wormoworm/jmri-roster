FROM php:7.4.5-apache

# We need the rewrite module enabled. This allows us to structure the API URLs as we like.
RUN a2enmod rewrite

COPY html /var/www/html

RUN chown -R www-data:www-data /var/www/html/
RUN chmod a+rx /var/www/html/