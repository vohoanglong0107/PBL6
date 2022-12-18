// import VoiceRecord from "@/components/VoiceRecord";
import dynamic from "next/dynamic";
const VoiceRecord = dynamic(() => import("../components/VoiceRecord"), { ssr: false });
export default function Web() {
  return <VoiceRecord />;
}
