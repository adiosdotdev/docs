# Contributing to Adios documentation

The user guides and API reference share their maintained source with the Adios
website. This guide covers local previews, validation, synchronization, and
Read the Docs setup.

## Build locally

Use Python 3.12:

```sh
python3 -m venv .venv
.venv/bin/pip install -r docs/requirements.txt -r docs/requirements-check.txt
.venv/bin/python docs/validate_api.py
.venv/bin/mkdocs build --strict
.venv/bin/mkdocs serve
```

The preview is available at `http://127.0.0.1:8000`. Building these pages does
not call the Adios API and requires no Adios credentials.

## Repository layout

- `docs/content/`: Markdown guides, API reference, and downloadable assets.
- `docs/nav.yml`: documentation navigation.
- `docs/validate_api.py`: offline OpenAPI, Postman, and example validation.
- `docs/api-provenance.json`: source hashes and API export metadata.
- `mkdocs.yml`: Material for MkDocs theme and build settings.
- `.readthedocs.yaml`: Read the Docs build configuration.
- `.github/workflows/docs.yml`: API validation and strict documentation build.

## Maintain the shared content

This repository is the public publishing mirror of the documentation maintained
in the Adios website repository. Make changes in its `docs/content/` and
`docs/navigation.json` so the website and Read the Docs stay in sync. Regenerate
the API reference there when the reviewed public API changes.

From the website checkout, with this repository alongside it as `adios-docs`:

```sh
npm run docs:export
rsync -av --delete --exclude='.git/' --exclude='.venv/' --exclude='site/' output/docs/readthedocs/ ../adios-docs/
git -C ../adios-docs diff --stat
git -C ../adios-docs diff --check
```

Review and commit the changes in this repository, then push them. Read the Docs
rebuilds the published documentation when the connected GitHub branch changes.
The website deploys through its own release process using the same sources.

## Connect Read the Docs

Import this public repository into Read the Docs and use `main` as the default
branch, with `.readthedocs.yaml` as the configuration file. Install the Read the
Docs GitHub App for this repository to enable automatic builds. The project URL
is assigned during import.

See the official [project setup instructions](https://docs.readthedocs.com/platform/stable/intro/add-project.html)
and [GitHub integration guide](https://docs.readthedocs.com/platform/stable/reference/git-integration.html).
