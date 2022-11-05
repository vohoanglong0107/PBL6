import React from "react";

import { ComponentStory, ComponentMeta } from "@storybook/react";

import ShowResult from "./ShowResult";

export default {
  component: ShowResult,
} as ComponentMeta<typeof ShowResult>;

export const Primary: ComponentStory<typeof ShowResult> = () => <ShowResult />;
