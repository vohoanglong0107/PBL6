import React from "react";

import { ComponentStory, ComponentMeta } from "@storybook/react";

import HelloWorld from "./HelloWorld";

export default {
  component: HelloWorld,
} as ComponentMeta<typeof HelloWorld>;

export const Primary: ComponentStory<typeof HelloWorld> = () => <HelloWorld />;
