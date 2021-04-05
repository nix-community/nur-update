with import <nixpkgs> { };
let
  python = python39;
in
python.pkgs.buildPythonApplication {
  name = "nur-update";
  src = ./.;
  propagatedBuildInputs = [
    python.pkgs.flask
  ];
  checkInputs = [
    mypy
    python.pkgs.black
    python.pkgs.flake8
    glibcLocales
  ];
  checkPhase = ''
    echo -e "\x1b[32m## run black\x1b[0m"
    black --version
    LC_ALL=en_US.utf-8 black --check .
    echo -e "\x1b[32m## run flake8\x1b[0m"
    flake8 --version
    flake8 nur_update
    echo -e "\x1b[32m## run mypy\x1b[0m"
    mypy --version
    mypy --strict nur_update
  '';
}
