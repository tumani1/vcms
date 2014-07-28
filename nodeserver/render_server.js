var http  = require("http"),
    url = require("url"),
    path = require("path"),
    jade = require("jade"),
    settings = require("../settings"),
    sdk = require(__dirname+"/sdk");

var jade_templates = {
    "/": "index.jade",
    "/index/": "index.jade"
};

function run_server(host, port) {
    var server = http.createServer(function(request, response) {
        var status = 200,
            head_obj = {"Content-Type": "text/html"};
        if (request.method === "GET") {
            var parsed = url.parse(request.url);
            var tmpl_name = jade_templates[parsed.pathname];
            if (tmpl_name) {
                jade.renderFile(path.join(settings.TEMPLATES_PATH, tmpl_name), function (error, html) {
                    if (error) {
                        status = 500;
                        response.end()
                    }
                    else{
                        head_obj["Content-Length"] = html.length;
                        response.end(html);
                    }
                });
            }
            else{
                status = 404;
            }
        }
        response.writeHead(status, head_obj);
        console.log("["+(new Date())+"] "+response.statusCode+' "'+request.method+' '+request.url+'"');
    });
    server.listen(port, host);
    console.log("["+(new Date())+"]"+" render server runnig on "+host+":"+port);
}

var conf = settings.conf('node_service.yaml');
run_server(conf["render_serv"]["host"], conf["render_serv"]["port"]);