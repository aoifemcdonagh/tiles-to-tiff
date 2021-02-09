"""
Convert existing ESRI tiles to .tif files using custom naming convention

ESRI tile naming convention: "large_tile_x00000_y00000_z00_w64_h64.png"
"""
import os
import subprocess
import glob
import shutil
from osgeo import gdal
from tile_convert import tile_edges

temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
output_dir = os.path.join(os.path.dirname(__file__), 'output')

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


def georeference_raster_tile(x, y, z, path, w=1, h=1,):
    bounds = tile_edges(x, y, z, w, h)
    name, extension = os.path.splitext(os.path.basename(path))
    tif_path = temp_dir + "/" + name + '.tif'
    gdal.Translate(tif_path,
                   path,
                   outputSRS='EPSG:4326',
                   outputBounds=bounds)


if __name__ == "__main__":
    args = get_args()

    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # iterate over files in png directory
    for filename in os.listdir(args.png):
        if filename.endswith(".png"):
            # get x, y, z values from filename
            x_val, y_val, zoom, w_val, h_val = 0, 0, 0, 1, 1
            image_data, _ = os.path.splitext(filename)  # get name without extension which contains image data
            values = image_data.split("_")  # split on underscore
            for val in values:
                if val[0] == "x":
                    x_val = int(val[1:])
                if val[0] == "y":
                    y_val = int(val[1:])
                if val[0] == "z":
                    zoom = int(val[1:])
                if val[0] == "w":
                    w_val = int(val[1:])
                if val[0] == "h":
                    h_val = int(val[1:])

            filepath = args.png + "/" + filename

            # convert .png files to .tif
            georeference_raster_tile(x_val, y_val, zoom, filepath, w=w_val, h=h_val)

    print("Merging tiles")
    merge_tiles(temp_dir + '/*.tif', args.output + '/merged.tif')
    print("Merge complete")

    shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)
