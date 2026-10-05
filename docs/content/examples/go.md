# Deploying Go

Compile the Go service to one production binary, then declare its port and health path explicitly.

Review the [Go deployment path](https://adios.dev/deploy-golang) or inspect the
[Go Gin template](https://adios.dev/deploy-golang#templates) before applying this runtime configuration
to an existing service.

## Configuration

Create an `adios.yaml` file in the root of your project:

```yaml
name: my-go-api
build_cmd: go build -o main .
start_cmd: ./main

runtime:
  name: go@1.25
  port: 8080
  health_path: /healthz

env:
  GIN_MODE: release
```

## Deploy

```bash
adios up
```
