"use client";

import { Button, Flex, Layout, Typography } from "antd";
import Link from "next/link";

const { Header } = Layout;
const { Title } = Typography;

export const SecondaryHeader = () => {
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
        <Link href="/">
          <Button type="primary">Go to events</Button>
        </Link>
      </Flex>
    </Header>
  );
};
