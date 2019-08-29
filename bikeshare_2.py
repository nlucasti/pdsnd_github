import time
import pandas as pd
import numpy as np
import calendar as calendar
import csv
from collections import Counter

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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input("Please enter the city for which you want to see bike share information(chicago, new york city, washington): ");
            city = city.lower()
            if city not in CITY_DATA:
                raise NameError();
        except NameError:
            print("Sorry, please enter a valid city");
        else:
            break
    city = city.replace(" ", "_")

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("Please enter the month(all, january, february, ... , june): ");
            month = month.lower()
            if month.title() not in calendar.month_name and month != 'all':
                raise NameError();
        except NameError:
            print("Sorry, please enter a valid month");
        else:
            break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("Please enter the day of the week(all, monday, tuesday, ... sunday): ")
            day = day.lower()
            if day.title() not in calendar.day_name and day != 'all':
                raise NameError();
        except NameError:
            print("Sorry, please enter a valid day of the week")

        else:
            break

    print('-'*40)
    return city, month, day

def convert_date(input):
    return time.strptime(input, '%Y-%m-%d %H:%M:%S')

def column(input, row_ind):
    return [row[row_ind] for row in input]

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
    with open(city + ".csv") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        s_dates = []
        header = next(readCSV)
        rem_data_all = []
        rem_data = []
        for row in readCSV:
            s_date = row[1]
            rem_data = row[2:]
            s_date = convert_date(s_date);
            if month == time.strftime("%B",s_date).lower() and day == 'all':
                s_date = time.strftime('%Y-%m-%d %H:%M:%S',s_date)
                s_dates.append(s_date)
                rem_data_all.append(rem_data)
            elif day == time.strftime("%A",s_date).lower() and month == 'all':
                s_date = time.strftime('%Y-%m-%d %H:%M:%S',s_date)
                s_dates.append(s_date)
                rem_data_all.append(rem_data)
            elif day == time.strftime("%A",s_date).lower() and month == time.strftime("%B",s_date).lower():
                s_date = time.strftime('%Y-%m-%d %H:%M:%S',s_date)
                s_dates.append(s_date)
                rem_data_all.append(rem_data)
            elif (month == 'all' and day == 'all'):
                s_date = time.strftime('%Y-%m-%d %H:%M:%S',s_date)
                s_dates.append(s_date)
                rem_data_all.append(rem_data)
    df_data = {header[1]: s_dates}
    for col in range(2, len(header)):
        if(header[col] is not None and df_data is not None):
            df_data.update({header[col]: column(rem_data_all, col - 2)})
#    df_data = {header[1]:s_dates,
#            header[2]: column(rem_data_all,0),
#            header[3]: column(rem_data_all,1),
#            header[4]: column(rem_data_all,2),
#            header[5]: column(rem_data_all,3),
#            header[6]: column(rem_data_all,4),
#            header[7]: column(rem_data_all,5),
#            header[8]: column(rem_data_all,6)
#            }

    df = pd.DataFrame(df_data)
    df = df.replace(r'^\s*$', np.nan, regex=True)



    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    date = pd.to_datetime(df['Start Time'])

    # display the most common month
    month_most_common = Counter(date.dt.month).most_common(1)
    print('The most common month is', [count[0] for count in month_most_common])

    # display the most common day of week
    day_most_common = Counter(date.dt.day).most_common(1)
    print('The most common day is', [count[0] for count in day_most_common])

    # display the most common start hour
    hour_most_common = Counter(date.dt.hour).most_common(1)
    print('The most common hour is', [count[0] for count in hour_most_common])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statisics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_most_common = Counter(df['Start Station']).most_common(1)
    print('The most common start station is', [count[0] for count in start_most_common])

    # display most commonly used end station
    end_most_common = Counter(df['End Station']).most_common(1)
    print('The most common end station is', [count[0] for count in end_most_common])

    # display most frequent combination of start station and end station trip
    end_most_common = Counter(df['Start Station'] + '->' + df['End Station']).most_common(1)
    print('The most common trip is between ', [count[0] for count in end_most_common])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = sum(pd.to_numeric(df['Trip Duration']))
    print('The total trip duration is', total, 'seconds')

    # display mean travel time
    avg_trip = total/len(df['Trip Duration'])
    print('The average trip duration is %.2f' %(avg_trip),'seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    type = Counter(df['User Type'])
    print('Counts of user types:', type)

    # Display counts of gender
    if(not KeyError):
        gender = Counter(df['Gender'])
        print('Counts of gender:', gender)

    # Display earliest, most recent, and most common year of birth
    if(not KeyError):
        df = df.dropna(subset=['Birth Year'])
        year_most_common = df['Birth Year'].value_counts().idxmax()
        sorted_year = sorted(df['Birth Year'])
        year_earliest = sorted_year[0]
        year_recent = sorted_year[len(sorted_year)-1]

        print('Most Common Birth Year:', year_most_common)
        print('Earliest Birth Year:', year_earliest)
        print('Most Recent Birth Year:', year_recent)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_raw_data(df):
    more = input('Would you like to print raw data? Enter yes or no.\n')
    count = 5
    if more.lower() == 'yes':
        while True:
            print(df[count-5:count])
            restart = input('\nEnter \'q\' to stop. Enter any other key to continue.\n')
            if restart != 'q':
                count += 5
                continue
            elif restart == 'q':
                break
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        print_raw_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
