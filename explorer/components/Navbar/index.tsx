import Link from 'next/link';
import styles from './Navbar.module.css';

export default function Navbar() {
  return (
    <div className={styles.wrapper}>
      <div className={styles.branding}>
        <div className={styles.title}>
          <Link href="/">
            <a>HouseCat</a>
          </Link>
        </div>
        <div className={styles.subtitle}>
          affordable housing information catalogue
        </div>
      </div>
      <div className={styles.filler} />
      <div className={styles.menu}>
        <div className={styles.menuItem}>
          <Link href="/map">
            <a>Map</a>
          </Link>
        </div>
        <div className={styles.menuItem}>
          <Link href="/watchlist">
            <a>Watchlist</a>
          </Link>
        </div>
        <div className={styles.menuItem}>
          <Link href="/search">
            <a>Search</a>
          </Link>
        </div>
        <div className={styles.menuItem}>
          <Link
            href="https://profiles.wprdc.org/housing"
            target="_blank"
            rel="noreferrer noopener"
          >
            <a target="_blank" rel="noreferrer noopener">
              Indicators
            </a>
          </Link>
        </div>
        <div className={styles.menuItem}>
          <Link href="/about">
            <a>About</a>
          </Link>
        </div>
      </div>
    </div>
  );
}
