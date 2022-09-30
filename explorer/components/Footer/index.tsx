import styles from './Footer.module.css';
import Link from 'next/link';

const thisYear = new Date().getFullYear();

export default function Footer() {
  return (
    <div className={styles.wrapper}>
      <div className={styles.copyright}>
        Built by the Western Pennsylvania Regional Data Center and CMU CREATE
        Lab
      </div>
      <div className={styles.spacer} />
      <div className={styles.links}>
        <Link href="/terms">
          <a>Terms of Service</a>
        </Link>
        <a
          target="_blank"
          rel="noopener noreferrer"
          href="https://github.com/wprdc/housecat"
        >
          Source Code
        </a>
      </div>
    </div>
  );
}
