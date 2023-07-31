from mimesis import Generic
from polygons import *
from variables import *
from math import ceil
import pandas as pd


# Create Generic provider object 
g = Generic('en')


""" Data Tables """

# Active HUD Multifamily Insured Mortgages (Pennsylvania) - 384
table = []
for i in range(384):
    row = {
        'fha_loan_id': g.person.identifier(mask='######'),
        'hud_property_name': g.choice([g.finance.company(), g.address.address()]),
        'property_street_address': g.address.address(),
        'city': g.address.city(),
        'state': 'PA',
        'zip_code': g.address.zip_code(),
        'units': g.numeric.integer_number(start=1, end=500),
        'initial_endorsement_date': g.datetime.formatted_date(fmt="%Y-%m-%d", start=1980, end=2023),
        'original_mortgage_amount': g.numeric.integer_number(start=100000, end=150000000),
        'maturity_date': g.datetime.formatted_date(fmt="%Y-%m-%d", start=2023, end=2063),
        'term_in_months': g.numeric.integer_number(start=180, end=480),
        'interest_rate': g.numeric.float_number(start=2.0, end=8.5, precision=3),
        'current_principal_and_interest': g.finance.price(minimum=500, maximum=400000),
        'amoritized_principal_balance': g.finance.price(minimum=10000, maximum=1000000000),
        'holder_name': g.finance.company(),
        'holder_city': g.address.city(),
        'holder_state': g.address.state(),
        'servicer_name': g.finance.company(),
        'servicer_city': g.address.city(),
        'servicer_state': g.address.state(),
        'section_of_act_code': "".join(g.random.choices(g.text.alphabet(), k=3)),
        'program_category': g.text.text(quantity=1)
    }
    table.append(row)
ActiveHUDMultifamilyInsuredMortgages_df = pd.DataFrame.from_dict(table)
ActiveHUDMultifamilyInsuredMortgages_df.to_csv('./csv/ActiveHUDMultifamilyInsuredMortgages.csv', index=False, encoding='utf-8')


# All Buildings from LIHTC Projects (Pennsylvania) - 2,791
table = []
for i in range(2791):
    row = {
        'lihtc_project_id': g.person.identifier(mask='PAA########'),
        'normalized_state_id': g.choice([g.person.identifier(mask='TC####-####'), g.person.identifier(mask='PAA########')]),
        'hud_property_name': g.choice([g.finance.company(), g.address.address()]),
        'property_street_address': g.address.address(),
        'city': g.address.city(),
        'state': 'PA',
        'zip_code': g.address.zip_code(),
        'state_id': g.choice([g.person.identifier(mask='TC####-####'), g.person.identifier(mask='PAA########')]),
    }
    table.append(row)
AllBuildingsFromLIHTCProjects_df = pd.DataFrame.from_dict(table)
AllBuildingsFromLIHTCProjects_df.to_csv('./csv/AllBuildingsFromLIHTCProjects.csv', index=False, encoding='utf-8')


# HUD Inspection Scores (Allegheny County) - 75
table = []
for i in range(75):
    coords = generate_coords(poly=allegheny)
    row = {
        'development_code': g.person.identifier(mask='PA00######'),
        'state': 'PA',
        'latitude': coords[1],
        'longitude': coords[0],
        'county': 'Allegheny',
        'county_fips_code': '42003',
        'hud_property_name': g.choice([g.finance.company(), g.address.address()]),
        'property_street_address': g.address.address(),
        'inspection_id': g.numeric.integer_number(start=500000, end=700000),
        'inspection_property_id_multiformat': g.person.identifier(mask='PA00######'),
        'inspection_score': g.numeric.integer_number(start=25, end=100),
        'inspection_date': g.datetime.formatted_date(fmt="%Y-%m-%d", start=2015, end=2023),
        'participant_code': g.person.identifier(mask='PA00#'),
        'formal_participant_name': g.finance.company(),
        'geom': create_point(coords),
        'geom_webmercator': create_point(coords)
    }
    table.append(row)
HUDInspectionScores_df = pd.DataFrame.from_dict(table)
HUDInspectionScores_df.to_csv('./csv/HUDInspectionScores.csv', index=False, encoding='utf-8')


