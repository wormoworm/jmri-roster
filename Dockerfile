FROM php:7.2.30-apache

# We need the rewrite module enabled. This allows us to structure the API URLs as we like.
RUN a2enmod rewrite

COPY

