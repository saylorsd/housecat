/**
 *
 * MapFilterMenu
 *
 */
import * as React from 'react';
import { Field, FieldProps, Formik } from 'formik';

import styles from './MapFilterMenu.module.css';

import { Button } from '@wprdc-components/button';
import { Item } from '@wprdc-components/util';
import { Select } from '@wprdc-components/select';

import { FilterFormValues } from '../../types';

import { initValues, schema } from './schema';

interface Props {
  onSubmit: (params: FilterFormValues) => void;
}

export function MapFilterForm({ onSubmit }: Props) {
  function handleSubmit(params: FilterFormValues) {
    console.debug({ params });
    // clear out null values
    const cleanParams = Object.fromEntries(
      Object.entries(params).filter(([_, v]) => v !== null),
    );
    onSubmit(cleanParams);
  }

  return (
    <div className={styles.wrapper}>
      <Formik<FilterFormValues>
        initialValues={initValues}
        validateOnBlur
        onSubmit={handleSubmit}
      >
        {(formikProps) => {
          function handleReset() {
            formikProps.resetForm();
            formikProps.submitForm();
          }

          return (
            <form
              onReset={formikProps.handleReset}
              onSubmit={formikProps.handleSubmit}
            >
              {Object.entries(schema).map(([slug, record]) => {
                return (
                  <div className={styles.field} key={slug}>
                    <Field name={slug}>
                      {({
                        field, // { name, value, onChange, onBlur }
                        meta,
                      }: FieldProps) => {
                        return (
                          <Select
                            id={slug}
                            label={record.label}
                            name={field.name}
                            onBlur={field.onBlur}
                            selectedKey={field.value}
                            onSelection={(x) => {
                              field.onChange({
                                target: { value: x, name: field.name },
                              });
                            }}
                            errorMessage={meta.touched && meta.error}
                          >
                            {record.items.map((item) => (
                              <Item key={item.id}>{item.label}</Item>
                            ))}
                          </Select>
                        );
                      }}
                    </Field>
                  </div>
                );
              })}

              <div className={styles.buttonSection}>
                <Button type="submit">Apply Filters</Button>
                <Button onPress={handleReset}>Reset</Button>
              </div>
            </form>
          );
        }}
      </Formik>
    </div>
  );
}