# HUD Insured Multifamily Properties (Allegheny County) - 85
table = []
for i in range(85):
    coords = generate_coords(poly=allegheny)
    row = {
        'property_id': g.person.identifier(mask='800######'),
        'fha_loan_id': g.person.identifier(mask='######'),
        'longitude': coords[0],
        'latitude': coords[1],
        'geocoding_accuracy': 'R',
        'county': 'Allegheny',
        'county_fips_code': '42003',
        'congressional_district_code': str(g.numeric.integer_number(start=12, end=18)),
        'census_tract': g.person.identifier(mask='420########'),
        'municipality_fips': g.person.identifier(mask='800######'),
        'municipality_name': g.choice(municipalities),
        'hud_property_name': g.choice([g.finance.company(), g.address.address()]),
        'property_street_address': g.address.address(),
        'city': g.address.city(),
        'state': 'PA',
        'zip_code': g.address.zip_code(),
        'units': g.numeric.integer_number(start=1, end=500),
        'assisted_units': g.numeric.integer_number(start=0, end=600),
        'property_category_name': g.choice(['Insured-Subsidized', 'Insured-Unsubsidized']),
        'property_manager_name': g.person.full_name(),
        'property_manager_phone': g.person.phone_number(mask='(412) ###-####'),
        'associated_fha_loan_id': g.person.identifier(mask='######'),
        'initial_endorsement_date': g.datetime.formatted_date(fmt="%Y-%m-%d", start=1980, end=2023),
        'original_mortgage_amount': g.numeric.integer_number(start=100000, end=150000000),
        'maturity_date': g.datetime.formatted_date(fmt="%Y-%m-%d", start=2023, end=2063),
        'program_category': g.choice(['202/8 NC', '202/8 SR', '223(a)(7) Refi of 223f ALF', '223(a)(7) Refi of 223f Nursing/ ICF']),
        'program_category_2': 'None',
        'loan_units': g.numeric.integer_number(start=0, end=350),
        'client_group_name': g.choice(['Assisted Living Care', 'Elderly', 'Family & Elderly', 'Indv. families - not eld/ handicap	']),
        'client_group_type': g.choice(['Family', 'Elderly', 'None']),
        'section_of_act_code': "".join(g.random.choices(g.text.alphabet(), k=3)),
        'servicing_site_name_loan': g.choice(['Baltimore', 'Pittsburgh', 'OHP']),
        'geom': create_point(coords),
        'geom_webmercator': create_point(coords)
    }
    table.append(row)
HUDInsuredMultifamilyProperties_df = pd.DataFrame.from_dict(table)
HUDInsuredMultifamilyProperties_df.to_csv('./csv/HUDInsuredMultifamilyProperties.csv', index=False, encoding='utf-8')


# HUD Multifamily Fiscal Year Production (Pennsylvania) - 657
table = []
for i in range(657):
    row = {
        'fha_loan_id': g.person.identifier(mask='######'),
        'hud_property_name': g.choice([g.finance.company(), g.address.address()]),
        'city': g.address.city(),
        'state': 'PA',
        'initial_endorsement_date': g.datetime.formatted_date(fmt="%Y-%m-%d", start=1980, end=2023),
        'original_mortgage_amount': g.numeric.integer_number(start=100000, end=150000000),
        'program_category': g.choice(['202/8 NC', '202/8 SR', '223(a)(7) Refi of 223f ALF', '223(a)(7) Refi of 223f Nursing/ ICF']),
        'units': g.numeric.integer_number(start=1, end=500),
        'basic_fha_risk_share_or_other': g.choice(['Basic FHA', 'Hospitals & Group Practice', 'Risk Sharing']),
        'current_status_of_loan': g.choice(['Finally Endorsed', 'Initially Endorsed']),
        'date_of_firm_issue': g.datetime.formatted_date(fmt="%Y-%m-%d", start=2020, end=2023),
        'firm_commitment_lender': g.finance.company(),
        'holder_name': g.finance.company()
    }
    table.append(row)
HUDMultifamilyFiscalYearProduction_df = pd.DataFrame.from_dict(table)
HUDMultifamilyFiscalYearProduction_df.to_csv('./csv/HUDMultifamilyFiscalYearProduction.csv', index=False, encoding='utf-8')


