import { render, screen } from "@testing-library/react";
import Header from "./Header";

describe("Header", () => {
  it("renders a title", () => {
    render(<Header />);
    expect(screen.getByText("Docs")).toBeInTheDocument();
  });
});
