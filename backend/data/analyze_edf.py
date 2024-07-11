import mne
import os

# Path to the downloaded EDF file
file_path = '/Users/nil/Desktop/SC4111E0-PSG.edf'  # Replace with your actual file path

# Load the EDF file
raw = mne.io.read_raw_edf(file_path, preload=True, stim_channel='Event marker')

# Print basic information about the file
print(raw.info)

# Check if the Hypnogram file exists
hypnogram_path = file_path.replace('PSG.edf', 'Hypnogram.edf')
if os.path.exists(hypnogram_path):
    # Get annotations
    annotations = mne.read_annotations(hypnogram_path)
    raw.set_annotations(annotations)

    # Extract annotations to DataFrame
    annotations_df = raw.annotations.to_data_frame()

    print("Annotations:")
    print(annotations_df.head())
else:
    print(f"Hypnogram file not found: {hypnogram_path}")

# List all channels
channels = raw.ch_names
print("\nChannels:")
print(channels)

# Extract sample data from each channel
channel_data_samples = {}
for channel in channels:
    channel_data_samples[channel] = raw.get_data(picks=channel)[0][:10]

# Print the first few samples from each channel
for channel, data in channel_data_samples.items():
    print(f"\nChannel: {channel}")
    print(data)
