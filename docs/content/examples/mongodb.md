# Deploying MongoDB

Adios provides official templates for running MongoDB databases, making it simple to deploy a NoSQL document store with built-in persistence.

Review the [MongoDB deployment checks](https://adios.dev/deploy-mongo) or inspect the exact
[MongoDB 7 template](https://adios.dev/deploy-mongo#templates) before creating the service.

## Configuration

Create an `adios.yaml` file in the root of your project:

```yaml
name: my-mongodb
template: mongodb:7
env:
  MONGO_INITDB_ROOT_USERNAME: root
  MONGO_INITDB_ROOT_PASSWORD: "secret://MONGO_INITDB_ROOT_PASSWORD"
```

## Deploy

Before deploying, make sure to set your secrets using the CLI:

```bash
$ adios secret set MONGO_INITDB_ROOT_PASSWORD my_secure_password
```

Then you can run the deployment command:

```bash
$ adios up
```

Your MongoDB instance will be deployed with persistent storage automatically attached.
