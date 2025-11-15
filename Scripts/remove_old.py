'''
Removes all old powerpoints (older than 10 weeks) from the repo when run
'''

from datetime import datetime, timedelta, timezone
import os



def calculate_nth_sunday(current_date: datetime, n: int) -> datetime:
    '''
    Calculates the date of the nth sunday BACKWARDS from the current date
    '''

    days_back_until_sunday = current_date.weekday() + 1 # Days until the LAST Sunday
    days_back_until_nth_sunday = days_back_until_sunday + (n - 1) * 7  # Days until the nth Sunday
    next_nth_sunday = current_date - timedelta(days=days_back_until_nth_sunday)
    return next_nth_sunday

def get_last_sunday_auto(output_time_format="%Y_%m_%d", number=10, user_input=1) -> str:
    '''
    Obtains a required number of sundays from the current date
    '''
    while True:
        # Get the current date
        current_date = datetime.now(timezone.utc)

        # Calculate and display the first 5 Sundays
        selected_sunday = int(user_input)
        
        try:
            if 1 <= selected_sunday <= number:
                selected_date = calculate_nth_sunday(current_date, selected_sunday)
                # print(f"You selected: {selected_date.strftime('%Y-%m-%d')}")
                break
            else:
                print(f"Invalid input. Defaulting to 1")
                selected_sunday = 1
                continue
        except ValueError:
            print(f"Invalid input. Defaulting to 1.")
            selected_sunday = 1
            continue

    # Format the date as yy_mm_dd or some other format
    return selected_date.strftime(output_time_format)

def delete_past_powerpoints(protected=12):
    '''
    Uses subprocess to delete all powerpoints that are more than a quarter old
    '''

    # We keep protected + 3 powerpoints, any other ones with sundays in the past are deleted
    deleted_dates = [get_last_sunday_auto(number=100000000, user_input=i) 
                     for i in range(protected + 3, 100)]
    
    current_file_path = os.path.abspath(__file__)
    powerpoint_directory_path = os.path.abspath(os.path.join(os.path.dirname(current_file_path), '..','Complete slides'))
    
    for date in deleted_dates:
        file_to_delete = f'{os.path.join(powerpoint_directory_path, date)}.pptx'
        if os.path.exists(file_to_delete):
            print(f'Deleted {file_to_delete}')
            os.remove(file_to_delete)