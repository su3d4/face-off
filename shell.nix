with import <nixpkgs> { };
let
  pythonEnv = python314.withPackages (ps: [
    ps.numpy
    ps.toolz
    ps.ollama
    ps.python-lsp-server
  ]);
in
mkShell {
  packages = [
    pythonEnv

    black
    mypy

    libffi
    openssl
  ];
}
