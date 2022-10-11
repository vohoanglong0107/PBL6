import { render, screen } from "@testing-library/react";
import HelloWorld from "./HelloWorld";
import "@testing-library/jest-dom";
describe("HelloWorld", () => {
  it("renders a greeting", () => {
    render(<HelloWorld />);
    expect(screen.getByText("Hello World!")).toBeInTheDocument();
  });
});