# HUD Multifamily Inspection Scores (Pennsylvania) - 2,729
table = []
for i in range(2729):
    row = {
        'property_id': g.person.identifier(mask='800######'),
        'hud_property_name': g.choice([g.finance.company(), g.address.address()]),
        'inspection_property_id_multiformat': g.person.identifier(mask='PA00######'),
        'city': g.address.city(),
        'state': 'PA',
        'inspection_id': g.numeric.integer_number(start=500000, end=700000),
        'inspection_score': g.numeric.integer_number(start=25, end=100),
        'inspection_date': g.datetime.formatted_date(fmt="%Y-%m-%d", start=2015, end=2023)
    }
    table.append(row)
HUDMultifamilyInspectionScores_df = pd.DataFrame.from_dict(table)
HUDMultifamilyInspectionScores_df.to_csv('./csv/HUDMultifamilyInspectionScores.csv', index=False, encoding='utf-8')


# HUD Public Housing Buildings (Allegheny County) - 1,040
table = []
for i in range(1040):
    coords = generate_coords(poly=allegheny)
    row = {
        'development_code': g.person.identifier(mask='PA00######'),
        'longitude': coords[0],
        'latitude': coords[1],
        'geocoding_accuracy': g.choice(['4', 'B', 'R', 'T']),
        'county_fips_code': '42003',
        'census_tract': g.person.identifier(mask='420########'),
        'municipality_fips': g.person.identifier(mask='800######'),
        'municipality_name': g.choice(municipalities),
        'hud_property_name': g.choice([g.finance.company(), g.address.address()]),
        'property_street_address': g.address.address(),
        'city': g.address.city(),
        'state': 'PA',
        'zip_code': g.address.zip_code(),
        'units': g.numeric.integer_number(start=1, end=500),
        'owner_organization_name': 'Housing Authority of ' + g.choice(municipalities),
        'participant_code': g.person.identifier(mask='PA00#'),
        'formal_participant_name': g.finance.company(), 
        'project_name': g.address.street_name(),
        'total_dwelling_units': g.numeric.integer_number(start=1, end=500),
        'acc_units': g.numeric.integer_number(start=0, end=500),
        'total_occupied': g.numeric.integer_number(start=0, end=500),
        'regular_vacant': g.numeric.integer_number(start=0, end=50),
        'pha_total_units': g.numeric.integer_number(start=800, end=3000),
        'percent_occupied': str(g.numeric.integer_number(start=0, end=100)),
        'people_per_unit': g.numeric.float_number(start=1.0, end=4.0, precision=2),
        'people_total': g.numeric.integer_number(start=10, end=1500),
        'rent_per_month': g.numeric.integer_number(start=200, end=500),
        'median_inc_amnt': g.numeric.integer_number(start=65000, end=250000),
        'hh_income': g.numeric.integer_number(start=1, end=20000),
        'person_income': g.numeric.integer_number(start=5000, end=18000),
        'pct_lt5k': g.numeric.float_number(start=0, end=50, precision=10),
        'pct_5k_lt10k': g.numeric.float_number(start=0, end=75, precision=10),
        'pct_10k_lt15k': g.numeric.float_number(start=0, end=50, precision=10),
        'pct_15k_lt20k': g.numeric.float_number(start=0, end=40, precision=10),
        'pct_ge20k': g.numeric.float_number(start=0, end=50, precision=10),
        'pct_lt80_median': str(g.numeric.float_number(start=90, end=100, precision=10)),
        'pct_lt50_median': g.numeric.float_number(start=70, end=100, precision=10),
        'pct_lt30_median': g.numeric.float_number(start=50, end=100, precision=10),
        'pct_bed1': g.numeric.float_number(start=0, end=100, precision=10),
        'pct_bed2': g.numeric.float_number(start=0, end=100, precision=10),
        'pct_bed3': g.numeric.float_number(start=0, end=50, precision=10),
        'pct_overhoused': g.numeric.float_number(start=0, end=50, precision=10),
        'tminority': str(g.numeric.float_number(start=10, end=98, precision=10)),
        'tpoverty': str(g.numeric.float_number(start=10, end=80, precision=10)),
        'tpct_ownsfd': str(g.numeric.float_number(start=10, end=98, precision=10)),
        'chldrn_mbr_cnt': g.numeric.integer_number(start=1, end=30),
        'eldly_prcnt': str(g.numeric.float_number(start=0, end=100, precision=10)),
        'pct_disabled_lt62_all': str(g.numeric.float_number(start=0, end=70, precision=10)),
        'national_building_id': g.person.identifier(mask='######0000'),
        'geom': create_point(coords),
        'geom_webmercator': create_point(coords)
    }
    table.append(row)
