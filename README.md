# NUR update endpoint

[![Build Status](https://travis-ci.org/nix-community/nur-update.svg?branch=master)](https://travis-ci.org/nix-community/nur-update)

Notify NUR to check for an update of a repository.
This will update `repos.json.lock` in the [NUR](https://github.com/nix-community/NUR) repository if a new version is found.

## API

```
POST https://nur-update.herokuapp.com/update?repo=<REPO_NAME>
```

NOTE: Also we check all repositories at the moment independent of the `repo`
parameter, this is likely to change in future.

## Example

```console
$ curl -XPOST https://nur-update.herokuapp.com/update?repo=mic92
```

## Run the service yourself

1. Get the travis api token of your repository `travis token --pro`
2. Start the service: `TRAVIS_TOKEN=<TOKEN_FROM_PREVIOUS_COMMAND> python nur_update/__init__.py`

## Roadmap

Add webhook support for github/gitlab and co.
