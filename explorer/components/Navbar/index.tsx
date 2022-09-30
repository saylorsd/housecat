import Link from 'next/link';
import styles from './Navbar.module.css';
import { useLoggedIn } from '@wprdc-connections/housecat';
import { useEffect } from 'react';
import { useRouter } from 'next/router';

const LOGOUT_URL =
  process.env.NEXT_PUBLIC_LOGOUT_URL || 'http://localhost:8000/accounts/logout';
const LOGIN_URL =
  process.env.NEXT_PUBLIC_LOGIN_URL || 'http://localhost:8000/accounts/login';

interface Props {
  protect?: boolean;
}

export default function Navbar({ protect = true }) {
  const router = useRouter();

  const onError = () => {
    if (protect) router.push(LOGIN_URL);
  };
  const { data: currentUser } = useLoggedIn(onError);

  return (
    <div className={styles.wrapper}>
      <div className={styles.top}>
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
            <Link href="/terms">
              <a>Terms of Use</a>
            </Link>
          </div>
          <div className={styles.menuItem}>
            <Link href="/about">
              <a>About</a>
            </Link>
          </div>
        </div>
      </div>
      <div className={styles.bottom}>
        <div></div>
        <div>
          {currentUser ? (
            <div>
              Logged in as {currentUser.user.email} |{' '}
              <a href={LOGOUT_URL}>logout</a>
            </div>
          ) : (
            <a href={LOGIN_URL}>login </a>
          )}
        </div>
      </div>
    </div>
  );
}
