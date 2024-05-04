# NUR update endpoint

Notify NUR to check for an update of a repository.
This will update `repos.json.lock` in the [NUR](https://github.com/nix-community/NUR) repository if a new version is found.

## API

```
POST https://nur-update.nix-community.org/update?repo=<REPO_NAME>
```

NOTE: Also we check all repositories at the moment independent of the `repo`
parameter, this is likely to change in future.

## Example

```console
$ curl -XPOST https://nur-update.nix-community.org/update?repo=mic92
```

## Run the service yourself

1. Get the github api token of your repository from https://github.com/settings/tokens that has the workflow scope checked.
2. Start the service: `GITHUB_TOKEN=<TOKEN_FROM_PREVIOUS_COMMAND> python nur_update/__init__.py`
