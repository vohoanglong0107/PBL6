import React from "react";

import { ComponentStory, ComponentMeta } from "@storybook/react";

import Content from "./Content";

export default {
  component: Content,
} as ComponentMeta<typeof Content>;

export const Primary: ComponentStory<typeof Content> = () => <Content />;
