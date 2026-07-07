import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Nexora AI | AI Autonomous Coding Workspace',
  description: 'World-class futuristic AI coding platform and multi-agent system.',
  viewport: 'width=device-width, initial-scale=1, maximum-scale=1',
  themeColor: '#020617',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="icon" href="/favicon.ico" sizes="any" />
      </head>
      <body>
        <div className="min-h-screen bg-[#020617]">
          {children}
        </div>
      </body>
    </html>
  )
}
