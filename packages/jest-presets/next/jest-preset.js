/** @type (import('jest').Config) */
const config = {
  setupFilesAfterEnv: [
    "@testing-library/jest-dom",
    "@testing-library/jest-dom/extend-expect",
  ],
  testEnvironment: "jest-environment-jsdom",
};

module.exports = config;
