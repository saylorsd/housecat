import styles from './Footer.module.css';

const thisYear = new Date().getFullYear();

export default function Footer() {
  return (
    <div className={styles.wrapper}>
      <div className={styles.copyright}>
        &copy; {thisYear} Western Pennsylvania Regional Data Center, CMU CREATE
        Lab
      </div>
      <div className={styles.spacer} />
      <div className={styles.links}>
        <a
          target="_blank"
          rel="noopener noreferrer"
          href="https://github.com/wprdc/neighborhood-simulacrum"
        >
          GitHub
        </a>
      </div>
    </div>
  );
}
