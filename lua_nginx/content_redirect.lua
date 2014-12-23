local conf = require "common.config"
local not_found_url = '/error_404'

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
        ngx.log(ngx.ERR, "Failed to init memc: " .. err)
        return nil
    end

    memc:set_timeout(1000)

    local ok, err = memc:connect(conf['host'], conf['port'])
    if not ok then
        ngx.log(ngx.ERR, "Failed to connect memcache: " .. err)
        return nil
    end

    return memc
end

local function concat_url(location)
    local width, height = ngx.var.width, ngx.var.height
    if width and height and width ~= "" and height ~= "" then
        location = location .. "_" .. width .. "x" .. height
    end
    ngx.log(ngx.INFO, "URL for redirect: " .. location)
    return location
end

-- Инициализируем memcache и зададим ключ кеширования
local result
local memc = get_memc(conf.memcache)
local group, pk = ngx.var.group, ngx.var.pk
local memcache_key = "/" .. group .. "/" .. pk

-- Если инициализировали соединение
if memc then
    -- Проверим, есть ли в кеше по данному ключу
    result, flags, err = memc:get(memcache_key)
    if result and #result > 0 then
        return ngx.redirect(concat_url(result))
    end
end

-- Если в кеше ничего нету, отправим запрос в API
if not result then
    local http = require "common.http"
    local httpc = http.new()

    local uri = "http://" .. conf.noda['host'] .. ":" .. conf.noda['port'] .. ngx.var.uri
    local resp, err = httpc:request_uri(uri, {
        method = ngx.req.get_method(),
        body = ""
    })

    -- Проверка статуса запроса
    if (not resp or resp.status ~= ngx.HTTP_OK) then
        ngx.log(ngx.ERR, "Recieved failed to request")
        return not_found_url
    end

    local location
    local inner_empty = false
    local json = require "cjson"
    local result = json.decode(resp.body)

    if (result and result.location) then
        if (result.empty) then
            inner_empty = true
        end

        location = result.location
        if (#location > 0) then
            location = result.location
        else
            ngx.log(ngx.ERR, "Recieved empty result")
            return not_found_url
        end
    else
        ngx.log(ngx.ERR, "Error json convert")
        return not_found_url
    end

    --Установка значения в memcache
    local cache_exptime = conf.exptime[group]
    if memc and cache_exptime and not inner_empty then
        local ok, err = memc:set(memcache_key, location, cache_exptime)
        if not ok then
            ngx.log(ngx.ERR, "Failed to set memcache: " .. err)
        end
    end

    -- Перенаправление на url
    return ngx.redirect(concat_url(location))

else
    ngx.log(ngx.ERR, "Error in lua application")
    return not_found_url
end
