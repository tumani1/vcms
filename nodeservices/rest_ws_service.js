var http = require("http"),
    url = require("url"),
    querystring = require("querystring"),
    zerorpc = require("zerorpc"),
    formidable = require("formidable"),
    settings = require("../settings"),
    ws = require('ws');


function form_ipc_pack(pathname, headers, http_method, query_params) {
    var query_params = querystring.parse(query_params);

    return {api_method: pathname,
            api_type: http_method,
            token: headers['token'],
            x_token: headers['x-token'],
            query_params: query_params};
}

function run_server(host, port, bck_host, bck_port, heartbeat) {  // якобы общепринятое правило прятать всё в функцию
    var backend_client = new zerorpc.Client(heartbeat == undefined? {}: {heartbeatInterval: heartbeat}),
        IPC_pack;

    backend_client.connect("tcp://"+bck_host+":"+bck_port);
    var server = http.createServer(function(request, response) {
        var parsed_url = url.parse(request.url),
            pathname = parsed_url.pathname,
            query_params = parsed_url.query,
            http_method = request.method.toLowerCase(),
            headers = request.headers;

        if (["post", "put"].indexOf(http_method)>-1) {
            var form = new formidable.IncomingForm();
            IPC_pack = form_ipc_pack(pathname, headers, http_method, query_params);

            form.maxFieldsSize = 1024;  // TODO: не заваливается, если любое поле содержит больше данных
            form.maxFields = 6;
            form.parse(request, function(error, fields, files) {
                for (var field in fields) {  // заполняем IPC_pack параметрами из методов POST/PUT
                        if (!IPC_pack["query_params"].hasOwnProperty(field)) {
                            IPC_pack["query_params"][field] = fields[field];
                        }
                }
                backend_client.invoke("route", IPC_pack, function(error, res, more) {
                    if (error) {
                        console.log(error);
                        response.writeHead(404, {"Content-Type": "text/plain"});
                        response.end('Error');
                    }
                    if (!res && res != []) {
                        response.writeHead(404, {"Content-Type": "text/plain"});
                        response.end('Undefined response');
                    }
                    else if (res.hasOwnProperty('error')) {
                        var code = parseInt(res.error.code);
                        response.writeHead(code, {"Content-Type": "text/plain"});
                        response.end(res.error.message);
                    }
                    else {
                        response.writeHead(200, {"Content-Type": "application/json"});
                        response.end(JSON.stringify(res));
                    }
                });
            });
            form.on('error', function(error) {
                response.end(error.message);
            });
        }

        else {
            IPC_pack = form_ipc_pack(pathname, headers, http_method, query_params);
            backend_client.invoke("route", IPC_pack, function(error, res, more) {
                if (error) {
                    console.log(error);
                    response.writeHead(404, {"Content-Type": "text/plain"});
                    response.end('Error');
                }
                if (!res && res != []) {
                    response.writeHead(404, {"Content-Type": "text/plain"});
                    response.end('Undefined response');
                }
                else if (res.hasOwnProperty('error')) {
                    var code = parseInt(res.error.code);
                    response.writeHead(code, {"Content-Type": "text/plain"});
                    response.end(res.error.message);
                }
                else {
                    response.writeHead(200, {"Content-Type": "application/json"});
                    response.end(JSON.stringify(res));
                }
            });
        }
    });
    server.listen(port, host, function() {
       console.log("rest server runnig on "+host+":"+port);
    });

    var ws_server = new ws.Server({server: server});
    ws_server.on('connection', function(socket){
        socket.on("message", function(message){
            IPC_pack = JSON.parse(message);
            backend_client.invoke("route", IPC_pack, function(error, res, more) {
                if (!res) {
                    socket.send('Undefined response');
                }
                else if (res.hasOwnProperty('error')) {
                    socket.send(JSON.stringify({'error': res.error.code}));
                }
                else {
                    socket.send(JSON.stringify(res));
                }
            });
        });
    });
    ws_server.on('error', function(error) {
       console.error(error)
    });
}

var host = settings.NODE["rest_ws_serv"]["host"],
    port = settings.NODE["rest_ws_serv"]["port"],
    bck_host = settings.NODE["rest_ws_serv"]["backend"]["host"],
    bck_port = settings.NODE["rest_ws_serv"]["backend"]["port"],
    heartbeat = settings.HEARTBEAT;

if (settings.DEBUG) {
    run_server(host, port, bck_host, bck_port, heartbeat);
}
else {
    run_server(host, port, bck_host, bck_port);
}