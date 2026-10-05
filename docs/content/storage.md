# Storage, volumes, and backups

Adios separates object storage, workload volumes, backups, and build artifacts.
Open **Storage** in the dashboard and choose the tab for the data you need.

| Storage type | Use |
| --- | --- |
| S3 buckets | Files and objects accessed through object or S3-compatible APIs. |
| Volumes | Persistent filesystem data attached to workloads. |
| Backups | Available backup records and recovery information. |
| Build artifacts | Stored build outputs used by previews and deployments. |

## Create and use a bucket

1. Select the right team and open **Storage → S3 buckets**.
2. Choose **New bucket**, then select an Adios managed bucket or an external S3 bucket.
3. For an external bucket, provide its backend bucket name, endpoint, and required credentials.
4. Review the bucket's access and caching settings, then create it.
5. Open the bucket to browse objects and review connection information.

Use the endpoint and region shown for your bucket when configuring an S3 client.
Create a bucket access key when needed, save the returned secret privately, and
revoke keys that are no longer used. An access-key listing shows metadata; it
does not replace storing the secret at creation time.

The [object storage API](api/object-storage.md) supports listing, uploading,
downloading, and deleting objects. REST uploads accept raw bytes with an object
`key` query parameter, rather than multipart form data. The documented upload
limit is 5 GiB. Deleting a folder can delete its contents; review the prefix first.

## Public access and caching

Bucket access and edge caching are separate settings. Check both before serving
user uploads or downloadable files. Verify private objects remain inaccessible
to unauthenticated clients, and test cache behavior when updating public files.
Do not assume that an S3 bucket or a workload volume is public.

## Persistent volumes

Review the application's volume configuration and mount path before storing
state. Verify that the application writes to the mounted path and that data
survives a controlled restart. An application's source tree or build output is
not a substitute for a configured persistent volume.

For managed databases, follow the persistence and connection instructions for
[PostgreSQL](examples/postgres.md), [MySQL](examples/mysql.md),
[MongoDB](examples/mongodb.md), [Redis](examples/redis.md), or
[RabbitMQ](examples/rabbitmq.md).

## Backups and artifact cleanup

Inspect **Backups** for the records available to your workload. Confirm the
backup's source, time, and restore procedure, and test recovery on an appropriate
target before relying on it. Persistent storage by itself does not establish
that a usable backup exists.

Review **Build artifacts** before cleanup. Retained or in-use artifacts may be
needed by a release or preview and can be protected from deletion. Delete only
artifacts you have confirmed are no longer needed.
