import React from "react";

import { ComponentStory, ComponentMeta } from "@storybook/react";

import SupportList from "./SupportList";

export default {
  component: SupportList,
} as ComponentMeta<typeof SupportList>;

export const Primary: ComponentStory<typeof SupportList> = () => (
  <SupportList />
);
