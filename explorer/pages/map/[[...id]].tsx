/**
 *
 * MapPage
 *
 */
import * as React from 'react';

import { useRouter } from 'next/router';

import { FilterFormValues } from '../../types';

import { MapFilterForm } from '../../parts/MapFilterForm';
import { MapInterface } from '../../parts/MapInterface';
import { ProjectView } from '../../parts/ProjectView';

import Layout from '../../components/Layout';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';

import styles from '../../styles/Map.module.css';

import {
  useHousingProjectMap,
  useLoggedIn,
  usePublicHousingProject,
} from '@wprdc-connections/housecat';

import { LoadingMessage } from '@wprdc-components/loading-message';
import { LOGIN_URL } from '../../settings';

function MapPage() {
  const boardRef = React.useRef<HTMLDivElement>(null);

  const [filterParams, setFilterParams] = React.useState<FilterFormValues>();
  const [currentProject, setCurrentProject] = React.useState<number>();

  const { data: mapData, error } = useHousingProjectMap(filterParams);

  const { data: affordableHousingProject, isLoading } =
    usePublicHousingProject(currentProject);

  const onError = () => {
    router.push(LOGIN_URL);
  };
  const { data: currentUser } = useLoggedIn(onError);

  const router = useRouter();

  // handle query params
  React.useEffect(() => {
    const { id: _projectID } = router.query;
    // read data viz slug from path
    if (!!_projectID && _projectID.length)
      setCurrentProject(Number.parseInt(_projectID[0]));
  }, [router.query]);

  function handleFormChange(params: FilterFormValues) {
    setFilterParams(params);
  }

  function handleProjectSelect(id: number) {
    router.push(`/map/${id}`);
  }

  if (!!boardRef && boardRef.current) {
    boardRef.current.scrollTop = 0;
  }

  return (
    <div className={styles.wrapper}>
      <div className={styles.menuSection}>
        <h2 className={styles.filterTitle}>Filter</h2>
        <MapFilterForm onSubmit={handleFormChange} />
      </div>
      <div className={styles.mapSection}>
        <MapInterface
          mapData={mapData}
          filterParams={filterParams}
          handleProjectSelection={handleProjectSelect}
        />
      </div>
      <div ref={boardRef} className={styles.dashboardSection}>
        {!!affordableHousingProject && (
          <ProjectView project={affordableHousingProject} />
        )}
        {!currentProject && (
          <section id="intro" className={styles.infoSection}>
            <p className={styles.cta}>Click on the map to explore the data.</p>

            <p>
              Affordable housing is a growing issue of regional importance in
              our community. In May, 2016, the City of Pittsburgh&rsquo;s
              Affordable Housing Task Force released{' '}
              <a href="https://apps.pittsburghpa.gov/mayorpeduto/FinalReport_5_31_16.pdf">
                its report
              </a>{' '}
              to the Mayor and City Council. The report called for the creation
              of a centralized, publicly-accessible repository of affordable
              housing data to be hosted by the{' '}
              <a href="https://www.wprdc.org">
                Western Pennsylvania Regional Data Center
              </a>
              . In addition to including lists of deed and income-restricted
              properties, the Task Force also sought to use data to track
              compliance, monitor housing conditions, and establish an
              &lsquo;early warning system&rsquo; when use restrictions change,
              or condition issues threaten overall affordability and family
              stability.
            </p>
            <p>
              To support this goal of using data to proactively monitor threats
              to affordability, the Western Pennsylvania Regional Data Center at
              the University of Pittsburgh and the{' '}
              <a href="https://cmucreatelab.org/">Carnegie Mellon CREATE Lab</a>{' '}
              partnered to develop a frequently-updated collection of data about
              subsidized properties in Allegheny County from approximately 20
              different databases provided by HUD and the Pennsylvania Housing
              Finance Agency (PHFA). This tool launched in April 2022 allows
              people to view data for a project, and filter the data to display
              a subset of properties including those with low inspection scores
              and those that may have their subsidies expire in coming years.
              Users of the data explorer are also able to create watch lists of
              properties whose affordability is at risk. Properties can be
              viewed on a map, with data associated with each property displayed
              on screen.
            </p>
          </section>
        )}
        {!!currentProject && isLoading && (
          <LoadingMessage message="Loading project data" />
        )}
      </div>
    </div>
  );
}

MapPage.getLayout = function getLayout(page: React.ReactChildren) {
  return (
    <Layout Navbar={Navbar} Footer={Footer} protect={true}>
      {page}
    </Layout>
  );
};

export default MapPage;
