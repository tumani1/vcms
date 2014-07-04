# coding: utf-8
import time


def detetime_to_unixtime(datetime):
    return time.mktime(datetime.timetuple())
