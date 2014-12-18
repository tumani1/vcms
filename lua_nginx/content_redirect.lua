local conf = require "common.config";

local function return_not_found(msg)
    ngx.status = ngx.HTTP_NOT_FOUND;
    if msg then
        ngx.header["X-Message"] = msg;
    end
    ngx.exit(0)
end

local function get_memc(conf)
    local memcached = require "resty.memcached";
    local memc, err = memcached:new();
    if not memc then
        ngx.log(ngx.ERR, "Failed to init memc: " .. err)
        return nil
    end

    memc:set_timeout(1000)

    local ok, err = memc:connect(conf['host'], conf['port']);
    if not ok then
        ngx.log(ngx.ERR, "Failed to connect memcache: " .. err)
        return nil
    end

    return memc
end

local function concat_url(location)
    local width, height = ngx.var.width, ngx.var.height;
    if width and height and width ~= "" and height ~= "" then
        location = location .. "_" .. width .. "x" .. height;
    end
    ngx.log(ngx.INFO, "URL for redirect: " .. location);
    return location;
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
        return_not_found()
    end

    local location;
    local json = require "cjson"
    local result = json.decode(resp.body)

    if (result and result.location) then
        location = result.location;
        if (#location > 0) then
            location = result.location
        else
            ngx.log(ngx.ERR, "Recieved empty result")
            return_not_found()
        end
    else
        ngx.log(ngx.ERR, "Error json convert")
        return_not_found()
    end

    --Установка значения в memcache
    local cache_exptime = conf.exptime[prefix]
    if memc and cache_exptime then
        local ok, err = memc:set(memcache_key, location, cache_exptime)
        if not ok then
            ngx.log(ngx.ERR, "Failed to set memcache: " .. err)
        end
    end

    -- Перенаправление на url
    return ngx.redirect(concat_url(location))

else
    ngx.log(ngx.ERR, "Error in lua applivation")
    return_not_found()
end
