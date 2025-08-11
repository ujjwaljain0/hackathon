import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Providers } from './providers'

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI Scrum Dashboard | Next-Gen Project Management",
  description: "Revolutionary AI-powered Scrum Master and Project Manager dashboard with real-time insights, smart suggestions, and collaborative workflows.",
  keywords: ["scrum", "agile", "project management", "AI", "dashboard", "kanban", "sprint planning"],
  authors: [{ name: "AI Dashboard Team" }],
  viewport: "width=device-width, initial-scale=1",
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#0a0a0a" }
  ],
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "https://ai-scrum-dashboard.vercel.app",
    siteName: "AI Scrum Dashboard",
    title: "AI Scrum Dashboard | Next-Gen Project Management",
    description: "Revolutionary AI-powered Scrum Master and Project Manager dashboard with real-time insights, smart suggestions, and collaborative workflows.",
  },
  twitter: {
    card: "summary_large_image",
    site: "@ai_scrum_dash",
    creator: "@ai_scrum_dash",
    title: "AI Scrum Dashboard | Next-Gen Project Management",
    description: "Revolutionary AI-powered Scrum Master and Project Manager dashboard with real-time insights, smart suggestions, and collaborative workflows.",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <Providers>
          <div className="min-h-screen bg-background text-foreground">
            {children}
          </div>
        </Providers>
      </body>
    </html>
  );
}
