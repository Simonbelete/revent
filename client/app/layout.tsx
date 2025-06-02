import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Layout } from "antd";

import "./globals.css";
import "react-big-calendar/lib/css/react-big-calendar.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "REvent",
    template: `%s | REvent`,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <Layout
          className="min-h-screen bg-gray-50 h-full"
          style={{ height: "100vh" }}
        >
          {children}
        </Layout>
      </body>
    </html>
  );
}
