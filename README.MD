# Toggl-Cli-API

[![Docker](https://github.com/MaxWinterstein/toggl-cli-api/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/MaxWinterstein/toggl-cli-api/actions/workflows/docker-publish.yml)

Simply fastapi based wrap around [toggl-cli](https://github.com/AuHau/toggl-cli) to be used e.g. as docker container.

More designed like an RPC than API, but 🤷🏻‍♂️ .

## Why

This was mostly made to be used with an [elgato Stream Deck](https://www.elgato.com/en/stream-deck).  
There are some plugins available for toggl, but none provided me a simple _"Just continue the last thing I did"_ button.

## Run `toggl-cli-api`

There are multiple ways to use this little thing.  
I just run it as a docker container, e.g. on my synology.

All needed is your toggl API token, see below, and make it available as environment variable `TOGGL_TOKEN`.

### Run as docker

```bash
docker run --rm -ti -e TOGGL_TOKEN=123abcddef -p 8080:80 ghcr.io/maxwinterstein/toggl-cli-api:main
```

### Run as docker-compose

```yaml
version: "2.0"

services:
  toggl-cli-api:
    image: ghcr.io/maxwinterstein/toggl-cli-api:main
    environment:
      - TOGGL_TOKEN=123abcddef
    restart: always
    ports:
      - 8880:80
```

## Use with Elgato Strem Deck

First you need to install the [API Request](https://github.com/mjbnz/streamdeck-api-request) plugin by [@mjbnz](https://github.com/mjbnz):  
![](images/Plugin_API_Request.png)

Configuration is done like this:  
![](images/configuration.png)

Adjust IP/hostname/port to your needs.

### Get yout toggl token

See https://support.toggl.com/en/articles/3116844-where-is-my-api-key-located

## Restrictions

For the moment its main purpose it to `continue` and `stop` the last running entry.  
More features might be coming later.

## Thx

Thx to [@tobimori and his streamdeck-toggl](https://github.com/tobimori/streamdeck-toggl) that inspired me, showed me i have no clue of javascript and let me steal the icons. ❤️.
