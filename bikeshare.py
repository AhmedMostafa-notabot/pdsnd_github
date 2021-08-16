import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    flag=True
    while(flag==True):
        city = input('Which City do you want to inspect?\n (chicago, new york city, washington)\n')
        month = input('Which month do you want to analyze?\n (all, january, february, ... , june)\n')
        day = input('Which day do you want to analyze?\n (all, monday, tuesday, ... sunday)\n')
        if((city not in CITY_DATA.keys()) or (month !='all' and (month not in months))):
            print('Wrong Input Please make sure you choose from the given choices only.Thx!')
            continue
        else:
            flag=False
    print('-'*40)
    return city.lower(), month.lower(), day.lower()


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
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

    # TO DO: display the most common month
    commonmo=df['month'].mode()[0]
    print('Common Month is {}'.format(months[commonmo-1]))
    # TO DO: display the most common day of week
    commonda=df['day_of_week'].mode()[0]
    print('Common Day is', commonda)
    # TO DO: display the most common start hour
    commonhr=df['Start Time'].dt.hour.mode()[0]
    print('Common Hour is', commonhr)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    comstart=df.groupby(['Start Station'])['Start Station'].count().nlargest(1)
    print(comstart,'\n')
    # TO DO: display most commonly used end station
    comend=df.groupby(['End Station'])['End Station'].count().nlargest(1)
    print(comend,'\n')

    # TO DO: display most frequent combination of start station and end station trip
    comstend=df.groupby(['Start Station','End Station'])['Start Station','End Station'].count().nlargest(1,['Start Station','End Station'])
    print('Common Trip')
    print(comstend)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    tottime=df['Trip Duration'].sum()
    print('Total Travel Time in seconds {} seconds\nin minutes {} minutes\nin hours {} hours\nin days {} days\n'.format(tottime,tottime/60,tottime/3600,tottime/86400))
    # TO DO: display mean travel time
    meantime=df['Trip Duration'].mean()
    print('Mean Travel Time in seconds {} seconds\nin minutes {} minutes\n'.format(meantime,meantime/60))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print(user_types,'\n')
    # TO DO: Display counts of gender
    if(city != 'washington'): 
        # Because it doesn't have gender column or Birth Year
        gender = df.groupby(['Gender'])['Gender'].count()
        print(gender,'\n')
    # TO DO: Display earliest, most recent, and most common year of birth
        earlyye=df['Birth Year'].min()
        commonye=df['Birth Year'].mode()[0]
        recentye=df['Birth Year'].max()
        print('Earliest Year Of Birth: {} \nMost Recent Year Of Birth: {} \nCommon Year Of Birth:{}'.format(earlyye,recentye,commonye))
    else:
        print("Sorry But Washington Data doesn't contain Gender or Birth Year Column :(")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?\n")
    start_loc = 0
    flag=True
    while (flag==True):
        print(df.iloc[start_loc:(start_loc+5)])
        start_loc += 5
        view_display = input("Do you wish to continue?: Enter yes or no\n").lower()
        if(view_display=='yes'):
            continue
        else:
            flag=False
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_data(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
