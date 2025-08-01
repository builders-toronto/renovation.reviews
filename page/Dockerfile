FROM nginx:alpine
RUN apk add --no-cache python3 ca-certificates && update-ca-certificates
COPY ./index.html /usr/share/nginx/html/index.html
COPY ./story.html /usr/share/nginx/html/story.html
COPY images/ /usr/share/nginx/html/images/
COPY conf/default.conf /etc/nginx/conf.d/default.conf
WORKDIR /app
COPY supply_server.py /app/supply_server.py
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh
EXPOSE 1337
CMD ["/app/start.sh"]