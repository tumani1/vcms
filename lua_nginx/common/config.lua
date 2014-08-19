local conf = {
    exptime = {
        users     = 60,
        persons   = 60,
        topics    = 180,
        media     = 180,
        mediaunit = 180
    },
    sizes = {
        users     = {{30, 30}, {100, 100}},
        persons   = {{30, 30}, {100, 100}},
        topics    = {{30, 30}, {100, 100}},
        media     = {{30, 30}, {100, 100}},
        mediaunit = {{30, 30}, {100, 100}}
    },
    memcache = {
        host = '127.0.0.1',
        port = 11211
    },
    zerorpc = {
        host = '192.168.1.104',
        port = 6700
    },
    noda = {
        host = '127.0.0.1',
        port = 9902
    }
}

return conf
