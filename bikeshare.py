import time
import pandas as pd
import numpy as np
import calendar
from datetime import date
#via stack overflow for number formatting
import locale
locale.setlocale(locale.LC_ALL, '')

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            valid_cities = ['chicago', 'new york city', 'washington']
            city = input("Which city are you interested in: Chicago, New York City, or Washington? ").lower()
            if city not in valid_cities:
                raise ValueError
            else:
                break
        except ValueError:
            print("Please type one of the following: Chicago, New York City, or Washington. ")
            continue

    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        try:
            valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
            month = input("Information is available for either one or all months from January through June — which month(s) are you interested in? ").lower()
            if month not in valid_months:
                raise ValueError
            else:
                break
        except ValueError:
            print("Please type one of the following: January, February', March, April, May, June, or all. ")
            continue

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            valid_weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
            day = input("Information is available for either one or all days of the week — which day(s) are you interested in? ").lower()
            if day not in valid_weekdays:
                raise ValueError
            else:
                break
        except ValueError:
            print("Please type one of the following: Monday, Tuesday', Wednesday, Thursday, Friday, Saturday, Sunday, or all. ")
            continue

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
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
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

    # TO DO: display the most common month as month name
    #apply w/lambda via stack overflow for month name formatting
    df['month_name'] = df['month'].apply(lambda x: calendar.month_name[x])
    popular_month = df['month_name'].mode()[0]
    print("The most popular month was {}.".format(popular_month))
    # TO DO: display the most common day of week
    popular_weekday = df['day_of_week'].mode()[0]
    print("The most popular day of the week was {}.".format(popular_weekday))
    # TO DO: display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    #hour formatting via stack overflow
    df['hour_formatted'] = df['Start Time'].dt.strftime('%H').add(':00')
    # find the most popular hour
    popular_hour = df['hour_formatted'].mode()[0]
    print("The most popular hour to start a trip was {}.".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_startpoint = df['Start Station'].mode()[0]
    print("The most commonly used start station was {}.".format(popular_startpoint))
    # TO DO: display most commonly used end station
    popular_endpoint = df['End Station'].mode()[0]
    print("The most commonly used end station was {}.".format(popular_endpoint))
    # TO DO: display most frequent combination of start station and end station trip
    # after combining start and end station to create new column
    df['start_end'] = df['Start Station'] + "," + df['End Station'] 
    popular_start_end = df['start_end'].mode()[0]
    print("The most common trip started at {} and ended at {}.".format(popular_start_end.split(",")[0], popular_start_end.split(",")[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time and trips
    #count total trips
    total_trips = df['Trip Duration'].count()
    #format numbers to display with the thousands separator
    total_trips = f'{total_trips:n}'
    #get total travel time in seconds and use div, mod to convert to days, hours, etc.
    #calculating method below via python tutorial
    total_travel_time = df['Trip Duration'].sum()
    days = int(total_travel_time // (86400))
    days = f'{days:n}'
    total_travel_time = total_travel_time % (86400)
    hours = int(total_travel_time // 3600)
    total_travel_time %= 3600
    minutes = int(total_travel_time // 60)
    total_travel_time %= 60
    seconds = int(total_travel_time)
    print("All users combined took a grand total of {} trips that lasted for a grand total of: \n{} days, \n{} hours, \n{} minutes, \nand {} seconds on trips.".format(total_trips, days, hours, minutes, seconds))
    
    # TO DO: display mean travel time
    #get mean travel time in seconds and use div, mod to convert to minutes, seconds
    mean_travel_time = df['Trip Duration'].mean()
    minutes = int(mean_travel_time / 60)
    mean_travel_time %= 60
    seconds = int(mean_travel_time)
    print("The average trip was {} minutes and {} seconds long.".format(int(minutes), int(seconds)))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    
    # TO DO: Display counts of user types
    subscribers = df['User Type'].value_counts()[0]
    subscribers = f'{subscribers:n}'
    customers = df['User Type'].value_counts()[1]
    customers = f'{customers:n}'
    print("{} subscribers, and {} customers were active users.".format(subscribers, customers))
    
    # TO DO: Display counts of gender if pertinent data exists for the city selected
    if 'Gender' in df.columns:
        males = df['Gender'].value_counts()[0]
        males = f'{males:n}'
        females = df['Gender'].value_counts()[1]
        females = f'{females:n}'
        print("{} males, and {} females were active users.".format(males, females))
    else:    
        print("Gender data is unavailable for the selected city. ")
    
    # TO DO: Display earliest, most recent, and most common year of birth if pertinent data exists for the city selected
    current_year = date.today().year
    if 'Birth Year' in df.columns:
        #earliest birthyear for oldest users, calculate possible ages accordingly
        earliest_birthyear = int(df['Birth Year'].min())
        max_age_max = current_year - earliest_birthyear
        max_age_min = max_age_max - 1
        print("The earliest birth year among active users was {} - people born in {} are either {} or {} years old.".format(earliest_birthyear, earliest_birthyear, max_age_min, max_age_max))
        #latest birthyear for youngest users, calculate possible ages accordingly
        latest_birthyear = int(df['Birth Year'].max())
        min_age_max = current_year - latest_birthyear
        min_age_min = min_age_max - 1
        print("The earliest birth year among active users was {} - people born in {} are either {} or {} years old.".format(latest_birthyear, latest_birthyear, min_age_min, min_age_max))
        #most common birthyear and user age, calculate possible ages accordingly
        common_birthyear = int(df['Birth Year'].mode())
        common_age_max = current_year - common_birthyear
        common_age_min = common_age_max - 1
        print("The most common birth year among active users was {} - people born in {} are either {} or {} years old.".format(common_birthyear, common_birthyear, common_age_min, common_age_max))
    else:
        print("Birth year and age data is unavailable for the selected city. ")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def raw_data(df):
    """
    Asks user if they want to see 5 lines of raw data.
    Returns the 5 lines of raw data if user inputs `yes`. Iterate until user response with a `no`

    """

    start_row = 0
    end_row = 4

    while True:
        sample_data = input('\nWould you like to see all available information for five trips? Enter yes or no.\n')
        # Check if response is yes, print the raw data and increment count by 5
        #offer the user 5 rows of sample data, set to display all columns
        if sample_data.lower() == 'yes':
            #display settings via python tutorial
            with pd.option_context('display.max_columns', 20):
                five_rows = df.loc[start_row:end_row]
                print(five_rows)
                start_row+=5
                end_row+=5
        # otherwise break
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        #invite the user to restart or exit
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
