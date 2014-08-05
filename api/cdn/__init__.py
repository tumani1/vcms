# coding: utf-8
import on_play
import on_done

routing = {
    'on_play': {
        'get': on_play.get},
    'on_done': {
        'get': on_done.get},
}

__all__ = ['routing', ]
