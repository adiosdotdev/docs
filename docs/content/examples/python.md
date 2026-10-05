# Deploying Python with Flask

This example runs Flask with a production WSGI server. Use the equivalent production command for Django, FastAPI, or another Python framework.

Review the [Python deployment path](https://adios.dev/deploy-python), the focused
[Flask deployment page](https://adios.dev/deploy-flask), or the
[Flask template](https://adios.dev/deploy-flask#templates) before applying this configuration to
an existing project.

## Configuration

Create an `adios.yaml` file in the root of your project:

```yaml
name: my-flask-api
build_cmd: pip install -r requirements.txt
start_cmd: gunicorn app:app --bind 0.0.0.0:$PORT

runtime:
  name: python@3.13
  port: 8000
  health_path: /healthz

env:
  FLASK_ENV: production
  SECRET_KEY: secret://SECRET_KEY
```

## Deploy

Before deploying, make sure to set your secrets using the CLI:

```bash
adios secret set SECRET_KEY
```

Then you can run the deployment command:

```bash
adios up
```
