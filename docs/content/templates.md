# Templates

Adios templates are ready-to-deploy starters with an `adios.yaml` already in the
repo. Use them when you want a working app, API, database, cache, or queue before
you start wiring up build commands, runtime ports, volumes, and deploy settings
yourself.

- [Browse deployment paths](https://adios.dev/deploy)
- [Inspect a template contract](https://adios.dev/deploy-nextjs#templates)
- [Deploy a template](https://app.adios.dev/app/new?source=template&template=nextjs)

## Templates on Deployment Pages

Adios keeps the deployment decision and exact starter contract together:

- Use a **deployment page** to review whether a framework or service fits your
  runtime, health, secret, persistence, and failure requirements.
- On that same page, inspect each starter's repository, source path, package
  workflow, runtime, public template key, clone commands, and one-click deploy
  option.
- Use this documentation when you need the console and local clone mechanics.

Start from the [deployment directory](https://adios.dev/deploy) whether you already chose a
technology or still need to compare the available paths. Previous `/templates`
URLs permanently redirect to the corresponding deployment page.

## Available Templates

- **Next.js:** JavaScript and TypeScript starters using npm or pnpm.
- **Application platforms:** A Supabase-connected Node.js API, WordPress,
  PocketBase, and Strapi starters.
- **Static sites:** Nginx hosting for HTML, CSS, JavaScript, and SPAs.
- **Node.js API:** Express, Fastify, Hono, and NestJS starters.
- **Python API:** FastAPI, Django, Flask, Litestar, and Sanic starters.
- **Ruby apps and APIs:** Rails, Sinatra, Grape, Hanami Router, and Roda starters.
- **PHP apps and APIs:** Laravel, Symfony, CakePHP, CodeIgniter 4, Yii 2, and PHP 8.2 starters.
- **Go API:** Gin, Chi, Echo, Fiber, and Beego starters.
- **.NET apps and APIs:** ASP.NET Core, FastEndpoints, Blazor, ABP Framework, Orchard Core, and .NET 8 starters.
- **Data and search services:** PostgreSQL, pgvector, MongoDB, MySQL, Redis,
  RabbitMQ, Typesense, and Qdrant.

## Web Console

Use the console when you want the shortest path from a template to a live app.

1. Open the [deployment directory](https://adios.dev/deploy).
2. Pick the technology and inspect its exact starter variants.
3. Select **Deploy now**.
4. Log in or create an account when prompted.
5. Review the template, region, resources, and deploy policy.
6. Create the app and follow the deployment logs.

Template links include a `template` query value so the console can preselect the
right starter after authentication.

## Local Clone

Use the local path when you want to inspect or customize files before deploying.
Every catalog variant has its own standalone repository, so the repository root
is also the directory that contains `adios.yaml`:

```bash
git clone https://github.com/adiosdotdev/template-python-fastapi.git
cd template-python-fastapi
adios up
```

The same flow works for application and data-service templates:

```bash
git clone https://github.com/adiosdotdev/template-node-fastify.git
cd template-node-fastify
adios up
```

```bash
git clone https://github.com/adiosdotdev/template-postgres-16.git
cd template-postgres-16
adios up
```

Use the **View source** link on a deployment page to open the exact repository
for that variant. Run `adios up` from its repository root.

## Template Keys

These are the public template keys used by the console deploy links:

- **nextjs:** Next.js JavaScript starter using npm.
- **nextjs-pnpm:** Next.js JavaScript starter using pnpm.
- **nextjs-typescript:** Next.js TypeScript starter using npm.
- **nextjs-pnpm-typescript:** Next.js TypeScript starter using pnpm.
- **supabase:** Node.js API connected to an existing Supabase project.
- **wordpress:** WordPress 7 with managed MySQL and persistent content.
- **pocketbase:** PocketBase with persistent SQLite data and generated credentials.
- **strapi:** Strapi 5 with managed PostgreSQL and persistent uploads.
- **nginx:static:** Static Nginx site starter.
- **node-express, node-fastify, node-hono, node-nestjs:** Node.js API starters.
- **python-fastapi, python-fastapi-pipenv:** FastAPI starters.
- **python-django, python-django-pipenv:** Django starters.
- **python-gather:** MIT-licensed personal and team scheduling with Google Calendar, Microsoft Outlook, and iCloud CalDAV integrations. Includes public booking links, weekly availability, PostgreSQL, and a calendar retry worker. Configure provider credentials and your public HTTPS origin after deployment.
- **python-flask, python-flask-pipenv:** Flask starters.
- **python-litestar, python-sanic:** Litestar and Sanic starters.
- **ruby-rails:** Ruby on Rails starter.
- **ruby-sinatra:** Ruby Sinatra starter.
- **ruby-grape:** Ruby Grape starter.
- **ruby-hanami, ruby-roda:** Hanami Router and Roda starters.
- **php-laravel:** PHP Laravel starter.
- **php-symfony:** PHP Symfony starter.
- **php-cakephp, php-codeigniter4, php-yii2:** Additional PHP framework starters.
- **php:** PHP 8.2 starter.
- **go-gin:** Go Gin starter.
- **go-chi:** Go Chi starter.
- **go-echo:** Go Echo starter.
- **go-fiber:** Go Fiber starter.
- **go-beego:** Go Beego starter.
- **dotnet-aspnet-core:** ASP.NET Core starter.
- **dotnet-fastendpoints:** .NET FastEndpoints starter.
- **dotnet:** .NET 8 minimal API starter.
- **dotnet-blazor, dotnet-abp, dotnet-orchard-core:** .NET application starters.
- **postgres:15, postgres:16, postgres:17, pgvector:16:** PostgreSQL data services.
- **mongodb:7, mysql:8, redis:7:** Database and cache services.
- **rabbitmq:3-management:** RabbitMQ with its management interface.
- **typesense:** Typesense full-text and vector search service.
- **qdrant:** Qdrant vector database with administrator and read-only keys.

## After Deploy

After the deployment starts, use the app dashboard or CLI logs to inspect build
and runtime output:

```bash
adios logs --build
adios logs --runtime
```

Once the app has source attached, open it in a workspace to edit files, run
previews, add secrets, connect managed resources, and promote new deploys.
