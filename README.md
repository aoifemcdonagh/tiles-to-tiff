# tiles-to-tiff
Python script for converting XYZ raster tiles for slippy maps to a georeferenced TIFF image. Written for this tutorial: https://dev.to/jimutt/generate-merged-geotiff-imagery-from-web-maps-xyz-tile-servers-with-python-4d13

## Prerequisites:
- GDAL
- Empty "output" and "temp" folders in project directory. 

## Usage:
- Modify configuration in `tiles_to_tiff.py` according to personal preferences.
- Run script with `$ python tiles_to_tiff.py`

For more information see the accompanying dev.to post. 

## esri_to_tiff.py
- Convert existing ESRI tiles to .tif files using custom naming convention  
- ESRI tile naming convention: "large_tile_x00000_y00000_z00_w64_h64.png"  
    - 'x': x origin point of image
    - 'y': y origin point of image
    - 'z': zoom level
    - 'w': width of ESRI image in tiles
    - 'h': height of ESRI image in tiles
