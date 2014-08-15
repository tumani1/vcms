local conf = require "config";

local function return_not_found(msg)
    ngx.status = ngx.HTTP_NOT_FOUND
    if msg then
        ngx.header["X-Message"] = msg
    end
    ngx.exit(0)
end

local function get_memc(conf)
    local memcached = require "resty.memcached"
    local memc, err = memcached:new()
    if not memc then
        ngx.log(ngx.ERR, "failed to instantiate memc: " .. err)
        return nil
    end

    memc:set_timeout(1000)

    local ok, err = memc:connect(conf['host'], conf['port'])
    if not ok then
        ngx.log(ngx.ERR, "failed to connect: " .. err)
        return nil
    end

    return memc
end

local function test()

end

-- Инициализируем memcache и зададим ключ кеширования
local result;
local memc = get_memc(conf.memcache);
local prefix, pk = ngx.var.prefix, ngx.var.pk;
local memcache_key = "/" .. prefix .. "/" .. pk;

-- Если инициализировали соединение
if memc then
    -- Проверим, есть ли в кеше по данному ключу
    result, flags, err = memc:get(memcache_key)
    if result and #result > 0 then
        return ngx.redirect(result)
    end
end

-- Если в кеше ничего нету, отправим запрос через ZeroRPC
-- Вызов в ZeroRPC не гарантирую, что не заблочит nginx
if not result then
    local http = require "zerorpc.http"
    local httpc = http.new()
    local uri = "http://" .. conf.noda['host'] .. ":" .. conf.noda['port'] .. ngx.var.uri
    local resp, err = httpc:request_uri(uri, {
        method = ngx.req.get_method(),
        body = ""
    })

    if (resp and resp.status == ngx.HTTP_OK) then
        --  and resp.location and #resp.location > 0
        -- Установим значение в memcache
        local cache_exptime = conf.exptime[prefix]
        if memc and cache_exptime then
            local ok, err = memc:set(memcache_key, resp.body, cache_exptime)
            if not ok then
                ngx.log(ngx.ERR, "failed to set : " .. err)
            end
        end

        -- Redirect на url
        return ngx.redirect(resp.body)
    else
        ngx.log(ngx.ERR, "failed to request: " .. err)
    end

--    local client = require "zerorpc.client"
--    local S = client.new("tcp://" .. conf.zerorpc['host'] .. ":" .. conf.zerorpc['port'])
--
--    local scall = function(...)
--        local r = {S:call(...)}
--        assert(r[1])
--        return select(2, unpack(r))
--    end
--
--    local resp = scall("route", {
--        api_type = ngx.req.get_method(),
--        api_method = ngx.var.uri
--    })
--    S:close()
--
--    if (resp.code == 200 and resp.location and #resp.location > 0) then
--        -- Установим значение в memcache
--        local cache_exptime = conf.exptime[prefix]
--        if memc and cache_exptime then
--            local ok, err = memc:set(memcache_key, resp.location, cache_exptime)
--            if not ok then
--                ngx.log(ngx.ERR, "failed to set : " .. err)
--            end
--        end
--
--        -- Redirect на url
--        return ngx.redirect(resp.location)
--    end
end

return_not_found()
