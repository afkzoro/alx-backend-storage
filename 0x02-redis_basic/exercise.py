#!/usr/bin/env python3
""" Redis task using class Cache"""
import uuid
import redis
from typing import Union, Callable
import functools


def call_history(method: Callable) -> Callable:
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        # Store input arguments
        self._redis.rpush(input_key, str(args))

        # Execute the wrapped function to retrieve the output
        output = method(self, *args, **kwargs)

        # Store the output
        self._redis.rpush(output_key, output)

        return output

    return wrapper


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    def store(self, data):
        key = str(uuid.uuid4())
        self._redis.set(key, str(data))
        return key

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

    def replay(method):
        redis_client = redis.Redis()
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"

        inputs = redis_client.lrange(input_key, 0, -1)
        outputs = redis_client.lrange(output_key, 0, -1)

        print(f"{method.__qualname__} was called {len(inputs)} times:")

        for input_args, output in zip(inputs, outputs):
            input_args = input_args.decode()
            output = output.decode()
            print(f"{method.__qualname__}(*{input_args}) -> {output}")
