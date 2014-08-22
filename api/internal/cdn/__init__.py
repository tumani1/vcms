# coding: utf-8
import on_play
import on_done
import on_update


routing = (
    (r'^on_play$', {'get': on_play.get}),
    (r'^on_done$', {'get': on_done.get}),
    (r'^on_update$', {'get': on_update.get}),
)

__all__ = ['routing']
