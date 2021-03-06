parameters_desc = {
	"ADMIN_UNITS_LAYER":
		"Browse to a polygon feature class containing the administrative" \
		" units into which the sites are expected to fall. This file will" \
		" be used to gauge the geographic accuracy of the site locations. "
	, "SITE_LONGITUDE_FIELD":
		"Choose the field that contains the longitude (or X) coordinate."
	, "SITE_ID_FIELD":
		"Choose the field that contains the unique ID for the site. "
	, "SITES_LAYER":
		"Browse to the location of the feature class that contains the" \
		" point sites to be evaluated. \nThis point file must contain:" \
		"\n- A field with a unique identifier" \
		"\n- Separate fields for X (longitude) and Y (latitude) coordinates" \
		"\n- A field with a facility name" \
		"\n- A field indicating the administrative unit where the point" \
		" is expected to be located"
	, "SITE_LATITUDE_FIELD":
		"Choose the field that contains the latitude (or Y) coordinate."
	, "SITE_ADMIN_UNIT_FIELD":
		"Choose from the pop-up menu the name of the field in the site file" \
		" that contains the name of the administrative unit where the site" \
		" is expected to be located." \
		"\nThis field must be a text field."
	, "ADMIN_UNIT_NAME_FIELD":
		"Choose from the pop-up menu the field in the Administrative Unit" \
		"\nFeature Class that contains the name of the unit." \
		"\nThe list of names used for administrative units in both the point" \
		" file and administrative unit file must match. In other words," \
		" there should be no administrative unit names in the point file" \
		" that aren'trepresented by a polygon in the administrative unit" \
		" file. Spelling and naming conventions (i.e., \"Western\" vs." \
		"  \"Western District\") should be consistent."
	, "SITE_NAME_FIELD":
		"Choose the field that contains the name of the site (i.e., New Hope" \
		" Primary Clinic)."
	, "OUTPUT_LAYER":
		"File where the original points will be saved along with the" \
		" anomalies found."
}