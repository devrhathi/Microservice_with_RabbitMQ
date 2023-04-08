# Microservice communication with RabbitMQ

## Steps to execute

1. Open 2 terminals

2. Create rabbitmq_network and start rabbitmq container attached to it

```
docker network create rabbitmq_network
docker run --rm  --network rabbitmq_network -it -p 15672:15672 -p 5672:5672 --name rabbitmq rabbitmq
```

3. Execute `docker network inspect rabbitmq` and replace IP address in ConnectionParameters in producer and all consumers with the Gatway IP address shown.

4. In the other terminal, run following commands (make sure you are in project's root directory)

```
docker compose build
docker compose up
```

4. To restart, press `ctrl+c` in both terminals, then run `docker compose down` where microservices were running (not rabbitmq terminal) and start from step 1

## Issues to fix

- [ ] After a while, RabbitMQ connection to producer automatically stops saying : "missed heartbeats from client, timeout: 60s"

- [ ] None of the consumers are printing anything in the logs (console) using python's print statement (even though they are being executed)

- [ ] Read database not working
