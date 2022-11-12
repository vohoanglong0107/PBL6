import React from "react";

import { ComponentStory, ComponentMeta } from "@storybook/react";

import AboutUs from "./AboutUs";

export default {
  component: AboutUs,
} as ComponentMeta<typeof AboutUs>;

export const Primary: ComponentStory<typeof AboutUs> = () => <AboutUs />;
