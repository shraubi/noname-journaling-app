import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Unsaid — a journal that notices when you stop",
  description:
    "A private, model-free writing space that helps you move through a stuck thought.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
