"use client";

import { useEffect } from "react";

import { User } from "@/models";
import { apiPOST } from "@/lib/api_call";
import useSWRMutation from "swr/mutation";

export const useAuth = () => {
  //   const [user, setUser] = useState<User | null>();
  //   const [error, setError] = useState();

  const { trigger, data, error } = useSWRMutation<User, Error>("/me/", apiPOST);

  useEffect(() => {
    initAuth();
  }, []);

  useEffect(() => {
    console.log(data);
    console.log(error);
  }, []);

  const initAuth = async () => {
    try {
      await trigger();
    } catch {}
  };

  return {
    user: data,
    error,
  };
};
