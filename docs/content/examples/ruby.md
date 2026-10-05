# Deploying Ruby

This example deploys a Ruby web process such as Sinatra with explicit production commands and runtime settings.

Review the [Ruby deployment path](https://adios.dev/deploy-ruby) or inspect the
[Ruby on Rails template](https://adios.dev/deploy-rails#templates) before applying this runtime
configuration to an existing application.

## Configuration

Create an `adios.yaml` file in the root of your project:

```yaml
name: my-ruby-app
build_cmd: bundle install
start_cmd: bundle exec ruby app.rb

runtime:
  name: ruby@3.2
  port: 8080
  health_path: /healthz

env:
  RACK_ENV: production
```

## Deploy

```bash
adios up
```
