import json

import requests

from app import app, cache


# TODO Load these from config?
MOJANG_TIMEOUT = 5
MOJANG_DATA_CACHE_EXPIRES = 3600


class ProfileNotFound(Exception):
    def __init__(self, uuid=None, username=None):
        self.uuid = uuid
        self.username = username


class Profile(object):

    """Mojang user profile for Minecraft."""

    def __init__(self, uuid=None, username=None):
        if username:
            uuid = self._fetch_uuid_for_username(username)

        self.data = self._fetch_profile_for_uuid(uuid)

    @property
    def uuid(self):
        return self.data['id']

    @property
    def username(self):
        return self.data['name']

    def _fetch_uuid_for_username(self, username):
        cache_key = 'uuid_for_username_%s' % username

        @cache.cache(cache_key, expire=MOJANG_DATA_CACHE_EXPIRES)
        def get_uuid_from_mojang():
            try:
                url = "https://api.mojang.com/profiles"
                payload = {'agent': 'minecraft', 'name': username}
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=MOJANG_TIMEOUT)

                if response.status_code != requests.codes.ok:
                    raise ProfileNotFound(username=username)

                response = response.json()
                if response['size'] > 0:
                    return response['profiles'][0]['id']

            except ProfileNotFound as e:
                raise e

            except Exception as e:
                app.logger.exception(e)
                raise ProfileNotFound(username=username)

            raise ProfileNotFound(username=username)

        return get_uuid_from_mojang()

    def _fetch_profile_for_uuid(self, uuid):
        cache_key = 'profile_for_uuid_%s' % uuid

        @cache.cache(cache_key, expire=MOJANG_DATA_CACHE_EXPIRES)
        def get_profile_from_mojang():
            try:
                url = "https://sessionserver.mojang.com/session/minecraft/profile/%s" % uuid
                headers = {'Content-Type': 'application/json'}
                response = requests.get(url, headers=headers, timeout=MOJANG_TIMEOUT)

                if response.status_code != requests.codes.ok:
                    raise ProfileNotFound(uuid=uuid)

                return response.json()

            except ProfileNotFound as e:
                raise e

            except Exception as e:
                app.logger.exception(e)
                ProfileNotFound(uuid=uuid)

            raise ProfileNotFound(uuid=uuid)

        return get_profile_from_mojang()
