import { refreshAccessToken } from "@/lib/manage_tokens";
import { useEffect } from "react";

/**
 * Refresh token every 5min
 */
export const useRefreshAccessToken = () => {
  useEffect(() => {
    const interval = setInterval(
      () => {
        console.log("Refreshing access token...");
        refreshAccessToken();
      },
      5 * 60 * 1000
    ); // every 5 minutes

    return () => clearInterval(interval); // cleanup on unmount
  }, []);
};
