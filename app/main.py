import os

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from toggl import api, utils

app = FastAPI()

not_running_dict = {"is_running": False}
running_dict = {"is_running": True}


# Custom config without relying on any existing config file
config = utils.Config.factory(None)  # Without None it will load the default config file
config.api_token = os.environ.get("TOGGL_TOKEN")


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend())


@app.get("/")
async def root():
    """Redirect to /status (for the moment)"""
    return RedirectResponse("/status")


@app.get("/status")
@cache(expire=1)
async def status():
    """Returns running api.TimeEntry if running, else not_running_dict.

    As e.g. the Stream Desk software tends to fire huge amounts of requests we simply cache it for a few seconds
    to prevent extensive load on the toggl api.
    """
    if api.TimeEntry.objects.current(config=config):
        # can't return current as it throws stackoverflow, fix some day
        return running_dict
    return not_running_dict


@app.get("/continue")
async def continue_():
    """Continue last running entry"""

    res = continue__()
    return res


def continue__():
    last = api.TimeEntry.objects.all(order="desc", config=config)[0]
    if not last.is_running:
        last.continue_and_save()
        return running_dict
    else:
        return not_running_dict
        # return api.TimeEntry.objects.current(config=config)


@app.get("/toggle")
async def toggle():
    """Toggle running state"""
    if api.TimeEntry.objects.current(config=config):
        return stop_()
    else:
        return continue__()


@app.get("/stop")
async def stop():
    """Stop current running entry"""
    return stop_()


def stop_():
    api.TimeEntry.objects.current(config=config).stop_and_save()
    return not_running_dict
