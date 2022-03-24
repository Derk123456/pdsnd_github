import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

month_dict = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
month_dict_rev = {1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june'}

weekday_dict = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5,
                'sunday': 6}
weekday_dict_rev = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 4: 'friday', 5: 'saturday',
                    6: 'sunday'}


def data_check(element_list, str_text):
    """
    Input sequence which checks the data and reruns the input if necessary

    Args:
        (list) element_list - list of acceptable input data as strings
        (str) str_text - text which is displayed in the input
    Returns:
        (str) variable - allowed input
    """
    while 1:
        variable = input(str_text)
        if variable.lower() in element_list:
            break
        else:
            print('Please choose one of the possible definitions as written below.')
            continue
    return variable.lower()


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
        (str) filter_name - name of the chosen filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_list = ['chicago', 'new york city', 'washington']
    text = 'Choose one of the following cities: Chicago, New York City or Washington: '
    city = data_check(city_list, text)

    # get user input for filter
    filter_list = ['month', 'day', 'both', 'none']
    text = 'Would you like to filter the data by month, day, both or not at all?\nType "None" for no time filter: '
    filter_name = data_check(filter_list, text)

    # get user input for month (january, february, ... , june)
    if filter_name == 'month' or filter_name == 'both':
        month_list = ['january', 'february', 'march', 'april', 'may', 'june']
        text = 'Choose the month: January, February, ... , June: '
        month = data_check(month_list, text)
    else:
        month = None

    # get user input for day of week (monday, tuesday, ... sunday)
    if filter_name == 'day' or filter_name == 'both':
        day_list = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
        text = 'Choose the weekday: Monday, Tuesday, ... Sunday: '
        day = data_check(day_list, text)
    else:
        day = None

    print('-' * 40)
    return city, month, day, filter_name


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

    # Load data from csv file into DataFrame
    df = pd.read_csv(CITY_DATA[city.lower()])

    # Convert start time to datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Additional columns for month, weekday and hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['hour'] = df['Start Time'].dt.hour

    # Additional column connection start station - end station
    df['start - end'] = df['Start Station'] + ' -> ' + df['End Station']

    if month is not None:
        df = df[df['month'] == month_dict[month]]

    if day is not None:
        df = df[df['day_of_week'] == weekday_dict[day]]

    return df


