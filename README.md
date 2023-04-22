# Microservice communication with RabbitMQ

## Steps to execute

1. Open 2 terminals

2. Create rabbitmq_network and start rabbitmq container attached to it

```
docker network create rabbitmq_network
docker run --rm  --network rabbitmq_network -it -p 15672:15672 -p 5672:5672 --name rabbitmq -e RABBITMQ_HEARTBEAT=600 rabbitmq
```

3. Execute `docker network inspect rabbitmq_network` and replace IP address in ConnectionParameters in producer and all consumers with the Gatway IP address shown.

4. In the other terminal, run following commands (make sure you are in project's root directory)

```
docker compose build
docker compose up
```

4. To restart, press `ctrl+c` in both terminals, then run start from step 1

