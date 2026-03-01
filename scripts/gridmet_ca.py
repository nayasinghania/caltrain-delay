import os

import xarray as xr

CA_LAT_MIN = 32.5
CA_LAT_MAX = 42.0
CA_LON_MIN = -124.5
CA_LON_MAX = -114.0

input_dir = "data/raw/gridmet"
output_dir = "data/raw/gridmet_ca"
os.makedirs(output_dir, exist_ok=True)

files = sorted([f for f in os.listdir(input_dir) if f.endswith(".nc")])

for filename in files:
    output_path = f"{output_dir}/{filename}"

    if os.path.exists(output_path):
        print(f"Already clipped: {filename}")
        continue

    print(f"Clipping {filename}...")

    ds = xr.open_dataset(f"{input_dir}/{filename}")

    # Sort lat and lon to ensure ascending order
    ds = ds.sortby("lat")
    ds = ds.sortby("lon")

    # Clip to California
    ds_ca = ds.sel(lat=slice(CA_LAT_MIN, CA_LAT_MAX), lon=slice(CA_LON_MIN, CA_LON_MAX))

    print(f"  Shape: {dict(ds_ca.dims)}")

    ds_ca.to_netcdf(output_path)

    size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"Done: {filename} — {size:.1f} MB")

    ds.close()

print("All done")
