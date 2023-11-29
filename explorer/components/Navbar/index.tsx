import Link from 'next/link';
import styles from './Navbar.module.css';
import { useLoggedIn } from '@wprdc-connections/housecat';
import { useRouter } from 'next/router';
import { LOGIN_URL, LOGOUT_URL } from '../../settings';
import { Menu } from './Menu';
import { useState } from 'react';
import { HiChevronDown, HiChevronUp } from 'react-icons/hi';

interface Props {
  protect?: boolean;
}

export default function Navbar({ protect = true }) {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const router = useRouter();

  function handleButtonClick() {
    setIsOpen(!isOpen);
  }

  const onError = () => {
    if (protect) router.push(LOGIN_URL);
  };
  const { data: currentUser } = useLoggedIn(onError);

  return (
    <div className={styles.wrapper}>
      <div className={styles.accountLine}>
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
        <div className="ml-4 mr-4">
          {currentUser && currentUser.category === 'ADMIN' && (
            <Link href="/accounts/review">Review</Link>
          )}
        </div>
      </div>
      <div className={styles.top}>
        <div>
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

          <div>
            <button onClick={handleButtonClick} className={styles.menuButton}>
              {isOpen ? <HiChevronUp /> : <HiChevronDown />}
              Menu
            </button>
          </div>
        </div>
        <div className={styles.filler} />

        <div>
          <Menu isOpen={isOpen} />
        </div>
      </div>
    </div>
  );
}
