# Use latest stable Docker image for nginx server
FROM nginx:stable

# Change default configs to our modified ones.
RUN rm /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/
RUN rm /etc/nginx/conf.d/default.conf
COPY project.conf /etc/nginx/conf.d/

COPY bad-bots.conf /etc/nginx/conf.d/
COPY bot-list.map /etc/nginx/conf.d/


# Add certificates.
COPY certs/bmc-selfsigned.crt /etc/nginx/certs/bmc-selfsigned.crt
COPY certs/bmc-selfsigned.key /etc/nginx/certs/bmc-selfsigned.key

RUN apt-get update && apt-get install -y --no-install-recommends nano goaccess telnet traceroute apache2-utils logrotate

# Install logrotate
RUN apt-get update && apt-get -y install logrotate

# Add log rotating configs.
RUN rm /etc/logrotate.d/nginx
COPY logrotate/nginx /etc/logrotate.d/