var http  = require("http"),
    url = require("url"),
    fs = require("fs"),
    path = require("path"),
    yaml = require("js-yaml"),
    jade = require("jade"),
    settings = require("../settings.js");


function load_conf(filename) {
    return yaml.safeLoad(fs.readFileSync(path.join(settings.CONFIG_PATH, filename), 'utf8'));
}

function run_server(host, port) {
    var server = http.createServer(function(request, response) {
        if (request.method === "GET") {
            var parsed = url.parse(request.url);
            if (parsed.pathname === "/index.html") {
                  //асинхронно
//                fs.readFile(path.join(settings.TEMPLATES_PATH, 'index.jade'), {encoding: 'utf8'}, function(error, data) {
//                    var html = jade.render(data);
//                    response.end(html);
//                });

                  //синхронно
                jade.renderFile(path.join(settings.TEMPLATES_PATH, 'index.jade'), function(error, html) {
                    response.end(html);
                });
                response.end();
            }
        }
    });
    server.listen(port, host);
    console.log("render server runnig on "+host+":"+port);
}

var conf = load_conf('node_service.yaml');
run_server(conf["render_serv"]["host"], conf["render_serv"]["port"]);