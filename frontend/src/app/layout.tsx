import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'The Digital Chimera',
  description: 'An asynchronous collaborative drawing game.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col bg-slate-900 text-slate-50">
        <header className="glass-panel p-4 sticky top-0 z-50">
          <div className="max-w-6xl mx-auto flex justify-between items-center">
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-600">The Digital Chimera</h1>
            <nav className="space-x-4">
              <a href="/" className="hover:text-pink-400 transition">Draw</a>
              <a href="/gallery" className="hover:text-pink-400 transition">Gallery</a>
            </nav>
          </div>
        </header>
        <main className="flex-grow flex items-center justify-center p-4">
          {children}
        </main>
      </body>
    </html>
  );
}
