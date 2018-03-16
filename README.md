# SQUAD Plugin for QGIS

The Spatial Quality and Anomalies Diagnosis (SQUAD) tool checks for six anomalies that are based on common errors in point-location data sets. This information can be used to prioritize the type and extent of investigation needed for records that may have problems. The anomalies that can be checked are:

1. Missing coordinates
2. Truncated coordinates (lack of adequate precision)
3. Duplicate coordinates for distinct records
4. Duplicate key attributes (two identical names, but plotting in different locations)
5. Coordinate not located exactly where it would be expected (but falling within two kilometers of a border)
6. Coordinate not located anywhere near where expected

# Installation (manual)

## Downloading release code (for Windows users)

- Download the code from here
- Extract from zip file
- Rename folder to squad-plugin
- Copy the plugin into the .qgis2/python/plugins folder in your home directory

## Cloning repo (for Linux/Mac users)

- Open a terminal.
- Execute:
- git clone https://github.com/andre-ws/squad-plugin.git
  - cd squad-plugin
  - make install

## Enabling plugin

- Open QGIS
- Go to "Plugins"=>"Manage and install plugins"
- Click on "Installed" and enable "SQUAD Plugin"
