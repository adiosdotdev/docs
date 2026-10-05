# Deploying MySQL

Adios provides official templates for running MySQL databases.

Review the [MySQL deployment checks](https://adios.dev/deploy-mysql) or inspect the exact
[MySQL 8 template](https://adios.dev/deploy-mysql#templates) before creating the service.

## Configuration

Create an `adios.yaml` file in the root of your project:

```yaml
name: my-mysql-db
template: mysql:8
env:
  MYSQL_ROOT_PASSWORD: "secret://MYSQL_ROOT_PASSWORD"
  MYSQL_DATABASE: mydb
  MYSQL_USER: myuser
  MYSQL_PASSWORD: "secret://MYSQL_PASSWORD"
```

## Deploy

Before deploying, make sure to set your secrets using the CLI:

```bash
$ adios secret set MYSQL_ROOT_PASSWORD my_secure_password
$ adios secret set MYSQL_PASSWORD my_other_password
```

Then you can run the deployment command:

```bash
$ adios up
```

Your database will automatically be provisioned with a persistent volume so data is retained across restarts.
