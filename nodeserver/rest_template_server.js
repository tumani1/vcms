var http = require("http");
var zerorpc = require("zerorpc");
var url = require("url");
var querystring = require("querystring");
var log = console.log;


function validate(vurl) {
    var re = new RegExp("^\/([a-z]{4,10})(\/[0-9]+|\/[a-z0-9]+)?\/([a-z]{4,10})$");
    return re.exec(vurl);  // длинна массива соотвествует количеству групп в regexp +1
}

function form_ipc_pack(directives, method, query_params) {
    var qp = querystring.parse(query_params);
    qp["ident"] = (directives[2] ? directives[2].slice(1) : null);

    return {api_group: directives[1],
            api_method: directives[3],
            http_method: method,
            query_params: qp};
}

function run_server(host, port) {  // якобы общепринятое правило прятать всё в функцию
    var client = new zerorpc.Client();
    client.connect("tcp://127.0.0.1:4242");

    var server = http.createServer(function(request, response) {
        var parsed = url.parse(request.url);
        var vurl = parsed.pathname, query_params = parsed.query;
        var meth = request.method;
        var directives = validate(vurl);
        var IPC_pack;
        if (meth in ["POST", "PUT"] && directives != null) {
            IPC_pack = form_ipc_pack(directives, meth, query_params);
            log("received IPC: " + IPC_pack.toString());
            request.on('data', function(chunk) {
                IPC_pack["query_params"] = null;
                client.invoke("route", IPC_pack, function(error, res, more) {
                    response.writeHead(200, {"Content-Type": "text/plain"});
                    response.end(res);
                })
            });
        }
        else if (directives != null) {
            IPC_pack = form_ipc_pack(directives, meth, query_params);
            log("received IPC: " + IPC_pack.toString());
            client.invoke("route", IPC_pack, function(error, res, more) {
                response.writeHead(200, {"Content-Type": "text/plain"});
                response.end(res);
            });
        }
        else {
            log("invalid url");
            response.writeHead(404, {"Content-Type": "text/plain"});
            response.end("invalid url");
        }
        });
    server.listen(port, host);
    log("server runnig on "+host+":"+port);
}

run_server("127.0.0.1", 7777);