import os
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from urllib.request import Request, urlopen

RPC_URL = os.getenv("SOLANA_RPC_URL", "https://api.mainnet-beta.solana.com")
RENO_MINT = os.getenv("RENO_MINT", "BrEiwuaLCuG7nG9bMuDg9ihp6sisvD6DCqNjrudHxmzg")


class Handler(BaseHTTPRequestHandler):
    def _write(self, code, body, content_type="text/plain; charset=utf-8", extra_headers=None):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        if extra_headers:
            for k, v in extra_headers.items():
                self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def do_GET(self):
        path = urlparse(self.requestline.split(" ")[1])
        if path.path == "/reno/total-supply":
            try:
                qs = parse_qs(path.query)
                mint = (qs.get("mint", [RENO_MINT])[0]).strip()
                mode = (qs.get("mode", ["ui"])[0]).lower()  

                body = json.dumps({
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "getTokenSupply",
                    "params": [mint],
                }).encode("utf-8")

                req = Request(RPC_URL, data=body, headers={"Content-Type": "application/json"})
                with urlopen(req, timeout=10) as resp:
                    data = json.loads(resp.read().decode("utf-8"))

                v = data["result"]["value"]
                if mode == "raw":
                    out = v["amount"] 
                elif mode == "decimals":
                    out = str(v["decimals"])
                else:
                    out = v.get("uiAmountString") or str(v.get("uiAmount"))

                if out is None:
                    raise ValueError("empty output")

                self._write(200, str(out), extra_headers={
                    "Cache-Control": "public, max-age=15, s-maxage=30, stale-while-revalidate=60"
                })
            except Exception:
                self._write(200, "0")
            return

        if path.path == "/health":
            self._write(200, "ok")
            return

        self._write(404, "not found")


def main():
    server = HTTPServer(("127.0.0.1", 8000), Handler)
    server.serve_forever()


if __name__ == "__main__":
    main()