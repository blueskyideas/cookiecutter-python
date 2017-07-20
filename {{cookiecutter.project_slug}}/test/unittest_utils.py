'''
a collection of helpers to be used for unit testing
'''

import signal
import unittest
import asyncio
from unittest.mock import MagicMock

class TestHang(Exception):
    pass

def test_name(func):
    '''
    decorator that prints the test name before
    starting a test

    usage:

    @test_name
    def test_this(self):
        pass

    '''
    def inner(*args, **kwargs): 
        print ("\n******** STARTING TEST: %s *********" % func.__name__)
        return func(*args, **kwargs) 
    return inner


def _test_hang_handler(signum, frame):
    raise TestHang

def set_test_hang_alarm(func):
    '''
    decorator that sets an alarm of 1 second before
    starting any test.

    If a test takes longer than 1 second a TestHang
    exception is raised.

    usage inside a unittest.TestCase:

    @set_test_hang_alarm
    def setUp(self):
        pass
    '''

    def inner(*args,**kwargs):
        signal.signal(signal.SIGALRM, _test_hang_handler)
        signal.alarm(1)
        return func(*args,**kwargs)
    return inner

def clear_test_hang_alarm(func):
    '''
    decorator that resets any test hang alarms after
    a test is comleted.

    usage inside a unittest.TestCase:

    @clear_test_hang_alarm
    def tearDown(self):
        pass
    '''
    def inner(*args,**kwargs):
        signal.alarm(0)
        return func(*args,**kwargs)
    return inner

def close_all_threads(func):
    '''
    decorator that closes any threads after a test is run.

    usage inside a unittest.TestCase:

    add an object with a close method to self.threads_to_close.
    The close methods instructs the thread to close.

    @close_all_threads
    def test_this(self):
        pass
    '''
    def inner(self):
        try:
            return func(self)
        finally:
            [x.close() for x in self.threads_to_close]

    return inner

def asyncio_test(func):
    '''
    decorator that runs a test as a coroutine including
    setup and teardown coroutines.

    usage inside a unittest.TestCase:
    async def async_setUp(self):
        pass

    async def async_tearDown(self):
        pass

    @asyncio_test
    async def test_this(self):
        pass

    '''
    def inner(self):
        async def run(self,*args,**kwargs):
            await self.async_setUp()

            try:
                return await func(self,*args,**kwargs)
            finally:
                await self.async_tearDown()

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.set_debug(True)

        try:
            self.loop.run_until_complete(run(self))
        finally:
            self.loop.close()

    return inner

def AsyncMock(*args, **kwargs):
    '''
    function that mocks a coroutine. 

    mock attribute is a MagicMock object
    that records mock usage

    usage:

    x = AsyncMock()
    await x()

    x.mock.assert_called_once()
    '''
    m = MagicMock(*args, **kwargs)

    async def mock_coro(*args, **kwargs):
        return m(*args, **kwargs)

    mock_coro.mock = m
    return mock_coro