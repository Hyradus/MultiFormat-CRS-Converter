## **Multiple-format CRS Converter**
Usually reproject manually multiple files that have different crs can be tedious so this script and notebook may help.

## Brief description
This notebook reproject all shp/SHP, tiff/TIFF, tif/tif, gpkg/GPKG from a user-selected folder that have a valid crs to user input CRS.

Both script ask:
- **Output folder
- **Input folder
- ** Destination CRS


### Standalone
Is not recursive and convert only files available in the input folder


### Recursive
The RecursiveDirectory notebook and script create a list of folders and sub-folders in user input, then search for all files and reproject only compatible files while incompatible files are stored in ad-hoc subdirectories.
It also save a WKT file containing the source crs.
--------------------------------------------------------------------------

**Note: All file with extension different from [shp/SHP, tiff/TIFF, tif/tif, gpkg/GPKG] are copied inside a “non gis files” sub-folder in each folder.**





## **TO-DO**
- [X] Add recursive search
- [X] Add a function to move all not supported files in the destination path, recustructing the original strucutre of the directories.
- [ ] Parallelize everything

For problems contact: g.nodjoumi@jacobs-university.de
