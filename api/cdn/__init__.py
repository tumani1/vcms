# coding: utf-8
import on_play
import on_done
import on_update

routing = {
    'on_play': {
        'get': on_play.get},
    'on_done': {
        'get': on_done.get},
    'on_update': {
        'get': on_update.get},
}

__all__ = ['routing', ]