HUDPublicHousingBuildings_df = pd.DataFrame.from_dict(table)
HUDPublicHousingBuildings_df.to_csv('./csv/HUDPublicHousingBuildings.csv', index=False, encoding='utf-8')


# HUD Public Housing Developments (Allegheny County) - 77
table = []
for i in range(77):
    coords = generate_coords(poly=allegheny)
    row = {
        'development_code': g.person.identifier(mask='PA00######'),
        'longitude': coords[0],
        'latitude': coords[1],
        'geocoding_accuracy': g.choice(['4', 'B', 'R', 'T']),
        'county_fips_code': '42003',
        'census_tract': g.person.identifier(mask='420########'),
        'municipality_fips': g.person.identifier(mask='800######'),
        'municipality_name': g.choice(municipalities),
        'hud_property_name': g.choice([g.finance.company(), g.address.address()]),
        'property_street_address': g.address.address(),
        'city': g.address.city(),
        'state': 'PA',
        'zip_code': g.address.zip_code(),
        'units': g.numeric.integer_number(start=1, end=500),
        'owner_organization_name': 'Housing Authority of ' + g.choice(municipalities),
        'participant_code': g.person.identifier(mask='PA00#'),
        'formal_participant_name': g.finance.company(), 
        'project_name': g.address.street_name(),
        'total_dwelling_units': g.numeric.integer_number(start=1, end=500),
        'acc_units': g.numeric.integer_number(start=0, end=500),
        'total_occupied': g.numeric.integer_number(start=0, end=500),
        'regular_vacant': g.numeric.integer_number(start=0, end=50),
        'pha_total_units': g.numeric.integer_number(start=800, end=3000),
        'percent_occupied': str(g.numeric.integer_number(start=0, end=100)),
        'people_per_unit': g.numeric.float_number(start=1.0, end=4.0, precision=2),
        'people_total': g.numeric.integer_number(start=10, end=1500),
        'rent_per_month': g.numeric.integer_number(start=200, end=500),
        'median_inc_amnt': g.numeric.integer_number(start=65000, end=250000),
        'hh_income': g.numeric.integer_number(start=1, end=20000),
        'person_income': g.numeric.integer_number(start=5000, end=18000),
        'pct_lt5k': g.numeric.float_number(start=0, end=50, precision=10),
        'pct_5k_lt10k': g.numeric.float_number(start=0, end=75, precision=10),
        'pct_10k_lt15k': g.numeric.float_number(start=0, end=50, precision=10),
        'pct_15k_lt20k': g.numeric.float_number(start=0, end=40, precision=10),
        'pct_ge20k': g.numeric.float_number(start=0, end=50, precision=10),
        'pct_lt80_median': str(g.numeric.float_number(start=90, end=100, precision=10)),
        'pct_lt50_median': g.numeric.float_number(start=70, end=100, precision=10),
        'pct_lt30_median': g.numeric.float_number(start=50, end=100, precision=10),
        'pct_bed1': g.numeric.float_number(start=0, end=100, precision=10),
        'pct_bed2': g.numeric.float_number(start=0, end=100, precision=10),
        'pct_bed3': g.numeric.float_number(start=0, end=50, precision=10),
        'pct_overhoused': g.numeric.float_number(start=0, end=50, precision=10),
        'tminority': str(g.numeric.float_number(start=10, end=98, precision=10)),
        'tpoverty': str(g.numeric.float_number(start=10, end=80, precision=10)),
        'tpct_ownsfd': str(g.numeric.float_number(start=10, end=98, precision=10)),
        'chldrn_mbr_cnt': g.numeric.integer_number(start=1, end=30),
        'eldly_prcnt': str(g.numeric.float_number(start=0, end=100, precision=10)),
        'pct_disabled_lt62_all': str(g.numeric.float_number(start=0, end=70, precision=10)),
        'scattered_site_ind': g.choice(['Y', 'N']),
        'pd_status_type_code': 'M',
        'geom': create_point(coords),
        'geom_webmercator': create_point(coords)
    }
    table.append(row)
HUDPublicHousingDevelopments_df = pd.DataFrame.from_dict(table)
HUDPublicHousingDevelopments_df.to_csv('./csv/HUDPublicHousingDevelopments.csv', index=False, encoding='utf-8')


