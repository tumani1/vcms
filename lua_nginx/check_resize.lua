local conf = require "common.config"

local access, sizes = ngx.var.access, conf.sizes[ngx.var.group]
local width, height = tonumber(ngx.var.width, nil), tonumber(ngx.var.height, nil)

if width and height and sizes then
    for k,v in pairs(sizes) do
        if (width == v[1] and height == v[2]) then
            access = 1
            break
        end
    end
end

return access
