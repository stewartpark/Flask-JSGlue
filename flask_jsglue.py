from flask import current_app, make_response
from jinja2 import Markup
import re, json
   
JSGLUE_JS_PATH = '/jsglue.js'
JSGLUE_NAMESPACE = 'Flask'
rule_parser = re.compile(r'<(.+?)>')
splitter = re.compile(r'<.+?>')

def get_routes(app):
    output = []
    for r in app.url_map.iter_rules():
        endpoint = r.endpoint
        rule = r.rule
        rule_args = [x.split(':')[-1] for x in rule_parser.findall(rule)]
        rule_tr = splitter.split(rule)
        output.append((endpoint, rule_tr, rule_args))
    return sorted(output, key=lambda x: len(x[1]), reverse=True)

class JSGlue(object):
    def __init__(self, app=None, **kwargs):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        @app.route(JSGLUE_JS_PATH)
        def serve_js():
            return make_response(
                (self.generate_js(), 200, {'Content-Type': 'text/javascript'})
            )
        @app.context_processor
        def context_processor():
            return {'JSGlue': JSGlue}

    def generate_js(self):
        rules = get_routes(self.app)
        return """
var %s = new (function(){ return {
        // Internal data
        '_endpoints': %s,

        // Public methods
        'url_for': function(endpoint, rule) {
            var has_everything, url;

            for(var i in this._endpoints) {
                if(endpoint == this._endpoints[i][0]) {
                    url = ''; j = 0; has_everything = true;
                    for(var j = 0; j < this._endpoints[i][2].length; j++) {
                        t = rule[this._endpoints[i][2][j]];
                        if(t == undefined) {
                            has_everything = false;
                            break;
                        }
                        url += this._endpoints[i][1][j] + t;
                    }
                    if(has_everything) {
                        if(this._endpoints[i][2].length != this._endpoints[i][1].length) 
                            url += this._endpoints[i][1][j];
                        return url;
                    }
                }
            }                

            throw("Couldn't find the matching endpoint.");
        }
};});""" % (JSGLUE_NAMESPACE, json.dumps(rules)) 

    @staticmethod
    def include():
        return Markup('<script src="%s" type="text/javascript"></script>' % (JSGLUE_JS_PATH, ))
