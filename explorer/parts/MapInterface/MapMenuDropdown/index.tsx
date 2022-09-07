/**
 *
 * MapMenuDropdown
 *
 */
import * as React from 'react';

import { SelectProps } from '@wprdc-types/select';
import { Select } from '@wprdc-components/select';
import { Item } from '@wprdc-components/util';

interface Props<T> extends Omit<SelectProps<T>, 'children'> {}

export function MapMenuDropdown<T extends object>(props: Props<T>) {
  return (
    <Select<T> {...props}>
      <Item>test</Item>
    </Select>
  );
}
