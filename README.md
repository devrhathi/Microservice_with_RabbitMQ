# Microservice communication with RabbitMQ

## Steps to execute

1. Open 2 terminals

2. Create rabbitmq_network using this command:

```
docker network create rabbitmq_network --subnet=172.21.0.1/16 --gateway 172.21.0.1
```

3. Then start rabbitmq container attached to the network

```
docker run --rm  --network rabbitmq_network -it -p 15672:15672 -p 5672:5672 --name rabbitmq -e RABBITMQ_HEARTBEAT=800 rabbitmq
```

4. In the other terminal, run following commands (make sure you are in project's root directory)

```
docker compose build
docker compose up
```

5. To restart, press `ctrl+c` in both terminals, run the following command and then restart from step 3.

```
docker compose down
```
