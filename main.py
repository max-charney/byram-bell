import streamlit as st
import time
import itertools
import datetime
from datetime import timedelta
import pandas as pd
import pytz
import base64


def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )
        
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
        "Extra": page_extras,
    }

    # Sidebar navigation
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(pages.keys()))

    # Display the selected page
    pages[selection]()

def page_home():  
    # Set up the page
    st.title("Byram Bell")
    st.subheader("This website plays the bell sound at the scheduled times, so don't forget to adjust your volume accordingly!")
    timer_ph = st.empty()
    next_bell_container = st.empty()

    # Set the timezone to Eastern Standard Time
    eastern = pytz.timezone('US/Eastern')

    alarm_times = ["07:45:00", "08:10:00", "09:14:00", "09:18:00", "10:22:00", "10:26:00", "11:30:00", "12:13:00", "13:17:00", "13:21:00", "14:25:00"]

    # Get the current time in Eastern Standard Time
    current_time = datetime.datetime.now(eastern).strftime('%H:%M:%S')

    # Convert the times to datetime objects in Eastern Standard Time
    time_objects = [eastern.localize(datetime.datetime.strptime(time, '%H:%M:%S')) for time in alarm_times]

    # Calculate the time difference between each time and the current time
    time_deltas = [(time - eastern.localize(datetime.datetime.strptime(current_time, '%H:%M:%S'))) % datetime.timedelta(days=1) for time in time_objects]

    # Convert each alarm time back to 'HH:MM:SS' format
    alarm_times = [time.strftime('%H:%M:%S') for time in time_objects]

    # Sort the times based on their time delta from the current time
    alarm_times = [time for _, time in sorted(zip(time_deltas, alarm_times))]

    # Main loop
    # Cycle through the alarm times indefinitely
    for alarm_time in itertools.cycle(alarm_times):
        # Display the current alarm time
        military_time = datetime.datetime.strptime(alarm_time, '%H:%M:%S')
        regular_time = military_time.strftime('%I:%M %p')
        next_bell_container.text("Next bell at: "+ regular_time)
        
        # Loop until the alarm time is reached
        while True:       
            # Set the timezone to Eastern Time
            et = pytz.timezone('US/Eastern')

            # Get the current time in Eastern Time
            current_time = datetime.datetime.now(tz=et).strftime("%H:%M:%S")

            # Check if the current time matches the alarm time
            if current_time == alarm_time:
                timer_ph.metric("Time Until Next Bell", "0:00:00")
                autoplay_audio("schoolBell.mp3")
                time.sleep(5)
                break
            
            current_time = datetime.datetime.now(tz=et).strftime("%H:%M:%S")
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

def page_extras():
    st.subheader("This website was developed by Mr. Lewick and Max Charney")
    st.write("Check out the code in our github repository: https://github.com/max-charney/byram-bell")
    st.write("-------------------------------------")
    st.subheader("Find your optimal volume:")

    bell_button_ph = st.empty()
    reset_button_ph = st.empty()


    bell = bell_button_ph.button('Bell')
    if bell:
        reset=reset_button_ph.button("Reset Bell (Click before testing volume again)")
        autoplay_audio("schoolBell.mp3")
            
        

        
if __name__ == "__main__":
    main()
