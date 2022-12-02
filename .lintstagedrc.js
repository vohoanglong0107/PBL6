module.exports = {
  "*.{yaml,yml,json,md,html,css,scss,js,jsx,ts,tsx}": "prettier --write",
  Dockerfile: (absoluteFileNames) =>
    absoluteFileNames.map((absoluteFileName) => {
      const path = require("path");
      const fileName = path.basename(absoluteFileName);
      // https://github.com/hadolint/hadolint#configure
      return `docker run
        --rm
        -i
        -w /opt
        -v ${absoluteFileName}:/opt/${fileName}
        -v ${__dirname}/.hadolint.yaml:/opt/.hadolint.yaml
        ghcr.io/hadolint/hadolint
        hadolint
        /opt/${fileName}`;
    }),
  "*.{tf,tfvars}": "terraform fmt",
  "*.py": ["isort", "black"],
};
