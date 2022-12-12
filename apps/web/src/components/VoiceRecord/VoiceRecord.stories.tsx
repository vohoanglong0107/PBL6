import React from "react";

import { ComponentStory, ComponentMeta } from "@storybook/react";

import VoiceRecord from "./VoiceRecord";

export default {
  component: VoiceRecord,
} as ComponentMeta<typeof VoiceRecord>;

export const Primary: ComponentStory<typeof VoiceRecord> = () => (
  <VoiceRecord />
);
