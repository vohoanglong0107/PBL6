import { render, screen } from "@testing-library/react";
import ShowResult from "./ShowResult";
import "@testing-library/jest-dom";
describe("ShowResult", () => {
  it("renders a greeting", () => {
    render(<ShowResult />);
    // expect(screen.getByText("Hello World!")).toBeInTheDocument();
  });
});
