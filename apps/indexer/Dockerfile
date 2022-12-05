FROM python:3.8


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

RUN /opt/conda/bin/conda install -c pytorch -y faiss-cpu=1.7.3 &&\
  /opt/conda/bin/conda install -c conda-forge -y boto3=1.26.22 flask=2.1.3 gunicorn=20.1.0
WORKDIR /app

COPY . .

ENTRYPOINT ["/opt/conda/bin/conda", "run", "gunicorn", "app.wsgi:app"]
CMD ["-w", "4"]
