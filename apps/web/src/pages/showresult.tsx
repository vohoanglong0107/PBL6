import { useRouter } from "next/router";
import ShowResult from "@/components/ShowResult";

export default function Web() {
  const router = useRouter();
  const { results } = router.query;
  if (results)
    return <ShowResult results={JSON.parse(results as string)["data"]} />;
  return null;
}
