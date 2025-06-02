import { SecondaryHeader } from "@/components/common/headers";

export default async function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      <SecondaryHeader />

      <div className="max-w-7xl flex flex-col gap-12 items-start min-h-screen bg-gray-50">
        {children}
      </div>
    </>
  );
}
