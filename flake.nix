{
  description = "vectornav c++ library";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.05";
    utils.url = "github:numtide/flake-utils";
    vn_driver_lib.url = "github:RCMast3r/vn_driver_lib";
  };
  outputs = { self, nixpkgs, utils, vn_driver_lib }:
    let
      py_vn_driver_overlay = final: prev: {
        py_vn_driver = final.callPackage ./default.nix { };
      };
      
      my_overlays = [ vn_driver_lib.overlays.default py_vn_driver_overlay ];
      pkgs = import nixpkgs {
        system = "x86_64-linux";
        overlays = [ self.overlays.default ];
      };
    in
    {
      overlays.default = nixpkgs.lib.composeManyExtensions my_overlays;
      packages.x86_64-linux =
        rec {
          py_vn_driver = pkgs.py_vn_driver;
          default = py_vn_driver;
        };

      devShells.x86_64-linux.default =
        pkgs.mkShell rec {
          # Update the name to something that suites your project.
          name = "nix-devshell";
          packages = with pkgs; [
            # Development Tools
            py_vn_driver
          ];

          # Setting up the environment variables you need during
          # development.
          shellHook =
            let
              icon = "f121";
            in
            ''
              export PS1="$(echo -e '\u${icon}') {\[$(tput sgr0)\]\[\033[38;5;228m\]\w\[$(tput sgr0)\]\[\033[38;5;15m\]} (${name}) \\$ \[$(tput sgr0)\]"
            '';
        };

    };
}

