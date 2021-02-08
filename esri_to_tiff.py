"""
Convert existing ESRI tiles to .tif files using custom naming convention

ESRI tile naming convention: "large_tile_x00000_y00000_z00_w64_h64.png"
"""
import os
import subprocess
import glob
from osgeo import gdal
from tile_convert import tile_edges

def get_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--png", type=str,
                        help="directory in which ESRI .png files are stored")
    parser.add_argument("--output", type=str,
                        help="output directory for merged .tif file")

    return parser.parse_args()


def merge_tiles(input_pattern, output_path):
    merge_command = ['gdal_merge.py', '-o', output_path]

    for name in glob.glob(input_pattern):
        merge_command.append(name)

    subprocess.call(merge_command)


def georeference_raster_tile(x, y, z, path):
    bounds = tile_edges(x, y, z)
    filename, extension = os.path.splitext(path)
    gdal.Translate(filename + '.tif',
                   path,
                   outputSRS='EPSG:4326',
                   outputBounds=bounds)


if __name__ == "__main__":
    args = get_args()

    # iterate over files in png directory
    for filename in os.listdir(args.png):
        if filename.endswith(".png"):
            # get x, y, z values from filename
            x, y, z = 0, 0, 0
            values = filename.split("_")  # split on underscore
            for val in values:
                if val[0] == "x":
                    x = int(val[1:])
                if val[0] == "y":
                    y = int(val[1:])
                if val[0] == "z":
                    z = int(val[1:])

            filepath = args.png + "/" + filename

            # convert .png files to .tif
            georeference_raster_tile(x, y, z, filepath)

    print("Merging tiles")
    merge_tiles(args.png + '/*.tif', args.output + '/merged.tif')
    print("Merge complete")
