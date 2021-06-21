import random
import time

class uuid64:

    @staticmethod
    def int():
        """Return UUID as integer"""
        base = __builtin__.int(time.time()) << 48
        rand = random.SystemRandom().getrandbits(16)
        return base + rand

    @staticmethod

    def hex():
        """Return UUID as hexidecimal"""
        return hex(int())[2:-1]

    @staticmethod

    def bin():
        """Return UUID as binary"""
        return bin(int())[2:]

    @staticmethod
    def oct():
        """Return UUID as octodecimal"""
        return oct(int())[:-1]