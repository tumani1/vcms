local conf = {
    exptime = {
        users     = 60,
        persons   = 60,
        topics    = 180,
        media     = 180,
        mediaunit = 180
    },
    sizes = {
        users     = {{30, 30}, {100, 100}, {200, 200}},
        persons   = {{30, 30}, {100, 100}, {200, 200}},
        topics    = {{30, 30}, {100, 100}, {200, 200}},
        media     = {{30, 30}, {100, 100}, {200, 200}},
        mediaunit = {{30, 30}, {100, 100}, {200, 200}}
    },
    memcache = {
        host = '127.0.0.1',
        port = 11211
    },
    noda = {
        host = '127.0.0.1',
        port = 5507
    }
}

return conf
