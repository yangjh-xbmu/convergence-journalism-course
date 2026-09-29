"""Serve the built slides locally; no internet, Node.js, or third-party Python packages needed."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import webbrowser


def main() -> None:
    parser = argparse.ArgumentParser(description="离线课件本地播放器（需要 Python 3）")
    parser.add_argument("--root", default=".", help="相对本脚本的课件目录")
    parser.add_argument("--port", type=int, default=0, help="默认自动选择空闲端口")
    parser.add_argument("--no-open", action="store_true", help="不自动打开浏览器")
    args = parser.parse_args()
    root = (Path(__file__).resolve().parent / args.root).resolve()
    if not (root / "index.html").is_file():
        parser.error(f"未找到已构建课件：{root / 'index.html'}")
    handler = partial(SimpleHTTPRequestHandler, directory=str(root))
    with ThreadingHTTPServer(("127.0.0.1", args.port), handler) as server:
        url = f"http://127.0.0.1:{server.server_port}/"
        print(f"Serving offline slides at {url}", flush=True)
        print("仅监听本机；关闭此窗口或按 Ctrl+C 停止。", flush=True)
        if not args.no_open:
            webbrowser.open(url)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
