import time
import calendar
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def is_valid(item, item_list):
    """
    Checks whether user input is valid. Otherwise a loop starts until input becomes valid.

    Arguments:
        (str) item - variable that stores the user response
        (list) item_list - a list of valid inputs a user is expected to enter

    Returns:
        (str) item - updated variable with valid input collected from the user.
    """
    print('\nAssessing your response...')

    while item not in item_list:
        print('Oops! Wrong input detected: \'{}\''.format(item))
        item = input('Please select one: {}\n--> '.format(' <-> '.join(item_list).title())).lower()
        print('\nAssessing your response...')

    print('Great Work!! \'{}\' right? Duly noted'.format(item).title())

    return item

def stat_calculator(df, col = 0):
    """
    Computes modal value, its count and percentage from specified column of a dataframe

    Arguments:
        (dataframe) df - dataframe from which to select column
        (str) col - name of column to select from dataframe

    Returns:
        (str) common - the modal value
        (int) common_count - frequency of modal value as count
        (int) common_pcent - frequency of modal value as percentage (2 decimal places)
    """
    # if no column is given treat the dataframe like a series
    if col == 0:
        common = df.mode()[0]
        common_count = df[df == common].count()
        common_pcent = (common_count / df.count()) * 100

    else:
        common = df[col].mode()[0]
        common_count = df[col][df[col] == common].count()
        common_pcent = (common_count / df[col].count()) * 100

    common_pcent = '{:.2f}'.format(common_pcent)

    return common, common_count, common_pcent

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello there! Let\'s explore some US bikeshare data!\n')

    # define the valid entries for City, Month and Weekday
    valid_cities = CITY_DATA.keys()
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

    # get user input for city ( HINT: Use a while loop to handle invalid inputs
    print('I have information from three cities: Chicago, New York City and Washington\n')
    print('Which city would you like to explore?')
    city = input('Enter your response here --> ').lower()

    # check the validity of user entry for City
    city = is_valid(city, valid_cities)

    # get user input for month (all, january, february, ... , june)
    print('\nI also have information for all months from January to June\n')
    print('Any particular month of interest? If not, please enter the keyword \'All\'')
    month = input('Enter your response here --> ').lower()

    # check the validity of user entry for month
    month = is_valid(month, valid_months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('One more thing! You can filter my analysis by any day from Monday to Sunday\n')
    print('Any particular day of interest? If not, please enter the keyword \'All\'')
    day = input('Enter your response here --> ').lower()

    # check the validity of user entry for Weekday
    day = is_valid(day, valid_days)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # calculate and display the most common month statistics with count and %
    common_month, common_month_count, common_month_pcent = stat_calculator(df, 'month')

    print('The most common month is {}; Count: {}; Percentage: {}%'\
    .format(calendar.month_name[common_month], common_month_count, common_month_pcent))

    # calculate and display the most common day of week statistics with count and %
    common_dow, common_dow_count, common_dow_pcent = stat_calculator(df, 'day_of_week')

    print('The most common day is {}; Count: {}; Percentage: {}%'\
    .format(common_dow, common_dow_count, common_dow_pcent))

    # calculate and display the most common start hour statistics with count and %
    hour = df['Start Time'].dt.hour
    common_hr, common_hr_count, common_hr_pcent = stat_calculator(hour)

    print('The most common hour is {}:00 hrs; Count: {}; Percentage: {}%'\
    .format(common_hr, common_hr_count, common_hr_pcent))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # calculate and display the most common start station statistics with count and %
    common_start_station, common_start_station_count,\
    common_start_station_pcent = stat_calculator(df, 'Start Station')

    print('The most commonly used start station is: {}; Count: {}; Percentage: {}%'\
    .format(common_start_station, common_start_station_count, common_start_station_pcent))

    # calculate and display the most common end station statistics with count and %
    common_end_station, common_end_station_count,\
    common_end_station_pcent = stat_calculator(df, 'End Station')

    print('The most commonly used end station is: {}; Count: {}; Percentage: {}%'\
    .format(common_end_station, common_end_station_count, common_end_station_pcent))

    # calculate and display the most common trips with count and %
    trips = 'From: ' + df['Start Station'] + ', To: ' + df['End Station']
    common_trips, common_trips_counts, common_trips_percent = stat_calculator(trips)

    print('The most common trips are {}; Count: {}; Percentage: {}%'\
    .format(common_trips, common_trips_counts, common_trips_percent))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time is {} seconds'.format(df['Trip Duration'].sum()))

    # display mean travel time
    print('The average travel time is {} seconds'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('Here are the different user types expressed in counts: \n{}\n'.format(user_types))
    print('As percentages:')
    print(df['User Type'].value_counts(normalize=True).mul(100).round(2).astype(str)+'%')

    # Display counts of gender
    print('\nCalculating Gender Stats ...\n')

    if 'Gender' in df:
        # Account for the null values in the gender column then print the count result
        gender = df['Gender'].fillna('Missing data')
        print('\nHere is the gender distribution of the users expressed in counts:')
        print(gender.value_counts())
        print('\nAs percentages:')
        print(gender.value_counts(normalize=True).mul(100).round(2).astype(str)+'%')

    else:
        print('This City has no data for gender')

    # Display earliest, most recent, and most common year of birth
    print('\nCalculating Birth Year Stats \n')

    if 'Birth Year' in df:

        print('Birth Year Statistics')
        print('Earliest Year: {}'.format(int(df['Birth Year'].min())))
        print('Most Recent Year: {}'.format(int(df['Birth Year'].max())))
        print('Most Common Year: {}'.format(int(df['Birth Year'].mode()[0])))
        print('Note: {} records are missing from the data'.format(df['Birth Year'].isnull().sum()))
    else:
        print('This City has no data for birth year')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """ Allows users to veiw raw data. 5 rows are displayed at each time"""

    answer = input('Would you love to see some of the raw data? Enter y/n --> ').lower()
    answer = is_valid(answer, ['y','n'])
    counter = 0

    #Start loop based on user response
    while answer == 'y':
        print('\nLoading the first five rows...\n')

        while counter < df.size and answer == 'y':
            print('Querying memory...\n')
            print(df[counter: counter+5])
            counter +=5
            answer = input('Would you love to see some more? Enter y/n --> ').lower()
            answer = is_valid(answer, ['y','n'])

        # End loop and notify the user when there is no more data to display
            if counter > df.size:
                print('\nOops! There is nothing more to display')
                break

    print('\nAlright, stopping right away ...')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no --> ').lower()
        restart = is_valid(restart, ['yes','no'])
        if restart != 'yes':
            break

    print('\n', '-'*40, '\nTHANK YOU FOR YOUR TIME\n', 'Come Back Again Soon!')

if __name__ == "__main__":
    main()
