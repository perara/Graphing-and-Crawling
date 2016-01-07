__author__ = 'perar'
import threading
from concurrent.futures import ThreadPoolExecutor


class Handler():


    def __init__(self, threads=4):
        self.threads = 4
        self.pool = ThreadPoolExecutor(max_workers=self.threads)
        self.futures = []


    def add(self, worker, *args):
        future = self.pool.submit(worker, *args)
        return future