# LIHTC (Pennsylvania) - 1,919
table = []
for i in range(1919):
    coords = generate_coords(poly=allegheny)
    row = {
        'lihtc_project_id': g.person.identifier(mask='PAA########'),
        'normalized_state_id': g.choice([g.person.identifier(mask='TC####-####'), g.person.identifier(mask='PAA########')]),
        'latitude': coords[1],
        'longitude': coords[0],
        'census_tract': g.person.identifier(mask='420########'),
        'census_tract_2000': g.person.identifier(mask='420########'),
        'county_fips_code': g.person.identifier(mask='4200#'),
        'municipality_fips': g.person.identifier(mask='#######'),
        'hud_property_name': g.choice([g.finance.company(), g.address.address()]),
        'property_street_address': g.address.address(),
        'city': g.address.city(),
        'state': 'PA',
        'zip_code': g.address.zip_code(),
        'units': g.numeric.integer_number(start=1, end=700),
        'assisted_units': g.numeric.integer_number(start=0, end=600),
        'count_0br': g.numeric.integer_number(start=1, end=400),
        'count_1br': g.numeric.integer_number(start=1, end=200),
        'count_2br': g.numeric.integer_number(start=1, end=100),
        'count_3br': g.numeric.integer_number(start=1, end=100),
        'count_4br': g.numeric.integer_number(start=1, end=75),
        'federal_id': g.person.identifier(mask='PAA########'),
        'state_id': g.choice([g.person.identifier(mask='TC####-####'), g.person.identifier(mask='PAA########')]),
        'lihtc_credit': g.choice(['70 percent present value', '30 percent present value', 'Both', 'None']),
        'lihtc_construction_type': g.choice(['Acquisition and Rehab', 'New construction']),
        'lihtc_year_allocated': g.numeric.integer_number(start=1980, end=2023),
        'lihtc_year_in_service': g.numeric.integer_number(start=1980, end=2023),
        'lihtc_amount': g.choice(['None', str(g.numeric.integer_number(start=100, end=100000))]),
        'fmha_514_loan': g.choice([True, False, None]),
        'fmha_515_loan': g.choice([True, False, None]),
        'fmha_538_loan': g.choice([True, False, None]),
        'scattered_site_ind': g.choice(['Y', 'N']),
        'geom': create_point(coords),
        'geom_webmercator': create_point(coords)
    }
    table.append(row)
LIHTC_df = pd.DataFrame.from_dict(table)
LIHTC_df.to_csv('./csv/LIHTC.csv', index=False, encoding='utf-8')

# Multifamily Assistance & Section 8 Contracts - 1,066
table = []
for i in range(1066):
    row = {
        'property_id': g.person.identifier(mask='800######'),
        'hud_property_name': g.choice([g.finance.company(), g.address.address()]),
        'assisted_units': g.numeric.integer_number(start=0, end=600),
        'count_0br': g.numeric.integer_number(start=0, end=250),
        'count_1br': g.numeric.integer_number(start=0, end=500),
        'count_2br': g.numeric.integer_number(start=0, end=250),
        'count_3br': g.numeric.integer_number(start=0, end=200),
        'count_4br': g.numeric.integer_number(start=0, end=100),
        'count_5plusbr': g.numeric.integer_number(start=0, end=10),
        'contract_id': g.person.identifier(mask='PA##@@@####'),
        'program_type': g.choice(['202/8 NC', '202/8 SR', '223(a)(7) Refi of 223f ALF', '223(a)(7) Refi of 223f Nursing/ ICF']),
        'subsidy_start_date': g.datetime.formatted_date(fmt="%Y-%m-%d", start=1980, end=2023),
        'subsidy_expiration_date': g.datetime.formatted_date(fmt="%Y-%m-%d", start=2020, end=2043),
        'contract_duration_months': g.numeric.integer_number(start=2, end=660)
    }
    table.append(row)
MultifamilyAssistanceAndSection8Contracts_df = pd.DataFrame.from_dict(table)
MultifamilyAssistanceAndSection8Contracts_df.to_csv('./csv/MultifamilyAssistanceAndSection8Contracts.csv', index=False, encoding='utf-8')


