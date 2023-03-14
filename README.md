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

### Scrapy

##### Scrapy shell

Scrapy uses the `scrapy shell` to run interactive experiments.

```
scrapy crawl wikipedia
```

Pass crawler settings with the `-s` flag, like

```
scrapy crawl wikipedia -s CLOSESPIDER_ITEMCOUNT=50
```

Project-level crawler settings can be found in `webvis/settings.py`.

Pass spider settings with the `-a` flag, like

```
scrapy crawl wikipedia -a branching_factor=4
```

##### Scrapy scripts

Scrape from python script:

```
python webviz/process.py
```

### Test

```sh
pytest
```
