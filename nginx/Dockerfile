# Use official Nginx image
FROM nginx:latest

# Install OpenSSL
RUN apt update -y && apt upgrade -y && apt install -y openssl

# Setup SSL key
RUN mkdir -p /etc/nginx/ssl
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
	-keyout /etc/ssl/private/giternance.key \
	-out /etc/ssl/certs/giternance.crt \
	-subj "/C=US/ST=State/L=City/O=Giternance/OU=IT/CN=giternance.local"

# Create Nginx runtime directory
RUN mkdir -p /var/run/nginx

# Copy Nginx config
COPY ./config/default.conf /etc/nginx/conf.d

# Copy HTML contents
COPY ./pages /usr/share/nginx/html

# Expose HTTPS port
EXPOSE 443

# Run Nginx in foreground
CMD ["nginx", "-g", "daemon off;"]