# Subsidy extract from HUD Insured Multifamily - 85
table = []
for i in range(85):
    coords = generate_coords(poly=allegheny)
    row = {
        'property_id': g.person.identifier(mask='800######'),
        'latitude': coords[1],
        'longitude': coords[0],
        'geocoding_accuracy': 'R',
        'county': 'Allegheny',
        'county_fips_code': '42003',
        'congressional_district_code': str(g.numeric.integer_number(start=12, end=18)),
        'census_tract': g.person.identifier(mask='420########'),
        'municipality_fips': g.person.identifier(mask='800######'),
        'municipality_name': g.choice(municipalities),
        'hud_property_name': g.choice([g.finance.company(), g.address.address()]),
        'property_street_address': g.address.address(),
        'city': g.address.city(),
        'state': 'PA',
        'zip_code': g.address.zip_code(),
        'units': g.numeric.integer_number(start=1, end=350),
        'assisted_units': g.numeric.integer_number(start=0, end=200),
        'occupancy_date': g.datetime.formatted_date(fmt="%Y-%m-%d", start=1968, end=2020),
        'property_category_name': g.choice(['Insured-Subsidized', 'Insured-Unsubsidized']),
        'property_manager_name': g.person.full_name(),
        'property_manager_company': g.finance.company(),
        'property_manager_address': g.address.address(),
        'property_manager_phone': g.person.phone_number(mask='(412) ###-####'),
        'property_manager_email': g.person.email(),
        'contract_id': g.person.identifier(mask='PA##@@@####'),
        'program_type': g.choice(['202/8 NC', '202/8 SR', '223(a)(7) Refi of 223f ALF', '223(a)(7) Refi of 223f Nursing/ ICF']),
        'subsidy_units': g.numeric.integer_number(start=0, end=200),
        'subsidy_expiration_date': g.datetime.formatted_date(fmt="%Y-%m-%d", start=2020, end=2043),
        'count_0br': g.numeric.integer_number(start=0, end=250),
        'count_1br': g.numeric.integer_number(start=0, end=500),
        'count_2br': g.numeric.integer_number(start=0, end=250),
        'count_3br': g.numeric.integer_number(start=0, end=200),
        'count_4br': g.numeric.integer_number(start=0, end=100),
        'count_5plusbr': g.numeric.integer_number(start=0, end=10),
        'servicing_site_name_loan': g.choice(['Baltimore', 'Pittsburgh', 'OHP']),
        'inspection_id': g.numeric.integer_number(start=500000, end=700000),
        'inspection_score': g.numeric.integer_number(start=25, end=100),
        'client_group_name': g.choice(['Assisted Living Care', 'Elderly', 'Family & Elderly', 'Indv. families - not eld/ handicap	']),
        'client_group_type': g.choice(['Family', 'Elderly', 'None']),
        'geom': create_point(coords),
        'geom_webmercator': create_point(coords)
    }
    table.append(row)
SubsidyExtractFromHUDInsuredMultifamilyProperties_df = pd.DataFrame.from_dict(table)
SubsidyExtractFromHUDInsuredMultifamilyProperties_df.to_csv('./csv/SubsidyExtractFromHUDInsuredMultifamilyProperties.csv', index=False, encoding='utf-8')


# Subsidy extract from Multifamily Assistance - 216
table = []
for i in range(216):
    row = {
        'property_id': g.person.identifier(mask='800######'),
        'county_fips_code': '42003',
        'county': 'Allegheny',
        'congressional_district_code': str(g.numeric.integer_number(start=12, end=18)),
        'municipality_name': g.choice(municipalities),
        'hud_property_name': g.choice([g.finance.company(), g.address.address()]),
        'property_street_address': g.address.address(),
        'city': g.address.city(),
        'state': 'PA',
        'zip_code': g.address.zip_code(),
        'units': g.numeric.integer_number(start=1, end=500),
        'property_category_name': g.choice(['Insured-Subsidized', 'Insured-Unsubsidized']),
        'owner_organization_name': 'Housing Authority of ' + g.choice(municipalities),
        'owner_address': "%s, %s, %s %s" % (g.address.address(), g.address.city(), g.address.state(abbr=True), g.address.zip_code()),
        'owner_phone': g.person.phone_number(mask='(412) ###-####'),
        'owner_type': g.choice(['Limited Dividend', 'Non-Profit', 'Profit Motivated']),
        'owner_effective_date': g.datetime.formatted_date(fmt="%Y-%m-%d", start=1964, end=2022),
        'owner_id': g.numeric.integer_number(start=1500, end=422999),
        'property_manager_name': g.person.full_name(),
        'property_manager_company': g.finance.company(),
        'property_manager_address': g.address.address(),
        'property_manager_phone': g.person.phone_number(mask='(412) ###-####'),
        'property_manager_email': g.person.email(),
        'property_manager_type': g.choice(['Limited Dividend', 'Non-Profit', 'Profit Motivated']),
        'servicing_site_name': g.choice(['Baltimore', 'Pittsburgh', 'OHP']),
    }
    table.append(row)
