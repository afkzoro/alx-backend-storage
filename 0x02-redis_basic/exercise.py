#!/usr/bin/env python3
""" Redis task using class Cache"""
import uuid
import redis
from typing import Union, Callable
import functools


def replay(func: Callable) -> None:
    """
    Display the history of calls for a given function.

    Args:
        func: The function to display the history for.
    """
    inputs_key = f"{func.__qualname__}:inputs"
    outputs_key = f"{func.__qualname__}:outputs"

    inputs = cache._redis.lrange(inputs_key, 0, -1)
    outputs = cache._redis.lrange(outputs_key, 0, -1)

    print(f"{func.__qualname__} was called {len(inputs)} times:")
    for input_data, output_data in zip(inputs, outputs):
        input_str = input_data.decode("utf-8")
        output_str = output_data.decode("utf-8")
        print(f"{func.__qualname__}(*{input_str})")


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs and outputs for a function.
    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = f"{method.__qualname__}:inputs"
        outputs_key = f"{method.__qualname__}:outputs"

        input_data = str(args)
        self._redis.rpush(inputs_key, input_data)

        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, output)

        return output

    return wrapper


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

    @call_history
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