def time_stats(df, chosen_filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    # display count number common hour
    count_hour = df[df['hour'] == popular_hour]['hour'].count()

    # display the most common month
    popular_month = df['month'].mode()[0]
    pop_month_name = month_dict_rev[popular_month].title()
    # display count number common month
    count_month = df[df['month'] == popular_month]['month'].count()

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    pop_day_name = weekday_dict_rev[popular_day].title()
    # display count number common day of week
    count_day = df[df['day_of_week'] == popular_month]['day_of_week'].count()

    if chosen_filter == 'both':
        print('Most popular hour: {}, Count: {}, Filter: {}'.format(popular_hour, count_hour, chosen_filter))
    elif chosen_filter == 'month':
        print(
            'Most popular day of week: {}, Count: {}, Most popular hour: {}, Count: {}, Filter: {}'.format(pop_day_name,
                                                                                                           count_day,
                                                                                                           popular_hour,
                                                                                                           count_hour,
                                                                                                           chosen_filter))
    elif chosen_filter == 'day':
        print('Most popular month: {}, Count: {}, Most popular hour: {}, Count: {}, Filter: {}'.format(pop_month_name,
                                                                                                       count_month,
                                                                                                       popular_hour,
                                                                                                       count_hour,
                                                                                                       chosen_filter))
    else:
        print('Most popular month: {}, Count: {}, Most popular day of week: {}, Count: {}, Most popular hour: {}, '
              'Count: {}, Filter: {}'.format(pop_month_name, count_month, pop_day_name, count_day, popular_hour,
                                             count_hour, chosen_filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df, chosen_filter):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    pop_start_station = df['Start Station'].mode()[0]
    count_start_station = df[df['Start Station'] == pop_start_station]['Start Station'].count()

    # display most commonly used end station
    pop_end_station = df['End Station'].mode()[0]
    count_end_station = df[df['End Station'] == pop_end_station]['End Station'].count()

    # display most frequent combination of start station and end station trip
    pop_connection = df['start - end'].mode()[0]
    count_connection = df[df['start - end'] == pop_connection]['start - end'].count()

    print('Start Station: {}, Count: {} - End Station: {}, Count: {}, Filter: {}'.format(pop_start_station,
                                                                                         count_start_station,
                                                                                         pop_end_station,
                                                                                         count_end_station,
                                                                                         chosen_filter))
    print('Trip: ({}), Count: {}, Filter: {}'.format(pop_connection, count_connection, chosen_filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df, chosen_filter):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_duration = df['Trip Duration'].sum()

    # display mean travel time
    avg_duration = df['Trip Duration'].mean()

    # number of entries
    count_entries = df['Trip Duration'].count()

    print('Total Duration: {}, Count: {}, Avg Duration: {}, Filter: {}'.format(total_duration, count_entries,
                                                                               avg_duration, chosen_filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, chosen_filter):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    count_subscribers = df[df['User Type'] == 'Subscriber']['User Type'].count()
    count_customers = df[df['User Type'] == 'Customer']['User Type'].count()

    if 'Gender' in df:
        # Display counts of gender
        count_male = df[df['Gender'] == 'Male']['Gender'].count()
        count_female = df[df['Gender'] == 'Female']['Gender'].count()
        print('Male: {}, Female: {}, Filter: {}'.format(count_male, count_female, chosen_filter))

    if 'Birth Year' in df:
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        pop_birth_year = int(df['Birth Year'].mode()[0])
        count_birth_year = df[df['Birth Year'] == pop_birth_year]['Birth Year'].count()
        print(
            'Earliest Birth Year: {}, Most recent Birth Year: {}, Most Common Birth Year: {}, Count: {}, Filter: {}'.format(
                earliest_birth_year, recent_birth_year, pop_birth_year, count_birth_year, chosen_filter))

    print('Subscribers: {}, Customers: {}, Filter: {}'.format(count_subscribers, count_customers, chosen_filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def raw_data(df):
    """ Shows raw data on demand. """

    show_data = input('Do you want to see the raw data? Type "Yes" or "No".')
    df = df.fillna('no information')
    x = 0
    if 'Gender' in df and 'Birth Year' in df:
        while show_data.lower() != 'no':
            for x in range(x, x + 5):
                print('-' * 40 + '\n"" : {},\nBirth Year: {},\nEnd Station: {},\nEnd Time: {},\nGender: {},\nStart '
                                 'Station: {},\nStart Time: {},\nTrip Duration: {},\nUser Type: {}\n'.format(
                    df.iloc[x][0], df.iloc[x][8], df.iloc[x][5], df.iloc[x][2], df.iloc[x][7],
                    df.iloc[x][4], df.iloc[x][1], df.iloc[x][3], df.iloc[x][6]))
            show_data = input('Do you want to see more entries? Type "Yes" or "No".')
            x += 1
    else:
        while show_data.lower() != 'no':
            for x in range(x, x + 5):
                print('-' * 40 + '\n"" : {},\nEnd Station: {},\nEnd Time: {},\nStart Station: {},\nStart Time: {},'
                                 '\nTrip Duration: {},\nUser Type: {}\n'.format(
                    df.iloc[x][0], df.iloc[x][5], df.iloc[x][2], df.iloc[x][4], df.iloc[x][1], df.iloc[x][3], df.iloc[x][6]))

            show_data = input('Do you want to see more entries? Type "Yes" or "No".')
            x += 1


def main():
    while 1:
        city, month, day, chosen_filter = get_filters()
        df = load_data(city, month, day)

        time_stats(df, chosen_filter)
        station_stats(df, chosen_filter)
        trip_duration_stats(df, chosen_filter)
        user_stats(df, chosen_filter)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
