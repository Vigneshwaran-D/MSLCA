{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.virtualenv
    pkgs.sqlite
    pkgs.gcc
    pkgs.pkg-config
  ];
}

