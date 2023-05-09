import streamlit as st
import time
from playsound import playsound
import itertools
import datetime
from datetime import timedelta
import pandas as pd
import pytz

timezone = pytz.timezone('US/Eastern') # replace with your desired time zone
now = datetime.datetime.now(timezone)
st.write(now.strftime("%H:%M:%S"))

def main():
    # Set up page
    st.set_page_config(
        page_title="Byram Bell",
        page_icon="bobcatlogo.png",
        initial_sidebar_state="expanded",
    )

    hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden; position: absolute; top: 0;}
        </style>
        """

    st.markdown(hide_menu_style, unsafe_allow_html=True)


    hide_footer_style = """
            <style>
            footer {visibility: hidden; position: absolute; top: 0;}
            </style>
            """

    st.markdown(hide_footer_style, unsafe_allow_html=True)

    st.markdown("""
            <style>
                .block-container {
                        padding-top: 1rem;
                        padding-bottom: 0rem;
                    }
            </style>
            """, unsafe_allow_html=True)

    # Define sidebar pages
    pages = {
        "Home": page_home,
        "Bell Schedule": page_bell_schedule,
        "Credits": page_credits,
    }

    # Sidebar navigation
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))

    # Display the selected page
    pages[selection]()

def page_home():
    # Set up the page
    st.title("TEST")
    st.subheader("Our website plays the bell sound at the scheduled times, so don't forget to adjust your volume accordingly!")
    timer_ph = st.empty()
    next_bell_container = st.empty()


    # Alarm times
    alarm_times = ["07:45:00", "08:10:00", "09:14:00", "09:18:00", "10:22:00", "10:26:00", "11:30:00", "12:13:00", "13:17:00", "13:21:00", "14:25:00"]

    # Sort alarm times
    # Convert the alarm times to datetime.time objects
    alarm_times_dt = [datetime.datetime.strptime(t, '%H:%M:%S') for t in alarm_times]

    # Get the current time
    current_time = datetime.datetime.now()

    # Define a key function to calculate the time difference between each alarm time and the current time
    def time_difference(time):
        time_dt = datetime.datetime.combine(current_time.date(), time.time())
        if time_dt >= current_time:
            return (time_dt - current_time).total_seconds()
        else:
            return (time_dt - current_time + datetime.timedelta(days=1)).total_seconds()

    # Sort the alarm times based on the time difference from the current time
    sorted_alarm_times_dt = sorted(alarm_times_dt, key=time_difference)

    # Convert the sorted alarm times back to the original format
    alarm_times = [t.strftime('%H:%M:%S') for t in sorted_alarm_times_dt]

    # Main loop
    # Cycle through the alarm times indefinitely
    for alarm_time in itertools.cycle(alarm_times):
        # Display the current alarm time
        military_time = datetime.datetime.strptime(alarm_time, '%H:%M:%S')
        regular_time = military_time.strftime('%I:%M %p')
        next_bell_container.text("Next bell at: "+ regular_time)

        # Loop until the alarm time is reached
        while True:        
            # Get the current time
            current_time = datetime.datetime.now().strftime("%H:%M:%S")

            # Check if the current time matches the alarm time
            if current_time == alarm_time:
                timer_ph.metric("Time Until Next Bell", "0:00:00")
                playsound('schoolBell.mp3')
                break
            
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            current_time = datetime.datetime.strptime(current_time, '%H:%M:%S')

            if current_time < military_time:
                time_difference = military_time - current_time            
                timer_ph.metric("Time Until Next Bell", str(time_difference))

            elif current_time > military_time:
                time_difference = military_time - current_time
                timer_ph.metric("Time Until Next Bell", str(time_difference + timedelta(days=1)))

            else:
                timer_ph.metric("Time Until Next Bell", "Something went wrong, please try again later")

            # Wait for 1
            time.sleep(1)
def page_bell_schedule():
    df = pd.DataFrame(
    data=(
        ("7:45 AM"),
        ("8:10 AM"), 
        ("9:14 AM"), 
        ("9:18 AM"), 
        ("10:22 AM"), 
        ("10:26 AM"), 
        ("11:30 AM"), 
        ("12:13 AM"), 
        ("1:17 PM"), 
        ("1:21 PM"), 
        ("2:25 PM")
        ),
        columns=["Bell Times"],
    )

    df.index += 1
    st.table(df)

def page_credits():
    st.subheader("This website was developed by Mr. Lewick and Max Charney")
    st.write("Checkout the code in our github repository: https://github.com/max-charney/byram-bell")

if __name__ == "__main__":
    main()
