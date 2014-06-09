var http = require("http"),
    url = require("url"),
    querystring = require("querystring"),
    fs = require("fs"),
    path = require("path"),
    zerorpc = require("zerorpc"),
    yaml = require("js-yaml"),
    formidable = require("formidable"),
    log = console.log;


function load_conf(filename) {
    return yaml.safeLoad(fs.readFileSync(path.resolve(__dirname, filename), 'utf8'));
}

function validate(vurl) {
    // user/friends
    // topics/{name}/info
    // persons/{id}/values
    var re = new RegExp("^\/([a-z]{4,10})(\/[0-9]+|\/[a-z0-9]+)?\/([a-z]{4,10})$");
    return re.exec(vurl);  // длинна массива соотвествует количеству групп в regexp +1
}

function form_ipc_pack(directives, method, query_params) {
    /*Список групп методов API проекта:
     [auth, user, topics,
      media, content, persons,
      stream, chat, users,
      mediaunits, msgr]
    Хитро формируем параметр из первой и второй групп регулярного выражения, удаляя начальный слэш у второй группы
    и последнюю букву s у первой группы, если она присутствует. Это необходимо для правльной перелачи в API методы.
    */
    var qp = querystring.parse(query_params);
    if (directives[2]) {
        var k = directives[1].match('(.*[^s])')[0];
        qp[k] = directives[2].slice(1);
    }

    return {api_group: directives[1],
            api_method: directives[3],
            http_method: method,
            token: 'echo_token', //TODO сделать парсинг заголовка токена
            query_params: qp};
}

function run_server(host, port) {  // якобы общепринятое правило прятать всё в функцию
    var max_KB = 4 * 1024,
        services = load_conf('../configs/zerorpc_services.yaml'),
        zero_clients = [];  // клиенты, по которым настраивать балансировку
    for (var s=0;s<services.length;s++) {
        var cl =  new zerorpc.Client();
        cl.connect(services[s]["schema"]+"://"+services[s]["host"]+":"+services[s]["port"]);
        zero_clients.push(cl);
    }

    var server = http.createServer(function(request, response) {
        var parsed = url.parse(request.url),
            vurl = parsed.pathname, query_params = parsed.query,
            meth = request.method.toLowerCase(),
            directives = validate(vurl),
            IPC_pack;

        if (["post", "put"].indexOf(meth)>-1 && directives != null) {
            var all_data = '',
                form = new formidable.IncomingForm();
            IPC_pack = form_ipc_pack(directives, meth, query_params);
            log("received IPC: " + JSON.stringify(IPC_pack));

            form.maxFields = 1;
            form.maxFieldsSize = max_KB;
            form.parse(request, function(error, fields, files) {
                log(fields);
                for (var property in fields) {
                        if (!IPC_pack["query_params"].hasOwnProperty(property)) {
                            IPC_pack["query_params"][property] = fields[property];
                        }
                    }
                zero_clients[0].invoke("route", IPC_pack, function(error, res, more) {
                    response.writeHead(200, {"Content-Type": "text/plain"});
                    response.end(JSON.stringify(res));
                });
            });





//            request.on('data', function(chunk) {
//                /*накапливание данных, потому как ответ может придти за раз неполностью*/
//                log(chunk.length);
//                log(chunk.toString());
//                all_data += chunk;
//            });
//
//            request.on("end", function() {
//                if (all_data.length < max_KB) {
//                    all_data = formidable();
//                    all_data = JSON.parse(all_data.toString()); //TODO: ломается на невалидных данных
//                    for (var attrname in all_data) {
//                        IPC_pack["query_params"][attrname] = all_data[attrname];
//                    }
//                    zero_clients[0].invoke("route", IPC_pack, function(error, res, more) {
//                        response.writeHead(200, {"Content-Type": "text/plain"});
//                        response.end(res);
//                    });
//                }
//                else {
//                    response.writeHead(400, {"Content-Type": "text/plain"});
//                    response.end("too large request");
//                }
//            })
        }

        else if (directives != null) {
            IPC_pack = form_ipc_pack(directives, meth, query_params);
            log("received IPC: " + JSON.stringify(IPC_pack));
            zero_clients[0].invoke("route", IPC_pack, function(error, res, more) {
                response.writeHead(200, {"Content-Type": "text/plain"});
                response.end(JSON.stringify(res));
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

var conf = load_conf('../configs/node_service.yaml');
run_server(conf["host"], conf["port"]);