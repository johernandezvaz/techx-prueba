import './globals.css';
import type { Metadata }  from 'next';
import { Inter } from 'next/font/google';
import { Toaster } from '../components/ui/sonner';

const inter = Inter({ subsets: ['latin']});

export const metadata: Metadata = {
  title: 'Parte 1: Procesador de Recibo',
  description: 'Extrae texto de imagenes de tus recibos'
};

export default function RootLayout({
  children,
} : {
  children: React.ReactNode,
}) {
  return (
    <html lang='es'>
      <body className={inter.className}>
        {children}
        <Toaster position='top-right'/>
      </body>
    </html>
  );
}