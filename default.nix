with import <nixpkgs> {};
python3Packages.buildPythonApplication {
  name = "env";
  src = ./.;
  propagatedBuildInputs = [
    python3Packages.flask
  ];
}
