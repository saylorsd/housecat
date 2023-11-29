import styles from './Navbar.module.css';
import Link from 'next/link';
import { useState } from 'react';

interface MenuProps {
  isOpen: boolean;
}
export function Menu({ isOpen }: MenuProps) {
  return (
    <div className={styles.menu}>
      <nav className={isOpen ? styles.openMenu : styles.closedMenu}>
        <ul>
          <li className={styles.menuItem}>
            <Link href="/map">
              <a>Map</a>
            </Link>
          </li>
          <li className={styles.menuItem}>
            <Link href="/watchlist">
              <a>Watchlist</a>
            </Link>
          </li>
          <li className={styles.menuItem}>
            <Link href="/search">
              <a>Search</a>
            </Link>
          </li>
          <li className={styles.menuItem}>
            <Link
              href="https://profiles.wprdc.org/housing"
              target="_blank"
              rel="noreferrer noopener"
            >
              <a target="_blank" rel="noreferrer noopener">
                Indicators
              </a>
            </Link>
          </li>
          <li className={styles.menuItem}>
            <Link href="/terms">
              <a>Terms of Use</a>
            </Link>
          </li>
          <li className={styles.menuItem}>
            <Link href="/about">
              <a>About</a>
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
}
