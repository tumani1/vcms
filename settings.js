var path = require('path'),
    fs = require("fs"),
    yaml = require("js-yaml");


var PROJECT_PATH = __dirname;
exports.TEMPLATES_PATH = path.join(PROJECT_PATH, 'templates');
exports.conf = function(filename) {
    return yaml.safeLoad(fs.readFileSync(path.join(exports.PROJECT_PATH, 'nodeservices', filename), 'utf8'));
};