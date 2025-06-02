"use client";

import { useState } from "react";
import { useForm, Controller } from "react-hook-form";
import { Alert, Button, Form, Input, Typography, message } from "antd";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import useSWRMutation from "swr/mutation";
import { useRouter } from "next/navigation";

import { apiPOST } from "@/lib/api_call";
import { JWT } from "@/lib/jwt";

const { Title } = Typography;

const schema = yup.object().shape({
  username: yup.string().required("username is required"),
  password: yup.string().required("Password is required"),
});

type LoginFormInputs = {
  username: string;
  password: string;
};
export const SignIn = () => {
  const router = useRouter();
  const [submitError, setSubmitError] = useState("");

  const {
    handleSubmit,
    control,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormInputs>({
    resolver: yupResolver(schema),
  });

  const { trigger } = useSWRMutation("/auth/token/", apiPOST);

  const onSubmit = async (data: LoginFormInputs) => {
    try {
      setSubmitError("");
      const res = await trigger(data);

      const { access, refresh } = res;

      JWT.setAccessToken(access);
      JWT.setRefreshToken(refresh);

      message.success("Login successful");

      router.push("/");
    } catch (error) {
      console.log(error);
      setSubmitError("Invalid credentials");
    }

    // try {
    //   console.log("Login Data:", data);
    //   message.success("Logged in successfully");
    // } catch {
    //   message.error("Login failed");
    // }
  };

  return (
    <div style={{ maxWidth: 400, margin: "100px auto" }}>
      <Title level={2}>Login</Title>
      <Form onFinish={handleSubmit(onSubmit)} layout="vertical">
        {submitError && (
          <Alert
            message="Error"
            description={submitError}
            type="error"
            showIcon
            style={{ marginBottom: 16 }}
          />
        )}

        <Form.Item
          label="User name"
          validateStatus={errors.username ? "error" : ""}
          help={errors.username?.message}
        >
          <Controller
            name="username"
            control={control}
            defaultValue=""
            render={({ field }) => (
              <Input {...field} placeholder="Enter your User name" />
            )}
          />
        </Form.Item>

        <Form.Item
          label="Password"
          validateStatus={errors.password ? "error" : ""}
          help={errors.password?.message}
        >
          <Controller
            name="password"
            control={control}
            defaultValue=""
            render={({ field }) => (
              <Input.Password {...field} placeholder="Enter your password" />
            )}
          />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" block loading={isSubmitting}>
            Log In
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};
