import React from "react";

import { ComponentStory, ComponentMeta } from "@storybook/react";

import ShowResult from "./ShowResult";

export default {
  component: ShowResult,
} as ComponentMeta<typeof ShowResult>;

export const Primary: ComponentStory<typeof ShowResult> = () => (
  <ShowResult
    results={[
      { id: "0", title: "Safe and Sound", artist: "Taylor Swift" },
      { id: "1", title: "Cheap Thrills", artist: "Sia" },
    ]}
  />
);
