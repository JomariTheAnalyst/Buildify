import './globals.css'

export const metadata = {
  title: 'AI Website Builder - Create Websites with AI',
  description: 'Transform your ideas into fully functional websites using the power of AI. Built with Next.js and Google Gemini AI.',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  )
}