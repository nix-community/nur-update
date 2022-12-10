{ buildPythonApplication, black, flake8, flask, mypy }:

buildPythonApplication {
  name = "nur-update";
  src = ./.;
  propagatedBuildInputs = [
    flask
  ];
  checkInputs = [
    mypy
    black
    flake8
  ];
  checkPhase = ''
    echo -e "\x1b[32m## run black\x1b[0m"
    black --version
    black --check .
    echo -e "\x1b[32m## run flake8\x1b[0m"
    flake8 --version
    flake8 nur_update
    echo -e "\x1b[32m## run mypy\x1b[0m"
    mypy --version
    mypy --strict nur_update
  '';
}
