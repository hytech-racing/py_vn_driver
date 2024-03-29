{

  description = "vectornav driver flake";
  inputs = {
    vn_driver_lib.url = "github:RCMast3r/vn_driver_lib";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-23.11";
    flake-utils.url = "github:numtide/flake-utils";
    asyncudp.url = "github:RCMast3r/asyncudp_nix";
    hytech_data_acq.url = "github:RCMast3r/data_acq/vectornav";
  };

  outputs = { self, nixpkgs, hytech_data_acq, vn_driver_lib, asyncudp, flake-utils }@inputs:
    flake-utils.lib.eachSystem [ "x86_64-linux" "aarch64-darwin" "x86_64-darwin" "aarch64-linux" ] (system:
      let
        vn_udp_driver_overlay = final: prev: {
          vn_udp_driver_pkg = final.callPackage ./default.nix { };
        };

        my_overlays = [
          vn_udp_driver_overlay
          vn_driver_lib.overlays.default
        ] ++ hytech_data_acq.overlays.x86_64-linux;


        pkgs = import nixpkgs {
          overlays = my_overlays;
          inherit system;
        };


        shared_shell = pkgs.mkShell rec {
          name = "nix-devshell";
          packages = with pkgs; [
            vn_udp_driver_pkg
          ];
          shellHook =
            let icon = "f121";
            in ''
              export PS1="$(echo -e '\u${icon}') {\[$(tput sgr0)\]\[\033[38;5;228m\]\w\[$(tput sgr0)\]\[\033[38;5;15m\]} (${name}) \\$ \[$(tput sgr0)\]"
            '';
        };
      in
      {
        overlays = my_overlays;
        devShells.default = shared_shell;

        packages = rec {
          default = pkgs.vn_udp_driver_pkg;
        };
      }
    );
}
