var http = require("http"),
    url = require("url"),
    querystring = require("querystring"),
    fs = require("fs"),
    path = require("path"),
    zerorpc = require("zerorpc"),
    yaml = require("js-yaml"),
    formidable = require("formidable"),
    settings = require("../settings.js");
    ws = require('ws');


function load_conf(filename) {
    return yaml.safeLoad(fs.readFileSync(path.join(settings.CONFIG_PATH, filename), 'utf8'));
}

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

function run_server(host, port) {  // якобы общепринятое правило прятать всё в функцию
    var max_KB = 4 * 1024,
        lb_conf = load_conf('zerorpc_service.yaml'),
        lb_client = new zerorpc.Client();  // клиент к балансировщику

    lb_client.connect(lb_conf["schema"]+"://"+lb_conf["host"]+":"+lb_conf["port"]);
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
            form.maxFields = 3;
            form.parse(request, function(error, fields, files) {
                for (var property in fields) {
                        if (!IPC_pack["query_params"].hasOwnProperty(property)) {
                            IPC_pack["query_params"][property] = fields[property];
                        }
                    }
                lb_client.invoke("route", IPC_pack, function(error, res, more) {
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
            lb_client.invoke("route", IPC_pack, function(error, res, more) {
                if (error) {
                    console.error(error);
                    response.end();
                }
                else {  //TODO: сделать структурный возврат ошибок с HTTP кодами
                    console.log(res);
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
            IPC_pack = JSON.parse(message)
            lb_client.invoke("route", IPC_pack, function(error, res, more) {
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

var conf = load_conf('node_service.yaml');
run_server(conf["rest_ws_serv"]["host"], conf["rest_ws_serv"]["port"]);