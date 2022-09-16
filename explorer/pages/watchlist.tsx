import * as React from 'react';
import styles from '../styles/Watchlist.module.css';

import { FilterFormValues } from '../types';
import { ProjectKey } from '@wprdc-types/shared';
import {
  affordableHousingProjectMapConnection,
  defaultAffordableHousingProjectMapConnectionProps,
  usePublicHousingProject,
  useWatchlist,
} from '@wprdc-connections/housecat';
import { Map } from '@wprdc-components/map';
import { ConnectedMapEventHandler } from '@wprdc-types/connections';
import { ListSelect } from '@wprdc-components/list-box';
import { Item } from '@wprdc-components/util';
import { LayerPanelVariant } from '@wprdc-types/map';
import Layout from '../components/Layout';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import { ProjectView } from '../parts/ProjectView';

interface Props {}

function Watchlist(props: Props) {
  const [currentProject, setCurrentProject] = React.useState<number>();

  const { data: watchlist } = useWatchlist('steves-watchlist');
  const { data: affordableHousingProject } =
    usePublicHousingProject(currentProject);

  function handleSelect(x: React.Key) {
    setCurrentProject(parseInt(x as string));
  }

  const handleClick: ConnectedMapEventHandler = (_, __, toolboxItems) => {
    if (!!toolboxItems) {
      const items = toolboxItems[ProjectKey.Housecat];
      if (!!items && items.length) setCurrentProject(items[0].id);
    }
  };
  return (
    <div className={styles.wrapper}>
      <div className={styles.menuSection}>
        <h2 className={styles.sectionHeader}>Watchlist</h2>
        {!!watchlist && (
          <ListSelect onSelectionChange={handleSelect}>
            {watchlist.projectIndices.map((projIdx) => (
              <Item key={projIdx.id}>{projIdx.name}</Item>
            ))}
          </ListSelect>
        )}
      </div>
      <div className={styles.mapSection}>
        <Map
          layerPanelVariant={LayerPanelVariant.None}
          onClick={handleClick}
          connections={[affordableHousingProjectMapConnection]}
          connectionHookArgs={{
            [ProjectKey.Housecat]: makeConnectionHookArgs({
              watchlist: watchlist?.slug,
            }),
          }}
        />
      </div>
      <div className={styles.dashboardSection}>
        {!!affordableHousingProject ? (
          <ProjectView project={affordableHousingProject} />
        ) : (
          <div className={styles.infoSection}>
            <h2 className={styles.infoTitle}>
              Find information on affordable housing
            </h2>
            <p className={styles.infoText}>
              Filter the data or zoom the map to locate the affordable housing
              project you are interested in.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

function makeConnectionHookArgs(filterParams?: FilterFormValues) {
  return {
    ...defaultAffordableHousingProjectMapConnectionProps,
    options: {
      ...defaultAffordableHousingProjectMapConnectionProps.options,
      filterParams,
    },
  };
}

Watchlist.getLayout = function getLayout(page: React.ReactChildren) {
  return (
    <Layout Navbar={Navbar} Footer={Footer}>
      {page}
    </Layout>
  );
};

export default Watchlist;
