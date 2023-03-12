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
poetry add pytest --group test # test dependencies
poetry add autpep8 --group dev # dev dependencies

poetry install

poetry install --without test,dev # only install runtime dependencies
```

## Scripts

### Scrape

```
scrapy crawl wikipedia -L WARN
```

Common crawl parameters:

```
-a start_url=https://en.wikipedia.org/wiki/Salix_bebbiana
-a children=4

-s DEPTH_LIMIT=2
-s CLOSESPIDER_ITEMCOUNT=10

```

Scrape from script:

```
python webviz/process.py
```

### Test

```sh
pytest
```
