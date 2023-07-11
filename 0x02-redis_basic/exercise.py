#!/usr/bin/env python3
""" Redis task using class Cache"""
import uuid
import redis
from typing import Union, Callable
import functools


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """_summary_

        Args:
            data (Union[str, bytes, int, float]): _description_

        Returns:
            str: _description_
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[str,
                                                          bytes, int, None]:
        """_summary_

        Args:
            key (str): _description_
            fn (Callable, optional): _description_. Defaults to None.

        Returns:
            Union[str, bytes, int, None]: _description_
        """
        data = self._redis.get(key)
        if data is not None:
            if fn is not None:
                data = fn(data)
            return data
        return None

    def get_str(self, key: str) -> Union[str, None]:
        """_summary_

        Args:
            key (str): _description_

        Returns:
            Union[str, None]: _description_
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """_summary_

        Args:
            key (str): _description_

        Returns:
            Union[int, None]: _description_
        """
        return self.get(key, fn=int)
