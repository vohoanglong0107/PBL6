module.exports = {
  "*.{json,md,js,jsx,ts,tsx}": "prettier --write",
  Dockerfile: (absoluteFileNames) =>
    absoluteFileNames.map((absoluteFileName) => {
      const path = require("path");
      const fileName = path.basename(absoluteFileName);
      return `docker run --rm -i -v ${absoluteFileName}:/opt/${fileName} hadolint/hadolint hadolint /opt/${fileName}`;
    }),
};
