"""
This file contains a simplified version of the code run in the EVAL_MVP deliverable by Dylan Lee

Authors
-------
Dylan Lee <dylan.lee@ertcorp.com>
Tadd Bindas <tadd.bindas@ertcorp.com>

"""
from pathlib import Path

import numpy as np

import os
import pdb
import argparse
import geopandas as gpd
import xarray as xr
import fsspec
import pandas as pd
from datetime import datetime
from typing import List, Tuple

import zarr

DATA_DIR = Path(__file__) / "../data/"

URL_CONUS = 's3://noaa-nwm-retrospective-3-0-pds/CONUS/zarr/chrtout.zarr'


def open_ds(url: str) -> xr.DataArray:
    return xr.open_zarr(
        fsspec.get_mapper(url, anon=True), consolidated=True, mask_and_scale=True
    )['streamflow'].drop_vars(['latitude', 'elevation', 'gage_id', 'longitude', 'order'])

# def get_feature_ids_in_huc8(nwm_flows: gpd.GeoDataFrame, huc8_gdf: gpd.GeoDataFrame) -> List[int]:
#     return sorted(nwm_flows[nwm_flows.intersects(huc8_gdf.unary_union)]['ID'].tolist())

# def get_peak_discharges(ds: xr.DataArray, feature_ids: List[int], start_time: datetime, end_time: datetime) -> pd.DataFrame:
#     # Select data for specified features and time window
#     ts = ds.sel(feature_id=feature_ids, time=slice(start_time, end_time))
    
#     # Get maximum streamflow values for each feature_id
#     peak_flows = ts.max(dim='time')
    
#     # Convert to dataframe and format
#     df = peak_flows.to_dataframe().reset_index()
#     return df[['feature_id', 'streamflow']].rename(columns={'streamflow': 'discharge'})

# def find_fim_version_dir(hydrofabric_dir: str, fim_version: str) -> str:
#     for dir_name in os.listdir(hydrofabric_dir):
#         if fim_version in dir_name:
#             return os.path.join(hydrofabric_dir, dir_name)
#     raise ValueError(f"FIM version '{fim_version}' not found in {hydrofabric_dir}")

# def check_huc_exists(fim_version_dir: str, huc: str) -> None:
#     if huc not in os.listdir(fim_version_dir):
#         raise ValueError(f"HUC '{huc}' not found in {fim_version_dir}")

def gen_retro_fim(feature_id_file: np.ndarray, date_range: Tuple[str, str], output_file: Path) -> None:
    feature_ids = np.load(feature_id_file).squeeze()
    ds = open_ds(URL_CONUS)
    start_time, end_time = [datetime.strptime(d, "%Y-%m-%d") for d in date_range]
    ts = ds.sel(feature_id=feature_ids, time=slice(start_time, end_time))
    # flowfile = get_peak_discharges(ds, feature_ids, start_time, end_time)
    ts.to_zarr(output_file, encoding={'streamflow': {'chunks': None}})


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate retrospective FIM")
    # parser.add_argument("--fim-version", required=True, help="FIM version")
    # parser.add_argument("--huc", required=False, help="HUC code")
    # parser.add_argument("--hydrofabric-dir", required=False, default = OUTPUTS_DIR, help="Path to hydrofabric directory")
    # parser.add_argument("--huc-shapes", required=False, default = os.path.join('/data','wbd','WBD_National.gpkg'), help="Path to huc gpkg")
    # parser.add_argument("--flow-feat", required=False, default = os.path.join('/data','nwm_hydrofabric',"nwm_flows.gpkg"), help="Path to flow features gpkg")
    # parser.add_argument("--output-timeseries", required=False, default = False, help="Path to flow features gpkg")

    # Load NWM flows and HUC8 geodataframes
    parser.add_argument("--feature_id_file", required=True, help="feature_ids")
    parser.add_argument("--date-range", required=True, nargs=2, help="Date range (start end)")
    parser.add_argument("--output_path", required=True, help="Path to the output directory")
    args = parser.parse_args()

    # gen_retro_fim(
    #     feature_id_file="/home/tadd.bindas/github/pi4/deliveries/rise_redelivery/near_real-time_sfincs/data/NWM/coffeyville_feature_ids_huc_8_headwater.npy", 
    #     date_range=["2019-05-20", "2019-06-03"],
    #     output_file="/home/tadd.bindas/github/pi4/deliveries/rise_redelivery/near_real-time_sfincs/data/NWM/huc_8_retro_headwater"
    # )
    # gen_retro_fim(
    #     feature_id_file=args.feature_id_file, 
    #     date_range=args.date_range,
    #     output_file=args.output_file
    # )
    # huc8_gdf = gpd.read_file(args.huc_shapes, layer="WBDHU8")
    # nwm_flows = gpd.read_file(args.flow_feat)

    # gen_retro_fim(args.feature_id_file, args.date_range)
    # gen_retro_fim(args.hydrofabric_dir, args.fim_version, args.huc, args.date_range, huc8_gdf, nwm_flows)

# data/NWM/coffeyville_feature_ids.npy
