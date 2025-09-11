import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read CSV file -- First column is index
df = pd.read_csv("Data/Spectral_Soft_Sensor_1.csv", index_col=0)
print(f"Dimensions:")
print(f"Rows = {df.shape[0]} observations")
print(f"Columns = {df.shape[1]} variables")

print(df.head(20))

# Determine where traits end, and bands start
print(df.columns[19:21])

print(df.columns[-1])

# Split variables as traits and bands
traits = df.columns[:20]
bands = df.columns[20:]

# We can conclude that there are;
print(f"Number of Observations: {df.shape[0]}")
print(f"Number of Traits: {len(traits)}")
print(f"Wavelength range: {bands[0]} - {bands[-1]}")# range = wavelength in this dataset

# Missing value analysis for traits
traits_null_counts = df[traits].isnull().sum()
traits_null_pct = df[traits].isnull().mean() * 100

trait_missing = pd.DataFrame({
    'Trait': traits,
    'MissingCount': traits_null_counts.values,
    'MissingPercent': traits_null_pct.values.round(2)
}).sort_values(by='MissingCount', ascending=False)

print(trait_missing)

# Check how many spectral bands are completely empty
bands_null_counts = df[bands].isnull().sum()

fully_missing_bands = (bands_null_counts == df.shape[0]).sum()
print(f"Number of completely missing bands: {fully_missing_bands}")

# Summary for traits
trait_stats = df[traits].describe().T 
trait_stats = trait_stats.round(4)

trait_summary = trait_stats[["mean", "std", "min", "50%", "max"]]
trait_summary.rename(columns={"50%": "median"}, inplace=True)

print(trait_summary.head(20))

# Histograms for traits
df[traits].hist(figsize=(12,8), bins=30, edgecolor='black')
plt.suptitle('Trait Distributions')
plt.tight_layout()
plt.show()

# Converting wavelengths to RGB, then visualize
wavelengths = bands.astype(int) # from '450' => 450

spectral_data = df[bands].values

# RGB range
def to_rgb(wmin, wmax): # RGB range
    return (wavelengths >= wmin) & (wavelengths <= wmax)

range_red = to_rgb(625, 740)  # https://en.wikipedia.org/wiki/Green
range_green = to_rgb(495, 570)# https://en.wikipedia.org/wiki/Green
range_blue = to_rgb(450, 495) # https://en.wikipedia.org/wiki/Blue

# Findind the RGB matrix
rgb_data = np.stack([
    np.nanmean(spectral_data[:, range_red], axis=1),
    np.nanmean(spectral_data[:, range_green], axis=1),
    np.nanmean(spectral_data[:, range_blue], axis=1)
], axis=1)

# Min-max normalization (0-1)
rgb_normalized = np.zeros_like(rgb_data)
for i in range(3):  # R, G, B
    channel = rgb_data[:, i]
    rgb_normalized[:, i] = (channel - np.nanmin(channel)) / (np.nanmax(channel) - np.nanmin(channel))

# Visualization for the first 50 Observations
plt.figure(figsize=(10, 1))
plt.imshow([rgb_normalized[0:50]], aspect='auto')
plt.title("RGB Representation of First 50 Observations")
plt.axis('off')
plt.show()

plt.figure(figsize=(10, 1))
plt.imshow([rgb_normalized[1300:1350]], aspect='auto')
plt.title("RGB Representation of Random 50 Observations")
plt.axis('off')
plt.show()