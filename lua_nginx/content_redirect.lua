local cjson = require "cjson"
local memcached = require "resty.memcached"

local conf = require "common.config"

local function not_found_url(memc)
    if (memc) then
        memc:set_keepalive(0, 100)
    end

    return '/error_404'
end

local function return_not_found(msg)
    ngx.status = ngx.HTTP_NOT_FOUND
    if msg then
        ngx.header["X-Message"] = msg
    end
    ngx.exit(0)
end

local function concat_url(location)
    local width, height = ngx.var.width, ngx.var.height
    if width ~= "" and height ~= "" then
        location = location .. "_" .. width .. "x" .. height
    end

    ngx.log(ngx.INFO, "URL for redirect: " .. location)
    return location
end

-- Инициализируем memcache и зададим ключ кеширования
local result
local group, pk = ngx.var.group, ngx.var.pk
local memcache_key = "/" .. group .. "/" .. pk

-- Если инициализировали соединение
local memc, err = memcached:new()
local ok, err = memc:connect(conf.memcache['host'], conf.memcache['port'])

if ok then
    -- Проверим, есть ли в кеше по данному ключу
    local result, flags, err = memc:get(memcache_key)
    if result and #result > 0 then
        memc:set_keepalive(0, 100)
        return ngx.redirect(concat_url(result))
    end
end


-- Если в кеше ничего нету, отправим запрос в API
if not result then
    local resp = ngx.location.capture("/api" .. ngx.var.uri)

    -- Проверка статуса запроса
    if (not resp or resp.status ~= ngx.HTTP_OK) then
        ngx.log(ngx.ERR, "Recieved failed to request")
        return not_found_url(memc)
    end

    local location
    local inner_empty = false
    local result = cjson.new().decode(resp.body)

    if (result and result.location) then
        location = result.location
        if (#location > 0) then
            location = result.location
        else
            ngx.log(ngx.ERR, "Recieved empty result")
            return not_found_url(memc)
        end

        if (result.empty) then
            inner_empty = true
        end
    else
        ngx.log(ngx.ERR, "Error json convert")
        return not_found_url(memc)
    end

    --Установка значения в memcache
    local cache_exptime = conf.exptime[group]
    -- and not inner_empty
    if memc and cache_exptime then
        local ok, err = memc:set(memcache_key, location, cache_exptime)
        if not ok then
            ngx.log(ngx.ERR, "Failed to set memcache: " .. err)
        end

        -- memc:close()
    end

    -- Перенаправление на url
    return ngx.redirect(concat_url(location))

else
    ngx.log(ngx.ERR, "Error in lua application")
    return not_found_url(memc)
end
