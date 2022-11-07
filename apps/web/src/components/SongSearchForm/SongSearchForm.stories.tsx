import React from "react";

import { ComponentStory, ComponentMeta } from "@storybook/react";

import SongSearchForm from "./SongSearchForm";

export default {
  component: SongSearchForm,
} as ComponentMeta<typeof  SongSearchForm>;

export const Primary: ComponentStory<typeof SongSearchForm> = () => <SongSearchForm />;
