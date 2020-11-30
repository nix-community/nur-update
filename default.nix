with import <nixpkgs> {};
python3Packages.buildPythonApplication {
  name = "nur-update";
  src = ./.;
  propagatedBuildInputs = [
    python3Packages.flask
  ];
  checkInputs = [
    mypy python3.pkgs.black python3.pkgs.flake8 glibcLocales
  ];
  checkPhase = ''
    echo -e "\x1b[32m## run black\x1b[0m"
    LC_ALL=en_US.utf-8 black --check .
    echo -e "\x1b[32m## run flake8\x1b[0m"
    flake8 nur_update
    echo -e "\x1b[32m## run mypy\x1b[0m"
    mypy --strict nur_update
  '';
}
