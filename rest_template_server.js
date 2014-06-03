var http = require("http");
var url = require("url");
var zerorpc = require("zerorpc");


function validate(vurl) {
    // user/friends.format
    // topics/{name}/info.format
    // persons/{id}/values.format
    var re = new RegExp("^\/([a-z]{4,10})(\/[0-9]+|\/[a-z0-9]+)?\/([a-z]{4,10})$");
    if (re.test(vurl) == true) {
        
    }
}

function form_ipc_pack(purl, http_method) {
    var parsed_url = url.parse(purl, true);
    var idx = parsed_url.pathname.lastIndexOf(".");
    var api_directives = parsed_url.pathname.slice(0, idx).split("/");
    var query_params = parsed_url.query;
    var api_group = api_directives[1];
    var api_method = api_directives[2];
    if (api_directives.length > 3) {
        var id = api_directives[2];
        api_method = api_directives[3];
        query_params["id"] = id;  // id не может быть и в url, и в параметрах GET запроса одновременно
    }
    var api_format = parsed_url.pathname.slice(idx+1);

    return JSON.stringify({api_group: api_group,
                           api_method: api_method,
                           api_format: api_format,
                           http_method: http_method,
                           query_params: query_params});
}

function run_server(host, port) {  // якобы общепринятое правило прятать всё в функцию
    var client = new zerorpc.Client();
    client.connect("tcp://127.0.0.1:4242");

    var server = http.createServer(function(request, response) {
        var IPC_pack = form_ipc_pack(request.url, request.method);
        console.log("received IPC: " + IPC_pack.toString());
        client.invoke("route", IPC_pack, function(error, res, more) {
            response.writeHead(200, {"Content-Type": "text/plain"});
            response.end(res);
        });
    });
    server.listen(port, host);
    console.log("server runnig on "+host+":"+port);
}

run_server("127.0.0.1", 7777);