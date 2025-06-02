"use client";

import { useAuth } from "@/hooks";
import { Button, Flex, Layout, Typography } from "antd";
import Link from "next/link";

const { Header } = Layout;
const { Title } = Typography;

export const PrimaryHeader = ({
  onCreateEvent,
}: {
  onCreateEvent: () => void;
}) => {
  const { user } = useAuth();

  return (
    <Header className="bg-white shadow-sm px-4 flex justify-between items-center">
      <Title
        level={3}
        className="!m-0 text-white"
        style={{ color: "white !important" }}
      >
        REvent
      </Title>
      <Flex gap={5}>
        {user && (
          <Button type="primary" onClick={onCreateEvent}>
            Create Event
          </Button>
        )}
        {!user && (
          <Link href="/sign-in">
            <Button type="primary">Login</Button>
          </Link>
        )}
        {!user && (
          <Link href="/sign-up">
            <Button>Sign up</Button>{" "}
          </Link>
        )}
      </Flex>
    </Header>
  );
};
