{ pkgs ? import <nixpkgs> { } }:
let
  myAppEnv = pkgs.poetry2nix.mkPoetryEnv {
    projectDir = ./.;
    python = pkgs.python38;
  };
in
myAppEnv.env.overrideAttrs (oldAttrs: {
  buildInputs = with pkgs; [
    poetry
    nodejs-16_x
    google-cloud-sdk
    kubectl
    argo
    argocd
    terraform
  ];
})
