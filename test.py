from flask import Flask
import unittest
import subprocess
from flask_jsglue import JSGlue

def runUrlFor(src, url_for):
    f = open('/tmp/test.js', 'w')
    f.write("location={host:'localhost',protocol:'http:'};" + bytes.decode(src) + ";console.log(Flask.url_for(%s))" % url_for)
    f.close()
    return bytes.decode(subprocess.check_output('node /tmp/test.js', stderr=subprocess.STDOUT, shell=True)).strip()

class FlaskJSGlueTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.jsglue = JSGlue(self.app)

        handler = lambda: "ok"
        self.app.add_url_rule('/', 'case0', handler)
        self.app.add_url_rule('/<a>', 'case1', handler)
        self.app.add_url_rule('/test/<a>', 'case2', handler)
        self.app.add_url_rule('/<int:a>/test', 'case3', handler)
        self.app.add_url_rule('/<int:a>/<int:b>', 'case4', handler)
        self.app.add_url_rule('/<a>/data', 'case5', handler)
        self.app.add_url_rule('/<b>/hello', 'case5', handler)
        self.app.add_url_rule('/<a>/data/<b>', 'case5', handler)

        self.client = self.app.test_client()

    def test_url_for_0(self):
        assert runUrlFor(self.client.get('/jsglue.js').data, "'case0'") == "/"        

    def test_url_for_1(self):
        assert runUrlFor(self.client.get('/jsglue.js').data, "'case1', {a: 3}") == "/3"        

    def test_url_for_2(self):
        assert runUrlFor(self.client.get('/jsglue.js').data, "'case2', {a: 'hello'}") == "/test/hello"        

    def test_url_for_3(self):
        assert runUrlFor(self.client.get('/jsglue.js').data, "'case3', {a: 00000}") == "/0/test"        

    def test_url_for_4(self):
        assert runUrlFor(self.client.get('/jsglue.js').data, "'case4', {a: 1, b: 9}") == "/1/9"        

    def test_url_for_5(self):
        assert runUrlFor(self.client.get('/jsglue.js').data, "'case5', {a: 1}") == "/1/data"        
        assert runUrlFor(self.client.get('/jsglue.js').data, "'case5', {b: 'hello'}") == "/hello/hello"        
        assert runUrlFor(self.client.get('/jsglue.js').data, "'case5', {a: 1, b: 9}") == "/1/data/9"        

    def test_url_for_6(self):
        assert runUrlFor(self.client.get('/jsglue.js').data, "'case0', {'_external': true}") == "http://localhost/"        
        assert runUrlFor(self.client.get('/jsglue.js').data, "'case2', {a: 'hello', '_external': true, '_scheme': 'https'}") == "https://localhost/test/hello"        
        assert runUrlFor(self.client.get('/jsglue.js').data, "'case5', {a: 1, b: 9, '_external': true}") == "http://localhost/1/data/9"        
        assert runUrlFor(self.client.get('/jsglue.js').data, "'case0', {'_anchor': 'test'}") == "/#test"        
        assert runUrlFor(self.client.get('/jsglue.js').data, "'case2', {a: 'hello', '_external': false, '_anchor': 'hello'}") == "/test/hello#hello"        
        assert runUrlFor(self.client.get('/jsglue.js').data, "'case5', {a: 1, b: 9, '_external': true, '_scheme': 'https', '_anchor': 'test'}") == "https://localhost/1/data/9#test"        




if __name__ == '__main__':
    unittest.main()
