#!/usr/bin/env python3
""" web.py- Caching exercise """
import requests
import redis
import functools

CACHE_EXPIRATION = 10

redis_client = redis.Redis()


def count_calls(func):
    @functools.wraps(func)
    def wrapper(url):
        key = f"count:{url}"
        redis_client.incr(key)
        return func(url)
    return wrapper


def cache_result(func):
    @functools.wraps(func)
    def wrapper(url):
        key = f"result:{url}"
        cached_result = redis_client.get(key)
        if cached_result:
            return cached_result.decode("utf-8")
        result = func(url)
        redis_client.setex(key, CACHE_EXPIRATION, result)
        return result
    return wrapper


@count_calls
@cache_result
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text


# Usage example:
html_content = get_page("http://slowwly.robertomurray.co.uk")
print(html_content)