SubsidyExtractFromMultifamilyAssistanceAndSection8Contracts_df = pd.DataFrame.from_dict(table)
SubsidyExtractFromMultifamilyAssistanceAndSection8Contracts_df.to_csv('./csv/SubsidyExtractFromMultifamilyAssistanceAndSection8Contracts.csv', index=False, encoding='utf-8')


# LIHTC Data from PHFA (Allegheny County) - 103
table = []
for i in range(103):
    row = {
        'pmindx': g.numeric.integer_number(start=200, end=7000),
        'hud_property_name': g.choice([g.finance.company(), g.address.address()]),
        'assisted_units': g.numeric.integer_number(start=0, end=200),
        'total_lihtc_allocation': g.numeric.integer_number(start=0, end=15000000),
        'unit_restriction': g.choice(['0% at 0% AMI', '20% at 50% AMI', '40% at 60% AMI']),
        'lihtc_credit': g.choice(['30 percent present value', '70 percent present value']),
        'lihtc_year_allocated': g.numeric.integer_number(start=1990, end=2020),
        'lihtc_year_in_service': g.numeric.integer_number(start=1995, end=2020),
        'last_year_of_rca': g.numeric.integer_number(start=2020, end=2050)
    }
    table.append(row)
LIHTCDataFromPHFA_df = pd.DataFrame.from_dict(table)
LIHTCDataFromPHFA_df.to_csv('./csv/LIHTCDataFromPHFA.csv', index=False, encoding='utf-8')


# Demographics by Housing Project from PHFA.. - 166
table = []
for i in range(166):
    row = {
        'property_id': g.person.identifier(mask='800######'),
        'pmindx': g.numeric.integer_number(start=200, end=10800),
        'normalized_state_id': g.person.identifier(mask='TC####-####'),
        'fha_loan_id': g.person.identifier(mask='033#####'),
        'application_number': g.choice([g.person.identifier(mask='TC####-####'), g.person.identifier(mask='N-#### / TC####-####'), g.person.identifier(mask='Y-#### / TC####-####')]),
        'state_id': g.person.identifier(mask='TC####-####'),
        'contract_id': g.person.identifier(mask='PA##@@@####'),
        'hud_property_name': g.choice([g.finance.company(), g.address.address()]),
        'property_street_address': g.address.address(),
        'city': g.address.city(),
        'state': 'PA',
        'zip_code': g.address.zip_code(),
        'owner_organization_name': 'Housing Authority of ' + g.choice(municipalities),
        'assisted_units': g.numeric.integer_number(start=0, end=600),
        'demographic': g.choice(['General', 'Elderly']),
        'physical_disability_housing': g.choice([True, False]),
        'mental_disability_housing': g.choice([True, False]),
        'homeless_housing': g.choice([True, False]),
        'owner_representative': g.finance.company(),
        'property_manager_company': g.finance.company(),
        'scattered_sites': g.choice([True, None])
    }
    table.append(row)
DemographicsByHousingProjectFromPHFA_df = pd.DataFrame.from_dict(table)
DemographicsByHousingProjectFromPHFA_df.to_csv('./csv/DemographicsByHousingProjectFromPHFA.csv', index=False, encoding='utf-8')


