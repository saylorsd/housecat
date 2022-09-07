import * as React from 'react';

import DefaultFooter from '../Footer';
import DefaultNavbar from '../Navbar';

import styles from './Layout.module.css';

export interface LayoutProps {
  Navbar?: React.FC<any>;
  Footer?: React.FC<any>;
  children?: React.ReactNode | typeof React.Children;
}

export default function Layout({
  Navbar = DefaultNavbar,
  Footer = DefaultFooter,
  children,
}: LayoutProps) {
  return (
    <div className={styles.wrapper}>
      <Navbar />
      <main className={styles.main}>{children as React.ReactNode}</main>
      <Footer />
    </div>
  );
}
