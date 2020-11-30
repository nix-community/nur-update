import os
import sys
import json
from urllib.request import Request, urlopen
from datetime import datetime, timedelta
from typing import Dict, Optional, Any


from flask import Flask, request

app = Flask(__name__, static_folder=None)


def api_headers() -> Dict[str, str]:
    token = app.config["GITHUB_TOKEN"]

    return {
        "Content-Type": "application/json",
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}",
    }


URL = "https://api.github.com/repos/nix-community/NUR"


def last_build_time() -> Optional[datetime]:
    url = f"{URL}/actions/runs?per_page=1&branch=master"
    app.logger.info("get latest actions: %s", url)
    req = Request(url, headers=api_headers())

    last_builds = json.loads(urlopen(req).read())

    for build in last_builds["workflow_runs"]:
        return datetime.strptime(build["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    return None


@app.route("/", methods=["GET"])
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


@app.route("/update", methods=["POST"])
def update_travis() -> Any:
    ts = last_build_time()
    if ts is not None and (ts + timedelta(minutes=5)) > datetime.utcnow():
        return "The last build was less then 5 minutes ago, try later", 429

    repo = request.args.get("repo")

    if repo is None or repo == "":
        return "repo parameter is missing", 400

    data = json.dumps({"ref": "master"})

    url = f"{URL}/actions/workflows/update.yml/dispatches"
    app.logger.info("trigger workflow update: %s", url)
    req = Request(url, headers=api_headers(), data=data.encode("utf-8"), method="POST",)
    resp = urlopen(req).read()
    assert len(resp) == 0

    return "", 204


def load_token() -> None:
    token = os.environ.get("GITHUB_TOKEN", None)
    if token is None:
        print("no GITHUB_TOKEN environment variable set", file=sys.stderr)
        sys.exit(1)
    app.config["GITHUB_TOKEN"] = token


if __name__ == "__main__":
    load_token()
    app.run()
