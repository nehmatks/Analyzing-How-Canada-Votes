import pandas as pd

def process_all_years():
    # Process Voter Turnout Data
    # Open CSV file with pandas
    print("Processing voter turnout data...")
    df_turnout = pd.read_csv('q3_turnout_by_age_gender_and_province.csv')
    
    # Strip whitespace from all text columns used for filtering
    df_turnout['GENDER_E'] = df_turnout['GENDER_E'].astype(str).str.strip()
    df_turnout['AGE_GROUP_E'] = df_turnout['AGE_GROUP_E'].astype(str).str.strip()
    df_turnout['PROVINCE_E'] = df_turnout['PROVINCE_E'].astype(str).str.strip()
    
    # Only keep rows that have to do with the question
    df_turnout = df_turnout[
        (df_turnout['GENDER_E'] == 'All genders') & 
        (df_turnout['AGE_GROUP_E'] == 'All ages') &
        (df_turnout['PROVINCE_E'] != 'Canada')
    ].copy() # Copy these into a new spreadsheet
    
    # Diagnostic check
    print(f"Found {len(df_turnout)} usable turnout rows after filtering.")
    
    # Only keep columns that have to do with the question
    df_turnout['Turnout_%'] = pd.to_numeric(df_turnout['TURNOUT_ELIGIBLE_ELECTOR'], errors='coerce') * 100
    df_turnout_clean = df_turnout[['YEAR', 'PROVINCE_E', 'Turnout_%']].rename(
        columns={'PROVINCE_E': 'Province', 'YEAR': 'Year'} # Rename header rows
    )


    # Process Hourly Wage Data
    print("\nProcessing wage data...")
    df_wage = pd.read_csv('q3_job_wages.csv')
    
    # Strip whitespace from all text columns 
    df_wage['GEO'] = df_wage['GEO'].astype(str).str.strip()
    df_wage['North American Industry Classification System (NAICS)'] = df_wage['North American Industry Classification System (NAICS)'].astype(str).str.strip()
    df_wage['Statistics'] = df_wage['Statistics'].astype(str).str.strip()
    
    # Only keep colums of interest
    df_wage = df_wage[
        (df_wage['North American Industry Classification System (NAICS)'] == 'Total, all industries') &
        (df_wage['Statistics'] == 'Average offered hourly wage') &
        (df_wage['GEO'] != 'Canada')
    ].copy() 
    
    print(f"Found {len(df_wage)} usable wage rows after filtering.")
    
    df_wage['VALUE'] = pd.to_numeric(df_wage['VALUE'], errors='coerce')
    df_wage['Year'] = df_wage['REF_DATE'].astype(str).str[:4].astype(int) # Gets the date in "0000-00" grabs the year
    
    # Group the data by year and calculate the mean
    yearly_wages = df_wage.groupby(['Year', 'GEO'])['VALUE'].mean().reset_index()
    yearly_wages = yearly_wages.rename(columns={'VALUE': 'Avg_Wage'})
    
    # Take the previous year's wages to compare 
    prev_yearly_wages = yearly_wages.copy()
    prev_yearly_wages['Year'] = prev_yearly_wages['Year'] + 1 
    prev_yearly_wages = prev_yearly_wages.rename(columns={'Avg_Wage': 'Avg_Wage_Prev'})
    
    # Lines up the year's wages directly next to the previous year's wages
    wage_growth_df = pd.merge(yearly_wages, prev_yearly_wages, on=['Year', 'GEO'], how='inner')
    wage_growth_df['Wage_Growth_%'] = ((wage_growth_df['Avg_Wage'] / wage_growth_df['Avg_Wage_Prev']) - 1) * 100
    
    df_wage_clean = wage_growth_df[['Year', 'GEO', 'Wage_Growth_%']].rename(columns={'GEO': 'Province'})


    # Merge and Output Data
    print("\nMerging datasets...")
    
    # Merge on both columns
    final_df = pd.merge(df_turnout_clean, df_wage_clean, on=['Province', 'Year'], how='inner')
    
    # Sort the spreadsheet chronologically and round the numbers to 2 decimals
    final_df = final_df.sort_values(by=['Year', 'Province']).round(2)
    
    output_filename = 'q3_visualization_data_all_years.csv'
    final_df.to_csv(output_filename, index=False) # save to the intermediate CSV file
    
    # Check if the new CSV file has been populated
    if final_df.empty:
        print("\nError: The final dataset is still empty.")
        print("This means the Years or Provinces in the files do not match. Check the row counts above.")
    else:
        print(f"\nData successfully processed")
        print(final_df.head(15).to_string(index=False)) 

# Run the function
process_all_years()