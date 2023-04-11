# Microservice communication with RabbitMQ

## Steps to execute

1. Open 2 terminals

2. Create rabbitmq_network and start rabbitmq container attached to it

```
docker network create rabbitmq_network
docker run --rm  --network rabbitmq_network -it -p 15672:15672 -p 5672:5672 --name rabbitmq rabbitmq
```

3. Execute `docker network inspect rabbitmq_network` and replace IP address in ConnectionParameters in producer and all consumers with the Gatway IP address shown.

4. In the other terminal, run following commands (make sure you are in project's root directory)

```
docker compose build
docker compose up
```

4. To restart, press `ctrl+c` in both terminals, then run start from step 1

## Issues to fix

- [x] After a while, RabbitMQ connection to producer automatically stops saying : "missed heartbeats from client, timeout: 60s"

- [x] None of the consumers are printing anything in the logs (console) using python's print statement (even though they are being executed)

- [x] Read database not working

- [x] All requests are working for the first time, then the consumers are caching the action

- [ ] in delete_record request, find a way to return error Ack from consumer_three if srn passed to producer is not there in database
