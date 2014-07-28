var http = require("http"),
    url = require("url"),
    querystring = require("querystring"),
    zerorpc = require("zerorpc"),
    formidable = require("formidable"),
    settings = require("../settings"),
    ws = require('ws');

function validate(vurl) {
    // user/friends
    // topics/{name}/info
    // persons/{id}/values
    var re = new RegExp("^\/([a-z]{4,10})(\/[0-9]+|\/[a-z0-9]+)?\/([a-z]{4,10})$");
    return re.exec(vurl);  // длинна массива соотвествует количеству групп в regexp +1
}

function form_ipc_pack(directives, headers, method, query_params) {
    /*Список групп методов API проекта:
     [auth, user, topics,
      media, content, persons,
      stream, chat, users,
      mediaunits, msgr]
    Хитро формируем параметр из первой и второй групп регулярного выражения, удаляя начальный слэш у второй группы
    и последнюю букву s у первой группы, если она присутствует. Это необходимо для правльной передачи в API методы.
    */
    var qp = querystring.parse(query_params);
    if (directives[2]) {
        var k = directives[1].match('(.*[^s])')[0];
        qp[k] = directives[2].slice(1);
    }

    return {api_group: directives[1],
            api_method: directives[3],
            http_method: method,
            token: headers['token'],
            x_token: headers['x-token'],
            query_params: qp};
}

function run_server(host, port, bck_host, bck_port, heartbeat) {  // якобы общепринятое правило прятать всё в функцию
    var max_KB = 4 * 1024;
    var backend_client = new zerorpc.Client(heartbeat == undefined? {}: {heartbeatInterval: heartbeat})

    backend_client.connect("tcp://"+bck_host+":"+bck_port);
    var server = http.createServer(function(request, response) {
        var parsed = url.parse(request.url),
            vurl = parsed.pathname, query_params = parsed.query,
            meth = request.method.toLowerCase(),
            directives = validate(vurl),
            IPC_pack;
            headers = request.headers;

        if (["post", "put"].indexOf(meth)>-1 && directives != null) {
            var form = new formidable.IncomingForm();
            IPC_pack = form_ipc_pack(directives, headers, meth, query_params);

            form.maxFieldsSize = 1024;  // TODO: не заваливается, если любое поле содержит больше данных
            form.maxFields = 6;
            form.parse(request, function(error, fields, files) {
                for (var property in fields) {
                        if (!IPC_pack["query_params"].hasOwnProperty(property)) {
                            IPC_pack["query_params"][property] = fields[property];
                        }
                    }
                backend_client.invoke("route", IPC_pack, function(error, res, more) {
                    response.writeHead(200, {"Content-Type": "text/plain"});
                    response.end(JSON.stringify(res));
                });
            });
            form.on('error', function(error) {
                response.end(error.message);
            });
        }

        else if (directives != null) {
            IPC_pack = form_ipc_pack(directives, headers, meth, query_params);
            backend_client.invoke("route", IPC_pack, function(error, res, more) {
                if (error) {
                    console.error(error);
                    response.end();
                }
                else {  //TODO: сделать структурный возврат ошибок с HTTP кодами
                    response.writeHead(200, {"Content-Type": "text/plain"});
                    response.end(JSON.stringify(res));
                }
            });
        }

        else {
            response.writeHead(404, {"Content-Type": "text/plain"});
            response.end("invalid url");
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
                if (error){
                    console.error(error);
                    return;
                }
                socket.send(JSON.stringify(res));
            });
        });
    });
    ws_server.on('error', function(error){
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
