import React from "react";

import { ComponentStory, ComponentMeta } from "@storybook/react";

import Contact from "./Contact";

export default {
  component: Contact,
} as ComponentMeta<typeof Contact>;

export const Primary: ComponentStory<typeof Contact> = () => <Contact />;
