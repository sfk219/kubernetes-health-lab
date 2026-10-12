"""Threaded standard-library HTTP server with probes and Prometheus metrics."""
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from collections import Counter
from threading import Lock
import os,json
COUNTS=Counter(); LOCK=Lock()
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path=self.path.split("?",1)[0]
        with LOCK:COUNTS[path]+=1
        if path in ("/live","/ready"):return self.reply(200,{"status":"ok"})
        if path=="/":return self.reply(200,{"service":"health-lab","environment":os.getenv("APP_ENV","local")})
        if path=="/metrics":
            with LOCK:items=list(COUNTS.items())
            lines=["# TYPE demo_http_requests_total counter"]+[f'demo_http_requests_total{{path="{k}"}} {v}' for k,v in sorted(items)]
            return self.write(200,("\n".join(lines)+"\n").encode(),"text/plain; version=0.0.4")
        return self.reply(404,{"detail":"not found"})
    def reply(self,status,value):self.write(status,json.dumps(value).encode(),"application/json")
    def write(self,status,body,mime):
        self.send_response(status);self.send_header("Content-Type",mime);self.send_header("Content-Length",str(len(body)));self.end_headers();self.wfile.write(body)
def main():ThreadingHTTPServer(("0.0.0.0",int(os.getenv("PORT","8080"))),Handler).serve_forever()
if __name__=="__main__":main()
