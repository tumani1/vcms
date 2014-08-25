local conf = require "common.config";

local width, height = ngx.var.width, ngx.var.height
local access, prefix =  ngx.var.access, ngx.var.prefix

if not (width and height) or width == "" or height == "" then
    return 1;
end

width, height = tonumber(width, nil), tonumber(height, nil)
if conf.sizes[prefix] then
    for k,v in pairs(conf.sizes[prefix]) do
        if (width == v[1] and height == v[2]) then
            access = 1;
            break;
        end
    end
end

return access;
