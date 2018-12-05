"""Tests file for Home Assistant CLI (hass-cli)."""
import os

import homeassistant_cli.cli as cli
from homeassistant_cli.config import Configuration
from unittest import mock
import pytest

HASSIO_SERVER_FALLBACK = "http://hassio/homeassistant"
HASS_SERVER = "http://localhost:8123"


@pytest.mark.parametrize("description,env,expected_server,expected_token", [
   ("No env set, all should be defaults",
    {},
    HASS_SERVER,
    None),
   ("If only HASSIO_TOKEN, use default hassio",
    {'HASSIO_TOKEN': 'supersecret'},
    HASSIO_SERVER_FALLBACK, "supersecret"),
   ("Honor HASS_SERVER together with HASSIO_TOKEN",
    {'HASSIO_TOKEN': 'supersecret',
     'HASS_SERVER': 'http://localhost:999999'},
    "http://localhost:999999", "supersecret"),
   ("HASS_TOKEN should win over HASIO_TOKEN",
    {'HASSIO_TOKEN': 'supersecret',
     'HASS_TOKEN': 'I Win!'},
    HASS_SERVER, 'I Win!'),
])
def test_defaults(description, env, expected_server, expected_token):

    mockenv = mock.patch.dict(os.environ,
                              env)

    try:
        mockenv.start()
        ctx = cli.cli.make_context('hass-cli', ['--timeout', '1', 'info'])
        with ctx:
            try:
                cli.cli.invoke(ctx)
            except Exception:
                pass

        cfg: Configuration = ctx.obj

        assert cfg.server == expected_server
        assert cfg.token == expected_token
    finally:
        mockenv.stop()
