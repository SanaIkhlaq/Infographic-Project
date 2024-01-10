import pandas as pd
import matplotlib.pyplot as plt
import seaborn

plt.figure(figsize=(12, 12))
gs = plt.GridSpec(3, 2, figure=plt.gcf())

# Define project title
project_title = ('Unveiling Climate Change in Angola (1990-2015): Visualizing'
                 ' Influential Factors and Trends\n '
                 'Name: Sana Ikhlaq, Student ID: 22075278')

# Set super title
plt.suptitle(project_title, fontsize=12, fontweight='bold')


def get_data(filename, country_codes, indicator_name):
    """
    This function load the dataset from excel file, filter dataset for the
    input indicator, convert the years columns to rows by using melt function,
    clean the dataframe records for any empty or missing valus and then
    return the original and cleaned data dataframes.
    :param filename:
    :param country_codes:
    :param indicator_name:
    :return: df, cleaned_data_df
    """

    # Read data
    df = pd.read_excel(filename, skiprows=3)

    # Select data for required indicator code
    indicators = df.loc[df['Indicator Code'].eq(indicator_name)]

    # Select data by country codes
    countries = indicators.loc[indicators['Country Code'].isin(country_codes)]

    # Convert year columns into rows
    final_data = countries.melt(id_vars=['Country Name', 'Country Code',
                                         'Indicator Name', 'Indicator Code'])

    # Make Year column
    final_data['Year'] = final_data['variable']

    # Clean data
    cleaned_data_df = final_data.dropna()

    return df, cleaned_data_df


def show_population_growth():
    """
    This function shows the population growth for the country Angola.
    :return: None
    """
    country = 'Angola'
    country_code = 'AGO'

    file = 'API_SP.POP.GROW_DS2_en_excel_v2_6299499.xls'

    # Call the function to get dataframes
    df, data = get_data(file, [country_code], 'SP.POP.GROW')

    # Filter data
    df_2 = data.loc[data['Country Code'].eq(country_code)]

    # Convert column datatype to integer
    df_2['Year'] = df_2['Year'].astype(int)

    years = df_2['Year'].values[20:-2]

    population = df_2['value'].values[20:-2]

    plt.subplot(gs[0, 0])
    # plt.figure()
    plt.title(f"{country} - Population Growth from 1990 to 2015")
    plt.plot(years, population, label='Angola')
    plt.xlabel('Years')
    plt.ylabel('Annual Population Growth')
    plt.xlim(1990, 2016)
    plt.legend()
    # plt.show()


def show_avg_temperature_line_plot():
    """
    This function load the dataset and show the temperature for
    country Angola from 1990 to 2015.
    """
    filename = 'global_land_temperatures_city.csv'
    df_temp = pd.read_csv(filename, delimiter=",", encoding='utf8')

    country = 'Angola'
    country_code = 'AGO'

    df2_temp = df_temp[df_temp["Country"] == country]

    df2_temp = df2_temp.dropna()

    df2_temp['Date'] = pd.to_datetime(df2_temp['dt'])

    df2_temp['Year'] = df2_temp['Date'].dt.year

    df2_temp = df2_temp[df2_temp['Year'] > 1989]
    df2_temp = df2_temp[df2_temp['Year'] < 2016]

    df2_temp = df2_temp.sort_values(by='Date')

    # plt.figure()
    plt.subplot(gs[0, 1])
    plt.plot(df2_temp['Date'], df2_temp['AverageTemperature'], label="Angola")
    title = f'{country} - Average Temperature from 1990 to 2015'
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel('Average Temperature (°C)')
    plt.legend(loc='lower right')
    # plt.show()


def forest_area_decline_stackedbar():
    file = 'API_AG.LND.FRST.K2_DS2_en_excel_v2_6299507.xls'
    country = 'Angola'
    code = 'AGO'

    # Call the function to get dataframes
    df, data = get_data(file, [code], 'AG.LND.FRST.K2')

    # Convert column datatype to integer
    data['Year'] = data['Year'].astype(int)

    data = data[data['Year'] > 1990]
    data = data[data['Year'] < 2016]

    plt.subplot(gs[1, 0])

    plt.stackplot(data['Year'], data['value'], color='orange')
    # plt.plot(data['Year'], data['value'], marker='o', color='b')

    plt.title(f'{country} - Decline in Forest Area from 1990 to 2015')
    plt.xlabel('Years')
    plt.ylabel('Forest Area (Square KM)')
    plt.legend(labels=['Forest Area Decline'])
    plt.grid(True)
    plt.tight_layout()
    # plt.show()


def nitrous_oxide_emission():
    file = 'API_EN.ATM.NOXE.KT.CE_DS2_en_excel_v2_6299147.xls'
    country = 'Angola'
    country_code = 'AGO'

    # Call the function to get dataframes
    df, data = get_data(file, [country_code], 'EN.ATM.NOXE.KT.CE')

    # Convert column datatype to integer
    data['Year'] = data['Year'].astype(int)

    data = data[data['Year'] > 1990]
    data = data[data['Year'] < 2016]

    plt.subplot(gs[1, 1])

    # plt.bar(data['Year'], data['value'], color='b')
    plt.plot(data['Year'], data['value'])

    plt.title(f'{country} - Nitrous Oxide Emissions from 1990 to 2015')
    plt.xlabel('Years')
    plt.ylabel('NO Emission (thousand metric tons)')
    plt.legend(labels=['Nitrous Oxide Emission'], loc='lower right')
    plt.tight_layout()
    # plt.show()


# Visualizations Description
desc = "This infographic aims to show the climate change in Angola between " \
       "1990 to 2015 and the factors influencing the climate change. In " \
       "the following visualizations, the rise and fall of temperature " \
       "can be mainly attributed to increase in population and emission " \
       "of nitrous oxide.\n\nVisualisation A: Shows how the temperature is " \
       "changing with passage of the years.\n\nVisualisation B: Shows how " \
       "average population has grown over the decades. Population rise was " \
       "highest in 2012 over the period.\n\nVisualisation C: The " \
       "supporting line chart shows the main factor for change in " \
       "climate: rise in Nitrous oxide emission  which is 19% over the " \
       "decades.\n\nVisualisation D: It depicts that forest area of the " \
       "country decrease by 12% over the period influencing the country's" \
       " temperature change."

# Show visualization summaries of all 4 plots.
plt.figtext(0.01, 0.10, desc, wrap=True, ha='left', fontsize=12)

show_population_growth()
show_avg_temperature_line_plot()
forest_area_decline_stackedbar()
nitrous_oxide_emission()

plt.savefig('22075278.png', dpi=300)
plt.show()
