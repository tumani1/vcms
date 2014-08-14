local ffi = require("ffi")

ffi.cdef[[
typedef unsigned char uuid_t[16];
void uuid_generate(uuid_t out);
void uuid_unparse(const uuid_t uu, char *out);
]]

local Z_VERSION = 3
local libuuid = ffi.os == "OSX" and ffi.C or ffi.load("uuid")

local gen_uuid = function()
    local buf = ffi.new('uint8_t[16]')
    local uu = ffi.new('uint8_t[?]', 36)

    libuuid.uuid_generate(buf)
    libuuid.uuid_unparse(buf, uu)

    return ffi.string(uu, 36)
end

local new_headers = function()
  return {
    message_id = gen_uuid(),
    v = Z_VERSION,
  }
end

return {
  new_headers = new_headers,
}
