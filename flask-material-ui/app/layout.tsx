import { ReactNode } from 'react';
import '../styles/globals.css'; // Import global styles
import RootLayout from './RootLayout';

const Layout = ({ children }: { children: ReactNode }) => {
  return (
    <html lang="en">
      <head>
        <title>Endava | Talent Explorer</title>
        <link rel="icon" href="/Endava_Symbol.svg" type="image/svg+xml" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </head>
      <body>
        <RootLayout>
          {children}
        </RootLayout>
      </body>
    </html>
  );
};

export default Layout;
