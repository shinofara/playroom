import useSWR from "swr";
import { swrFetcher } from "@/lib/api";

// SWR用カスタムフック
export const useSWRFetch = <T>(path: string | null) =>
  useSWR<T>(path, swrFetcher<T>, {
    revalidateOnFocus: false,
    errorRetryCount: 3,
  });
