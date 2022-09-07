import React from 'react';
import { useRouter } from 'next/router';

import styles from '../styles/Search.module.css';

import { ResourceOptionTemplateOptions } from '@wprdc-types/list-box';
import { ProjectIndex } from '@wprdc-types/housecat';

import {
  affordableHousingProjectConnection,
  defaultAffordableHousingListBoxProps,
  usePublicHousingProject,
} from '@wprdc-connections/housecat';

import { ConnectedSearchBox } from '@wprdc-components/search-box';

import Layout from '../components/Layout';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { ProjectView } from '../components/ProjectView';

function SearchPage() {
  const [currentProject, setCurrentProject] = React.useState<ProjectIndex>();
  const { data: affordableHousingProject } =
    usePublicHousingProject(currentProject);
  const router = useRouter();

  function handlePress() {
    router.push(`/housecat/map/${currentProject?.id}`);
  }

  return (
    <div className={styles.wrapper}>
      <div className={styles.searchSection}>
        <h2 className={styles.cta}>Find information on subsidized housing</h2>
        <ConnectedSearchBox<
          ProjectIndex,
          ResourceOptionTemplateOptions<ProjectIndex>
        >
          label="Search by project name"
          connection={affordableHousingProjectConnection}
          listBoxProps={defaultAffordableHousingListBoxProps}
          onSelection={setCurrentProject}
        />
      </div>
      <div className={styles.dataSection}>
        {!!affordableHousingProject && (
          <ProjectView
            project={affordableHousingProject}
            onMapLinkPress={handlePress}
          />
        )}
      </div>
    </div>
  );
}

SearchPage.getLayout = function getLayout(page: React.ReactChildren) {
  return (
    <Layout Navbar={Navbar} Footer={Footer}>
      {page}
    </Layout>
  );
};

export default SearchPage;
