/**
 *
 * MapInterface
 *
 */
import * as React from 'react';

import styles from './MapInterface.module.css';
import { MapRef } from 'react-map-gl';

import {
  APIMapBoxResponse,
  ConnectedMapEventHandler,
} from '@wprdc-types/connections';
import { ProjectKey } from '@wprdc-types/shared';
import { GeogBrief, GeographyType } from '@wprdc-types/geo';

import { GeographyConnection } from '@wprdc-connections/geo';
import {
  affordableHousingProjectMapConnection,
  defaultAffordableHousingProjectMapConnectionProps,
} from '@wprdc-connections/housecat';

import { ConnectedSelect } from '@wprdc-components/select';
import { Map } from '@wprdc-components/map';

import { FilterFormValues } from '../../types';
import { LayerPanelVariant } from '@wprdc-types/map';

interface Props {
  mapData?: APIMapBoxResponse;
  filterParams?: FilterFormValues;
  handleProjectSelection: (id: number) => void;
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

export function MapInterface({
  filterParams,
  handleProjectSelection,
  mapData,
}: Props) {
  const mapRef = React.useRef<MapRef>(null);

  const handleZoom = React.useCallback(
    ({ centroid }: { centroid?: [number, number] }) => {
      if (!!centroid) {
        mapRef.current?.flyTo({ center: centroid, zoom: 14, duration: 1300 });
      }
    },
    [],
  );

  const handleClick: ConnectedMapEventHandler = (_, __, toolboxItems) => {
    if (!!toolboxItems) {
      const items = toolboxItems[ProjectKey.Housecat];
      if (!!items && items.length) handleProjectSelection(items[0].id);
    }
  };

  const { source, layers } = mapData || { extras: {} };

  return (
    <div className={styles.wrapper}>
      <div className={styles.menuSection}>
        <fieldset className={styles.zoomControls}>
          <div className={styles.zoomLabel}>
            <legend className={styles.menuLegend}>
              Zoom
              <br />
              Map To
            </legend>
          </div>
          <div className={styles.zoomSection}>
            <ConnectedSelect<GeogBrief>
              label="Zip code"
              aria-label="zoom to zip code"
              id="zip-code-zoom"
              connection={new GeographyConnection(GeographyType.ZCTA, 100)}
              onSelection={handleZoom}
            />
          </div>
          <div className={styles.zoomSection}>
            <ConnectedSelect<GeogBrief>
              label="Pittsburgh Neighborhood"
              aria-label="zoom to neighborhood"
              connection={
                new GeographyConnection(GeographyType.Neighborhood, 100)
              }
              onSelection={handleZoom}
            />
          </div>
        </fieldset>
      </div>
      <div className={styles.mapSection}>
        {!!source && (
          <Map
            layerPanelVariant={LayerPanelVariant.None}
            ref={mapRef}
            sources={[source]}
            layers={layers}
            connections={[affordableHousingProjectMapConnection]}
            connectionHookArgs={{
              [ProjectKey.Housecat]: makeConnectionHookArgs(filterParams),
            }}
            onClick={handleClick}
          />
        )}
      </div>
    </div>
  );
}