# Apartment Distributions, Income Limits, and.. - 157
table = []
for i in range(157):
    row = {
        'pmindx': g.numeric.integer_number(start=200, end=10800),
        'hud_property_name': g.choice([g.finance.company(), g.address.address()]),
        'total_units': g.numeric.integer_number(start=10, end=350),
        'count_0br': g.numeric.integer_number(start=1, end=200),
        'count_1br': g.numeric.integer_number(start=1, end=200),
        'count_2br': g.numeric.integer_number(start=1, end=200),
        'count_3br': g.numeric.integer_number(start=1, end=200),
        'count_4br': g.numeric.integer_number(start=1, end=200),
        'count_5br': g.numeric.integer_number(start=1, end=10),
        'count_6br': g.numeric.integer_number(start=1, end=10),
        'plus_1_manager_unit': 1,
        'number_20percent_ami_limit': g.numeric.integer_number(start=1, end=20),
        'number_30percent_ami_limit': g.numeric.integer_number(start=1, end=10),
        'number_40percent_ami_limit': g.numeric.integer_number(start=1, end=50),
        'number_50percent_ami_limit': g.numeric.integer_number(start=1, end=200),
        'number_60percent_ami_limit': g.numeric.integer_number(start=1, end=200),
        'number_80percent_ami_limit': g.numeric.integer_number(start=1, end=200),
        'market_rate': g.numeric.integer_number(start=1, end=200),
        'other_income_limit': g.numeric.integer_number(start=1, end=200),
        'uncategorized_income_limit': g.numeric.integer_number(start=1, end=350),
        'units_w_section_811_subsidy': g.numeric.integer_number(start=1, end=10),
        'units_w_section_8_fair_market_rent': g.numeric.integer_number(start=1, end=50),
        'units_w_housing_vouchers': g.numeric.integer_number(start=1, end=75),
        'units_w_staff_unit': 1,
        'units_w_other_subsidy_type': g.numeric.integer_number(start=1, end=200),
        'units_w_project_based_section_8_certificate': g.numeric.integer_number(start=1, end=350),
        'units_w_uncategorized_subsidy': g.numeric.integer_number(start=1, end=250),
    }
    table.append(row)
PHFAStats_df = pd.DataFrame.from_dict(table)
PHFAStats_df.to_csv('./csv/PHFAStats.csv', index=False, encoding='utf-8')


""" Lookup Tables """

# Helper function to get IDs from data table
def get_ids(project_ids=list) -> tuple:
    n = len(project_ids)
    min = 75
    num_ids = random.randint(min, n)
    num_projects = 650
    multiplier = ceil(num_ids / num_projects)
    index_ids = random.sample(range(0, multiplier * num_projects), num_ids)
    return num_ids, index_ids, random.sample(project_ids, num_ids)


# Helper function for generating lookup tables
def generate_table(num_ids=int, project_ids=list, index_ids=list) -> pd.DataFrame:
    table = []
    for i in range(num_ids):
        row = {
            'projectidentifier_id': project_ids[i],
            'projectindex_id': index_ids[i]
        }
        table.append(row)
    
    return pd.DataFrame.from_dict(table)


# house_cat_projectindex_lihtc_project_id - 239
lihtc_ids = LIHTC_df['lihtc_project_id'].to_list()
num_ids, index_ids, project_ids = get_ids(lihtc_ids)
df = generate_table(num_ids, index_ids, project_ids)
df.to_csv('./csv/LIHTCProjectID.csv', index=False, encoding='utf-8')

# house_cat_projectindex_development_code - 77
development_ids = HUDPublicHousingBuildings_df['development_code'].to_list()
num_ids, index_ids, project_ids = get_ids(development_ids)
df = generate_table(num_ids, index_ids, project_ids)
df.to_csv('./csv/DevelopmentCode.csv', index=False, encoding='utf-8')

# house_cat_projectindex_fha_loan_id - 172
fha_loan_ids = HUDMultifamilyFiscalYearProduction_df['fha_loan_id'].to_list()
num_ids, index_ids, project_ids = get_ids(fha_loan_ids)
df = generate_table(num_ids, index_ids, project_ids)
df.to_csv('./csv/FHALoanID.csv', index=False, encoding='utf-8')

# house_cat_projectindex_normalized_state_id - 241
normalized_state_ids = LIHTC_df['normalized_state_id'].to_list()
num_ids, index_ids, project_ids = get_ids(normalized_state_ids)
df = generate_table(num_ids, index_ids, project_ids)
df.to_csv('./csv/NormalizeStateID.csv', index=False, encoding='utf-8')

# house_cat_projectindex_contract_id - 95
contract_ids = MultifamilyAssistanceAndSection8Contracts_df['contract_id'].to_list()
num_ids, index_ids, project_ids = get_ids(contract_ids)
df = generate_table(num_ids, index_ids, project_ids)
df.to_csv('./csv/ContractID.csv', index=False, encoding='utf-8')

# house_cat_projectindex_pmindx - 165
pmindx_ids = LIHTCDataFromPHFA_df['pmindx'].to_list()
num_ids, index_ids, project_ids = get_ids(pmindx_ids)
df = generate_table(num_ids, index_ids, project_ids)
df.to_csv('./csv/PMIndx.csv', index=False, encoding='utf-8')
