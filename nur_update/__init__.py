import os
import sys
import json
from urllib.request import Request, urlopen
from datetime import datetime, timedelta
from typing import Dict, Optional, Any

from flask import Flask, request

app = Flask(__name__, static_folder=None)


def api_headers() -> Dict[str, str]:
    token = app.config['TRAVIS_TOKEN']

    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Travis-API-Version": "3",
        "Authorization": f"token {token}",
    }


URL = "https://api.travis-ci.com/repo/nix-community%2FNUR"


def last_build_time() -> Optional[datetime]:
    req = Request(f"{URL}/builds?limit=10", headers=api_headers())

    last_builds = json.loads(urlopen(req).read())

    for build in last_builds["builds"]:
        if build["event_type"] == "api":
            return datetime.strptime(build["updated_at"],
                                     "%Y-%m-%dT%H:%M:%S.%fZ")
    return None


@app.route('/', methods=["GET"])
def index() -> Any:
    return f"""
<html>
  <head>
    <title>NUR update endpoint</title>
  </head>
  <body>
    <h1>NUR update endpoint</h1>
    <p>
      <h2>Usage</h2>
      <code>
      POST {request.url_root}update?repo=&lt;REPO_NAME&gt;
      </code>
    </p>
    <p>
      <h2>Example</h2>
      <code>
      $ curl -XPOST {request.url_root}update?repo=mic92
      </code>
    </p>
    <p>
      <h2>Source code</h2>
      Source code can be found on <a href="https://github.com/nix-community/nur-update">github</a>
    </p>
  </body>
</html>
"""


@app.route('/update', methods=["POST"])
def update_travis() -> Any:
    ts = last_build_time()
    if ts is not None and (ts + timedelta(minutes=5)) > datetime.utcnow():
        return "The last build was less then 5 minutes ago, try later", 429

    repo = request.args.get('repo')

    if repo is None or repo == "":
        return "repo parameter is missing", 400

    data = json.dumps({
        "request": {
            "message": "requested rebuild",
            "branch": "master"
        }
    })

    req = Request(
        f"{URL}/requests",
        headers=api_headers(),
        data=data.encode("utf-8"),
        method="POST")

    return urlopen(req).read()


def load_token() -> None:
    token = os.environ.get("TRAVIS_TOKEN", None)
    if token is None:
        print("no TRAVIS_TOKEN environment variable set", file=sys.stderr)
        sys.exit(1)
    app.config['TRAVIS_TOKEN'] = token


load_token()

if __name__ == '__main__':
    app.run()
