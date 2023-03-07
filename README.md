# Webviz

## Developer Setup

```sh
source setup.sh
```

This project uses [poetry]() to manage dependencies and [virtualenv]() to manage python versions.

### Poetry

The setup script installs poetry and activates the local virtualenv environment. Add new dependencies to the project using

```sh
poetry add numpy
poetry install
```

## Scripts

### Scrape

```
scrapy crawl wikipedia -L WARN
```

### Test

```sh
pytest || echo "Tests failed"
```
