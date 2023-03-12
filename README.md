# Webviz

## Developer Setup

```sh
source setup.sh
```

This project uses [poetry](https://python-poetry.org/docs/) to manage dependencies and virtual environments. No need to use `pip` or `virtualenv`.

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
