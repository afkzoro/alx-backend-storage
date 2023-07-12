#!/usr/bin/env python3
""" web.py- Caching exercise """
import requests
import redis
import functools

CACHE_EXPIRATION = 10


def count_calls(method):
    @functools.wraps(method)
    def wrapper(self, url):
        key = f"count:{url}"
        self._redis.incr(key)
        return method(self, url)
    return wrapper


def cache_result(method):
    @functools.wraps(method)
    def wrapper(self, url):
        key = f"result:{url}"
        cached_result = self._redis.get(key)
        if cached_result:
            return cached_result.decode("utf-8")
        result = method(self, url)
        self._redis.setex(key, CACHE_EXPIRATION, result)
        return result
    return wrapper


class WebPage:
    def __init__(self):
        self._redis = redis.Redis()

    @count_calls
    @cache_result
    def get_page(self, url: str) -> str:
        response = requests.get(url)
        return response.text


# Usage example:
web = WebPage()
html_content = web.get_page("http://slowwly.robertomurray.co.uk")
print(html_content)
