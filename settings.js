var path = require('path'),
    fs = require("fs"),
    yaml = require("js-yaml"),
    PROJECT_PATH = __dirname;

exports.CONFIG_PATH = path.join(PROJECT_PATH, 'configs');
exports.TEMPLATES_PATH = path.join(PROJECT_PATH, 'templates');
exports.conf = function(filename) {
    return yaml.safeLoad(fs.readFileSync(path.join(exports.CONFIG_PATH, filename), 'utf8'));
};