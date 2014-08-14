local client = require "zerorpc.client"
local S = client.new("tcp://192.168.1.104:6700")

local scall = function(...)
    local r = {S:call(...)}
    assert(r[1])
    return select(2, unpack(r))
end

local resp = scall("content_route", {
    api_type = ngx.req.get_method(),
    api_method = ngx.var.uri
})
S:close()

if (resp.code == 200 and resp.location and #resp.location > 0) then
    return ngx.redirect(resp.location)
end

ngx.status = ngx.HTTP_NOT_FOUND
ngx.exit(0)
