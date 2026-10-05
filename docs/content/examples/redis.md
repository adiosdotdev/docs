# Deploying Redis

Adios provides an official template for running Redis. Redis is often used for caching, session management, or as an in-memory data store.

Review the [Redis deployment checks](https://adios.dev/deploy-redis) or inspect the exact
[Redis 7 template](https://adios.dev/deploy-redis#templates) before creating the service.

## Configuration

Create an `adios.yaml` file in the root of your project:

```yaml
name: my-redis-cache
template: redis:7
```

## Deploy

```bash
$ adios up
```
