# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.245.2/containers/debian/.devcontainer/base.Dockerfile

# [Choice] Debian version (use bullseye on local arm64/Apple Silicon): bullseye, buster
ARG VARIANT="buster"
FROM mcr.microsoft.com/vscode/devcontainers/base:0-${VARIANT}

# ** [Optional] Uncomment this section to install additional packages. **
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

SHELL [ "/bin/bash", "-o", "pipefail", "-c" ]

# install gcloud sdk
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && \
  apt-get -y install --no-install-recommends \
  apt-transport-https=2.2.4 \
  ca-certificates=20210119 \
  gnupg=2.2.27-2+deb11u2 \
  lsb-release=11.1.0 && \
  echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
  curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
  apt-get update && \
  apt-get install -y --no-install-recommends \
  google-cloud-cli=409.0.0-0 \
  google-cloud-sdk-gke-gcloud-auth-plugin=409.0.0-0 && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

# install skaffold
RUN curl -Lo skaffold skaffold https://storage.googleapis.com/skaffold/releases/v2.0.0/skaffold-linux-amd64 && \
  install skaffold /usr/local/bin/ && \
  rm skaffold

# https://github.com/ContinuumIO/docker-images/blob/master/miniconda3/debian/Dockerfile
ARG CONDA_VERSION=py38_4.12.0

RUN set -x && \
  UNAME_M="$(uname -m)" && \
  if [ "${UNAME_M}" = "x86_64" ]; then \
  MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VERSION}-Linux-x86_64.sh"; \
  SHA256SUM="3190da6626f86eee8abf1b2fd7a5af492994eb2667357ee4243975cdbb175d7a"; \
  elif [ "${UNAME_M}" = "s390x" ]; then \
  MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VERSION}-Linux-s390x.sh"; \
  SHA256SUM="3125961430c77eae81556fa59fe25dca9e5808f76c05f87092d6f2d57f85e933"; \
  elif [ "${UNAME_M}" = "aarch64" ]; then \
  MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VERSION}-Linux-aarch64.sh"; \
  SHA256SUM="0c20f121dc4c8010032d64f8e9b27d79e52d28355eb8d7972eafc90652387777"; \
  elif [ "${UNAME_M}" = "ppc64le" ]; then \
  MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-${CONDA_VERSION}-Linux-ppc64le.sh"; \
  SHA256SUM="4be4086710845d10a8911856e9aea706c1464051a24c19aabf7f6e1a1aedf454"; \
  fi && \
  wget "${MINICONDA_URL}" -O miniconda.sh -q && \
  echo "${SHA256SUM} miniconda.sh" > shasum && \
  if [ "${CONDA_VERSION}" != "latest" ]; then sha256sum --check --status shasum; fi && \
  mkdir -p /opt && \
  sh miniconda.sh -b -p /opt/conda && \
  rm miniconda.sh shasum && \
  ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
  find /opt/conda/ -follow -type f -name '*.a' -delete && \
  find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
  /opt/conda/bin/conda clean -afy

USER vscode

RUN /opt/conda/bin/conda init bash && /opt/conda/bin/conda init zsh

ARG POETRY_VERSION=1.2.2

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=${POETRY_VERSION} /opt/conda/bin/conda run -n base --no-capture-output python3 - && \
  ~/.local/bin/poetry completions bash >> ~/.bash_completion && \
  mkdir ~/.zfunc && \
  ~/.local/bin/poetry completions zsh > ~/.zfunc/_poetry && \
  echo "fpath+=~/.zfunc" >> ~/.zshrc && \
  echo "autoload -Uz compinit && compinit" >> ~/.zshrc