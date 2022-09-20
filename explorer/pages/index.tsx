import Link from 'next/link';
import Image from 'next/image';

import styles from '../styles/Home.module.css';

import Layout from '../components/Layout';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';

import CREATELogo from '../assets/logos/create_logo.png';
import WPRDCLogo from '../assets/logos/wprdc-square.png';

function HousecatHome() {
  return (
    <div className={styles.wrapper}>
      <div>
        <h2 className={styles.infoTitle}>
          Find information on subsidized housing
        </h2>
        <div className={styles.buttonSection}>
          <Link href="/map">
            <button className={styles.bigButton}>
              <div className={styles.buttonTitle}>🗺 Map</div>
              <div className={styles.buttonText}>
                Explore all the data on a map
              </div>
            </button>
          </Link>
          <Link href="/watchlist">
            <button className={styles.bigButton}>
              <div className={styles.buttonTitle}>✔️ Watchlist</div>
              <div className={styles.buttonText}>
                Limit to selected projects
              </div>
            </button>
          </Link>
          <Link href="/search">
            <button className={styles.bigButton}>
              <div className={styles.buttonTitle}>🔍 Search</div>
              <div className={styles.buttonText}>
                Find information on subsidized housing
              </div>
            </button>
          </Link>
        </div>
        <div className={styles.smallButtonSection}>
          <Link href="https://profiles.wprdc.org/housing">
            <a
              target="_blank"
              rel="noreferrer noopener"
              className={styles.bigButton}
            >
              <div className={styles.buttonTitle}>📊 Indicators</div>
              <div className={styles.buttonText}>
                Community-level housing statistics.
              </div>
            </a>
          </Link>
          <Link href="/about">
            <button className={styles.bigButton}>
              <div className={styles.buttonTitle}>📜 About</div>
              <div className={styles.buttonText}>
                Information about the data and process
              </div>
            </button>
          </Link>
        </div>
        <div className={styles.content}>
          <p>
            <strong>
              Affordable housing is a growing issue of regional importance in
              our community.
            </strong>
            {'  '}
            In May, 2016, the City of Pittsburgh&rsquo;s Affordable Housing Task
            Force released{' '}
            <a href="https://apps.pittsburghpa.gov/mayorpeduto/FinalReport_5_31_16.pdf">
              its report
            </a>{' '}
            to the Mayor and City Council. The report called for the creation of
            a centralized, publicly-accessible repository of affordable housing
            data to be hosted by the{' '}
            <a href="https://www.wprdc.org">
              Western Pennsylvania Regional Data Center
            </a>
            . In addition to including lists of deed and income-restricted
            properties, the Task Force also sought to use data to track
            compliance, monitor housing conditions, and establish an
            &lsquo;early warning system&rsquo; when use restrictions change, or
            condition issues threaten overall affordability and family
            stability.
          </p>
          <p>
            To support this goal of using data to proactively monitor threats to
            affordability, the Western Pennsylvania Regional Data Center at the
            University of Pittsburgh and the{' '}
            <a href="https://cmucreatelab.org/">Carnegie Mellon CREATE Lab</a>{' '}
            partnered to develop a frequently-updated collection of data about
            subsidized properties in Allegheny County from approximately 20
            different databases provided by HUD and the Pennsylvania Housing
            Finance Agency (PHFA). This tool launched in April 2022 allows
            people to view data for a project, and filter the data to display a
            subset of properties including those with low inspection scores and
            those that may have their subsidies expire in coming years. Users of
            the data explorer are also able to create watch lists of properties
            whose affordability is at risk. Properties can be viewed on a map,
            with data associated with each property displayed on screen.
          </p>
        </div>
        <div className={styles.logos}>
          <h2></h2>
          <a href="https://www.wprdc.org">
            <Image src={WPRDCLogo} alt="WPRDC" />
          </a>
          <a href="https://cmucreatelab.org/">
            <Image src={CREATELogo} alt="WPRDC" />
          </a>
        </div>
      </div>
    </div>
  );
}

HousecatHome.getLayout = function getLayout(page: React.ReactChildren) {
  return (
    <Layout Navbar={Navbar} Footer={Footer} protect={false}>
      {page}
    </Layout>
  );
};

export default HousecatHome;
