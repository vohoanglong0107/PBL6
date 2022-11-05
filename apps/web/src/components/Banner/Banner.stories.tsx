import React from "react";

import { ComponentStory, ComponentMeta } from "@storybook/react";

import Banner from "./Banner";

export default {
  component: Banner,
} as ComponentMeta<typeof Banner>;

export const Primary: ComponentStory<typeof Banner> = () => <Banner />;