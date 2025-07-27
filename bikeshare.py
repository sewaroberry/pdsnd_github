import time
import pandas as pd
import numpy as np

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
    
    city = ""
    month = ""
    day = ""
    
    # Prompt user for city input; validate using a loop until a correct city is entered
    cities = ['chicago', 'new york city', 'washington']
    while True:
        city = input("Choose a city (chicago, new york city, washington): ").lower()
        if city in cities:
            break
        print("Sorry! We don't have data about this city. Please try again!")


    # Prompt user for month input; allow filtering by specific month or no filter ('all')
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Choose a month (january to june) or 'all': ").lower()
        if month in months:
            break
        print("Sorry! We don't have data about this month. Please try again!")


    # Prompt user for day input; allow filtering by specific day or no filter ('all')
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Choose a day of week or 'all': ").lower()
        if day in days:
            break
        print("Sorry! Your input is invalid. Please try again!")

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
    # Read the data from the csv file of the city
    df = pd.read_csv(CITY_DATA[city])
    
    # Convert 'Start Time' to datetime and 'End Time' to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    
    # Create new columns for month and day of week
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month
    if month != 'all':
        months_list = ['january', 'february', 'march', 'april', 'may', 'june']
        month_index = months_list.index(month) + 1
        df = df[df['month'] == month_index]

    # Filter by day of week
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month for bike travel
    print('Most common month: ', df['month'].value_counts().index[0])


    # Display the most common day of the week for bike travel
    print('Most common day of week: ', df['day_of_week'].value_counts().index[0])
    

    # Display the most frequent start hour for bike travel
    print('Most common start hour: ',df['hour'].value_counts().index[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display the most commonly used start station
    print('Most Common Start Station: ', df['Start Station'].value_counts().index[0])

    # Display the most commonly used end station
    print('Most Common End Station: ', df['End Station'].value_counts().index[0])

    # Display the most frequent combination of start and end stations
    df['Station Combination'] = df['Start Station'] + ' (start) and ' + df['End Station'] + ' (end).'
    print('The most common station combination for your selection is ', 
          df['Station Combination'].value_counts().index[0], '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display the total trip duration for selected data
    print('Total Travel Time: ', df['Trip Duration'].sum())

    # Display the average trip duration
    print('Mean Travel Time: ', df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display user type counts (e.g., Subscriber vs Customer)
    print('Counts of user types: ', df['User Type'].value_counts())

    # Display gender distribution (if available in dataset)
    if 'Gender' in df.columns:
      print('Counts of gender: ', df['Gender'].value_counts())

    # Display birth year stats: earliest, most recent, and most common (if available)
    if 'Birth Year' in df.columns:
      print('Most earliest year of birth: ', df['Birth Year'].sort_values().iloc[0])
      print('Most recent year of birth: ', df['Birth Year'].sort_values(ascending = False).iloc[0])
      print('Most common year of birth', df['Birth Year'].value_counts().index[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        row_index = 0
        while True:
            show = input("Would you like to see 5 rows of raw data? (yes or no): ").lower()
            if show != 'yes':
                break
            print(df.iloc[row_index:row_index+5])
            row_index += 5
            if row_index >= len(df):
                print("No more raw data to display.")
                break

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()