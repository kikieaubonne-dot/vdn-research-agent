"""Cooperative deadline and HTTP-attempt budget, shared across provider retries.

The checkpoint persists counters BEFORE each side effect. No worker threads or
background calls survive a cycle. An in-flight socket may finish after deadline.
"""
from __future__ import annotations

import time
from contextlib import contextmanager
from contextvars import ContextVar


class BudgetExhausted(RuntimeError):
    def __init__(self,reason,*,scope='operation',resource='unknown',limit=None,used=None):
        super().__init__(reason)
        self.scope,self.resource,self.limit,self.used=scope,resource,limit,used

    def details(self):
        return {'kind':'budget','reason':str(self),'scope':self.scope,'resource':self.resource,
                'limit':self.limit,'used':self.used}


CURRENT = ContextVar('vdn_budget', default=None)


class Budget:
    def __init__(self, seconds, max_http, checkpoint=None, *, http_scope='operation', time_scope='operation'):
        self.deadline = time.monotonic() + seconds
        self.seconds=seconds
        self.http_scope,self.time_scope=http_scope,time_scope
        self.max_http = max_http
        self.http_calls = 0
        self.checkpoint = checkpoint

    def check(self):
        if time.monotonic() >= self.deadline:
            raise BudgetExhausted('budget de temps atteint',scope=self.time_scope,resource='compute_s',limit=self.seconds,used=self.seconds)

    def request(self, timeout=20):
        self.check()
        if self.http_calls >= self.max_http:
            raise BudgetExhausted('budget HTTP atteint',scope=self.http_scope,resource='http_calls',limit=self.max_http,used=self.http_calls)
        if self.checkpoint:
            self.checkpoint('http_calls')
        self.http_calls += 1
        return min(timeout, max(0.001, self.deadline - time.monotonic()))


@contextmanager
def using(budget):
    token = CURRENT.set(budget)
    try:
        yield budget
    finally:
        CURRENT.reset(token)


def check():
    if CURRENT.get():
        CURRENT.get().check()


def request(timeout=20):
    return CURRENT.get().request(timeout) if CURRENT.get() else timeout


def fetch_attempt():
    check()
    active = CURRENT.get()
    if active and active.checkpoint:
        active.checkpoint('fetch')


def pause(seconds):
    check()
    budget = CURRENT.get()
    time.sleep(min(seconds, max(0, budget.deadline - time.monotonic())) if budget else seconds)
    check()
