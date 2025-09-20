import csv
import datetime

# Define start and end dates
start_date = datetime.datetime(2015, 4, 22, 7, 0, 0)
end_date = datetime.datetime(2020, 4, 22, 7, 0, 0)

# Define start and end integers
start_int = 365 * 5 + 1
end_int = 1

# Define askmedian range and calculate the rate of decrease
askmedian_range = start_int - end_int
askmedian_rate = askmedian_range / \
    ((end_date - start_date).total_seconds() / 3600)

# Define the two stocks
stocks = ['STOCK1', 'STOCK2']

# Define the CSV header
header = ['gmtTime', 'askMedian', 'bidMedian',
          'askVolume', 'bidVolume', 'spreadMedian', 'symbol']

# Create and open the CSV file
with open('testdata.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)

    # Loop through each hour between the start and end dates
    current_date = start_date
    while current_date <= end_date:
        # Loop through each stock
        for stock in stocks:
            # Calculate the askmedian and bidmedian for the current hour

            # Calculate the askmedian and bidmedian for the current hour
            current_askmedian = start_int - askmedian_rate * \
                (current_date - start_date).total_seconds() / 3600
            current_bidmedian = current_askmedian - 0.0141

            # Generate a row for the CSV file
            row = [current_date.strftime('%Y-%m-%d %H:%M:%S'),
                   current_askmedian,
                   current_bidmedian,
                   current_askmedian * 10,
                   current_bidmedian * 10,
                   0.0141,
                   stock]
            # Write the row to the CSV file
            writer.writerow(row)

        # Increment the current date by one hour
        current_date += datetime.timedelta(hours=1)
