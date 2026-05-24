{
  buildPythonApplication,
  flask,
  gunicorn,
  mypy,
  pygithub,
  ruff,
  setuptools,
}:

buildPythonApplication {
  name = "nur-update";
  pyproject = true;
  src = ./.;
  build-system = [ setuptools ];
  dependencies = [
    flask
    gunicorn
    pygithub
  ];
  nativeCheckInputs = [
    mypy
    ruff
  ];
  checkPhase = ''
    echo -e "\x1b[32m## run ruff\x1b[0m"
    ruff --version
    ruff check
    ruff format --check
    echo -e "\x1b[32m## run mypy\x1b[0m"
    mypy --version
    mypy --strict nur_update
  '';
}
