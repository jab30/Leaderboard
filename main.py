import streamlit as st
import pandas as pd
import os

# Set up the Streamlit app title
st.title("Baseball Pitch Analysis")

# Specify the directory containing your CSV files
csv_directory = 'csv_files'  # Change this to the path of the directory containing your CSV files

# Get a list of CSV files in the directory
csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]

# Create a dropdown menu for selecting a CSV file
selected_file = st.selectbox("Select a CSV file", csv_files)

# Load the selected CSV file
if selected_file is not None:
    df = pd.read_csv(os.path.join(csv_directory, selected_file))

    # Extract and display the date from the 'Date' column
    if 'Date' in df.columns:
        game_date = df['Date'].iloc[0]  # Assuming the date is the same for all rows
        st.write(f"Game Date: {game_date}")
    else:
        st.write("Date column not found in the selected CSV.")

    # First pitch strike percentage calculation
    st.header("First Pitch Strike Percentage")

    # Filter to include only the first pitch of each plate appearance
    first_pitch_df = df[df['PitchofPA'] == 1]

    # Define the strike conditions for the first pitch
    strike_conditions = [
        'StrikeSwinging', 'FoulBallNotFieldable', 'StrikeCalled', 'InPlay', 'FoulBallFieldable'
    ]

    # Calculate if the first pitch was a strike
    first_pitch_df['FirstPitchStrike'] = first_pitch_df['PitchCall'].isin(strike_conditions)

    # Group by pitcher and calculate the first pitch strike percentage
    FirstPitchStrike = first_pitch_df.groupby('Pitcher')['FirstPitchStrike'].mean() * 100

    # Display the result
    st.write("First Pitch Strike Percentage per Pitcher:")
    st.dataframe(FirstPitchStrike)

    # Two out of three strikes percentage calculation
    st.header("Two Out of Three Pitches Being Strikes Percentage")

    # Create a unique identifier for each plate appearance based on consecutive pitches by the same batter
    df['PlateAppearanceID'] = (df['Batter'] != df['Batter'].shift()).cumsum()

    # Filter to include only the first three pitches of each plate appearance
    first_three_pitches_df = df[df['PitchofPA'] <= 3]

    # Identify which pitches are strikes
    first_three_pitches_df['IsStrike'] = first_three_pitches_df['PitchCall'].isin(strike_conditions)

    # Group by pitcher and the newly created plate appearance ID to count strikes
    strike_counts = first_three_pitches_df.groupby(['Pitcher', 'PlateAppearanceID'])['IsStrike'].sum()

    # Calculate the percentage of plate appearances with at least two strikes in the first three pitches for each pitcher
    two_strike_pa_pct = (strike_counts >= 2).groupby('Pitcher').mean() * 100

    # Calculate the complement (100 - two_strike_pa_pct)
    TwoOfThree_pct = 100 - two_strike_pa_pct

    # Display the complement result
    st.write("Percentage of Plate Appearances with Fewer Than Two Strikes:")
    st.dataframe(TwoOfThree_pct)
