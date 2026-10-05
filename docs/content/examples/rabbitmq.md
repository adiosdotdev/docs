# Deploying RabbitMQ

Adios provides an official template for running RabbitMQ, a widely used open-source message broker.

Review the [RabbitMQ deployment checks](https://adios.dev/deploy-rabbitmq) or inspect the exact
[RabbitMQ management template](https://adios.dev/deploy-rabbitmq#templates) before
creating the broker.

## Configuration

Create an `adios.yaml` file in the root of your project:

```yaml
name: my-rabbitmq
template: rabbitmq:3-management
env:
  RABBITMQ_DEFAULT_USER: admin
  RABBITMQ_DEFAULT_PASS: "secret://RABBITMQ_DEFAULT_PASS"
```

*Note: The `3-management` template comes with the RabbitMQ Management UI plugin pre-enabled.*

## Deploy

Before deploying, make sure to set your secrets using the CLI:

```bash
$ adios secret set RABBITMQ_DEFAULT_PASS my_secure_password
```

Then you can run the deployment command:

```bash
$ adios up
```

Your broker will be ready to accept AMQP connections as well as provide access to the management dashboard.
