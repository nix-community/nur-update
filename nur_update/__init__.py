import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Optional, Any


from flask import Flask, request
from github import Github, Auth
from github.Branch import Branch

app = Flask(__name__, static_folder=None)


def get_auth() -> Auth.Auth:
    token = os.environ.get("GITHUB_TOKEN", None)
    if token is not None:
        return Auth.Token(token)

    private_key = os.environ.get("GITHUB_APP_PRIVATE_KEY", None)
    app_id = os.environ.get("GITHUB_APP_ID", None)
    installation_id = os.environ.get("GITHUB_APP_INSTALLATION_ID", None)
    if private_key is not None and app_id is not None and installation_id is not None:
        appauth = Auth.AppAuth(app_id, private_key)
        return appauth.get_installation_auth(int(installation_id))
    else:
        print(
            "either the GITHUB_TOKEN environment variable or the GITHUB_APP_{PRIVATE_KEY,APP_ID,INSTALLATION_ID} environment variables must be set",
            file=sys.stderr,
        )
        sys.exit(1)


nur_repo = Github(auth=get_auth()).get_repo("nix-community/NUR")
nur_default_branch: Branch = nur_repo.get_branch("main")


def last_build_time() -> Optional[datetime]:
    last_builds = nur_repo.get_workflow_runs(branch=nur_default_branch).get_page(0)
    app.logger.info("get latest actions: %s", nur_repo.url)

    for build in last_builds:
        return build.created_at
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
    if ts is not None and (ts + timedelta(minutes=5)) > datetime.now(timezone.utc):
        return "The last build was less then 5 minutes ago, try later", 429

    repo = request.args.get("repo")

    if repo is None or repo == "":
        return "repo parameter is missing", 400

    workflow = nur_repo.get_workflow("update.yml")
    workflow.create_dispatch(ref=nur_default_branch)
    app.logger.info("trigger workflow update: %s", workflow.url)

    return "", 204


def main() -> None:
    app.run()


if __name__ == "__main__":
    main()
