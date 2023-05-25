FROM nginx:1.21-alpine

# copy notebook website conents over
COPY notebooks /var/www/html
COPY .htpasswd /etc/nginx/

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d