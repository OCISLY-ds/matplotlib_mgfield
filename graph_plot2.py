import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pytz
import os

def plot_daily_reports(csv_file, output_dir):
    # Create output directory for daily reports if it doesn't exist
    daily_output_dir = os.path.join(output_dir, 'daily_reports')
    if not os.path.exists(daily_output_dir):
        os.makedirs(daily_output_dir)

    # Read the CSV file into a pandas DataFrame
    data = pd.read_csv(csv_file)

    # Combine 'Date' and 'Time' columns into a single datetime column
    data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])

    # Group data by date
    grouped_data = data.groupby(data['DateTime'].dt.date)

    # Plot data for each day
    num_files_created = 0
    for date, group in grouped_data:
        # Create a new figure
        plt.figure(figsize=(20, 12))

        # Plot the data
        plt.plot(group['DateTime'], group['MGField Value1'], marker='o', linestyle='solid', markersize=3, linewidth=2)

        # Set x-axis limits from 00:00 to 23:59
        plt.xlim(pd.Timestamp.combine(date, pd.Timestamp.min.time()), 
                 pd.Timestamp.combine(date, pd.Timestamp.max.time()))

        # Set labels and title
        plt.xlabel('Time')
        plt.ylabel('MGField Value in nT')
        plt.title(f'MGField Value1 on {date}')

        # Customize x-axis date formatting
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=1))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

        # Double the number of y-axis tick marks
        plt.gca().yaxis.set_major_locator(plt.MaxNLocator(nbins='auto', steps=[1, 2, 5, 10]))

        # Show y-axis grid lines
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Calculate operation (biggest value - smallest value)
        operation_result = group['MGField Value1'].max() - group['MGField Value1'].min()

        # Add a text box displaying the operation result
        plt.text(0.95, 0.95, f'Variation: {operation_result:.2f} nT', transform=plt.gca().transAxes, ha='right', va='top',
                 bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))

        # Save the plot to a file with the date included in the filename
        output_file = os.path.join(daily_output_dir, f'MGField_Value1_{date}.png')
        plt.savefig(output_file)
        num_files_created += 1

        # Close the current figure to release memory
        plt.close()

        # Print live updates
        print(f"Created daily report for {date} | Files created: {num_files_created}", end='\r')

    print("\nDaily reports creation completed.")
    print(f"Total daily reports created: {num_files_created}")

def plot_weekly_report(csv_file, output_dir):
    # Create output directory for weekly reports if it doesn't exist
    weekly_output_dir = os.path.join(output_dir, 'weekly_reports')
    if not os.path.exists(weekly_output_dir):
        os.makedirs(weekly_output_dir)

    # Read the CSV file into a pandas DataFrame
    data = pd.read_csv(csv_file)

    # Combine 'Date' and 'Time' columns into a single datetime column
    data['DateTime'] = pd.to_datetime(data['Date'] + ' ' + data['Time'])

    # Group data by week starting on Monday
    data['Week_Start'] = data['DateTime'] - pd.to_timedelta(data['DateTime'].dt.dayofweek, unit='D')
    grouped_data = data.groupby(data['Week_Start'].dt.date)

    # Plot data for each week
    num_files_created = 0
    for start_date, group in grouped_data:
        end_date = start_date + pd.DateOffset(days=6)  # Calculate end date (Sunday) of the week

        # Create a new figure
        plt.figure(figsize=(20, 12))

        # Plot the data
        plt.plot(group['DateTime'], group['MGField Value1'], linestyle='solid', linewidth=1.75)

        # Set x-axis limits from Monday 00:00 to Sunday 23:59
        plt.xlim(pd.Timestamp.combine(start_date, pd.Timestamp.min.time()), 
                 pd.Timestamp.combine(end_date, pd.Timestamp.max.time()))

        # Set labels and title
        plt.xlabel('Time')
        plt.ylabel('MGField Value in nT')
        plt.title(f'MGField Value1 from {start_date} to {end_date}')

        # Customize x-axis date formatting
        plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=6))
        plt.gca().tick_params(axis='x', rotation=45)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d-%H:%M'))

        # Double the number of y-axis tick marks
        plt.gca().yaxis.set_major_locator(plt.MaxNLocator(nbins='auto', steps=[1, 2, 5, 10]))

        # Show y-axis grid lines
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Calculate operation (biggest value - smallest value)
        operation_result = group['MGField Value1'].max() - group['MGField Value1'].min()

        # Add a text box displaying the operation result
        plt.text(0.95, 0.95, f'Variation: {operation_result:.2f} nT', transform=plt.gca().transAxes, ha='right', va='top',
                 bbox=dict(facecolor='white', alpha=0.5, edgecolor='black'))

        # Save the plot to a file with the start and end dates included in the filename
        output_file = os.path.join(weekly_output_dir, f'MGField_Value1_{start_date}_to_{end_date}.png')
        plt.savefig(output_file)
        num_files_created += 1

        # Close the current figure to release memory
        plt.close()

        # Print live updates
        print(f"Created weekly report from {start_date} to {end_date} | Files created: {num_files_created}", end='\r')

    print("\nWeekly reports creation completed.")
    print(f"Total weekly reports created: {num_files_created}")

# Example usage:
csv_file = '/Users/florianvonbargen/Desktop/matplotlib/2024-03-10_12-17-09.csv'
parent_output_dir = '/Users/florianvonbargen/Desktop/matplotlib/Graph_main'

# Create parent output directory if it doesn't exist
if not os.path.exists(parent_output_dir):
    os.makedirs(parent_output_dir)

# Generate daily reports
plot_daily_reports(csv_file, os.path.join(parent_output_dir, 'daily_reports'))

# Generate weekly reports
plot_weekly_report(csv_file, os.path.join(parent_output_dir, 'weekly_reports'))
