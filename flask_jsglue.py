import re
import json
import urllib.request
import os
from markupsafe import Markup
from flask import render_template, make_response, url_for, current_app

JSGLUE_JS_PATH = '/jsglue.js'
JSGLUE_NAMESPACE = 'Flask'
rule_parser = re.compile(r'<(.+?)>')
splitter = re.compile(r'<.+?>')

def download_js():
    try:
        source = 'https://raw.githubusercontent.com/stewartpark/Flask-JSGlue/master/templates/jsglue/js_bridge.js'
        target_dir = os.path.join(current_app.root_path, current_app.template_folder, 'jsglue')
        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
        target = os.path.join(target_dir, 'js_bridge.js')
        urllib.request.urlretrieve(source, target)
    except Exception as e:
        # print(str(e))  # DEBUG
        pass

def get_routes(app):
    output = []
    for r in app.url_map.iter_rules():
        endpoint = r.endpoint
        if app.config['APPLICATION_ROOT'] == '/' or\
                not app.config['APPLICATION_ROOT']:
            rule = r.rule
        else:
            rule = '{root}{rule}'.format(
                root=app.config['APPLICATION_ROOT'],
                rule=r.rule
            )
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
        namespace = JSGLUE_NAMESPACE
        rules = json.dumps(rules)
        template = 'jsglue/js_bridge.js'
        try:
            return render_template(template, namespace=namespace, rules=rules)
        except:
            download_js()
            return render_template(template, namespace=namespace, rules=rules)

    @staticmethod
    def include():
        js_path = url_for('serve_js')
        return Markup('<script src="%s" type="text/javascript"></script>') % (js_path,)
