{

  description = "Service to trigger updates of the NUR repository";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable-small";
  outputs = { self, nixpkgs }: {
    packages.x86_64-linux.nur-update = nixpkgs.legacyPackages.x86_64-linux.python3.pkgs.callPackage ./. { };
    packages.x86_64-linux.default = self.packages.x86_64-linux.nur-update;
  };
}
