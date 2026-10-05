# Deploying .NET

This example publishes and runs a .NET 8 web application with an explicit output path, port, and health endpoint.

Review [.NET deployment requirements](https://adios.dev/deploy-dotnet) or start from an
[ASP.NET Core template](https://adios.dev/deploy-aspnet-core#templates) before applying this
runtime configuration to an existing project.

## Configuration

Create an `adios.yaml` file in the root of your project:

```yaml
name: my-dotnet-api
build_cmd: dotnet publish -c Release -o out
start_cmd: dotnet out/MyApp.dll

runtime:
  name: dotnet@8
  port: 8080
  health_path: /healthz

env:
  ASPNETCORE_URLS: http://*:$PORT
```

## Deploy

```bash
adios up
```
