# Deploying PostgreSQL

Adios provides official templates for running PostgreSQL databases. Using a template simplifies configuration and ensures best practices for persistence and performance.

Review the [PostgreSQL deployment checks](https://adios.dev/deploy-postgres) and compare the
[available PostgreSQL templates](https://adios.dev/deploy-postgres#templates) before choosing a major
version.

## Configuration

Create an `adios.yaml` file in the root of your project:

```yaml
name: my-postgres-db
template: postgres:16
env:
  POSTGRES_USER: myuser
  POSTGRES_PASSWORD: "secret://POSTGRES_PASSWORD"
  POSTGRES_DB: mydb
```

*Note: You can also use `postgres:15` or `postgres:17` if you need a specific version.*

## Deploy

Before deploying, make sure to set your secrets using the CLI:

```bash
$ adios secret set POSTGRES_PASSWORD my_secure_password
```

Then you can run the deployment command:

```bash
$ adios up
```

Your database will automatically be provisioned with a persistent volume to ensure your data is saved across restarts.
