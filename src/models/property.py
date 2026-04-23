"""Property-level data models."""


# Standard field mappings for property data
COSTAR_PROPERTY_FIELDS = {
    "address": ["Address", "Property Address", "Street Address"],
    "city": ["City", "MSA", "Market"],
    "property_type": ["Property Type", "Sector", "Type"],
    "sub_type": ["Sub Type", "Building Type", "Subtype"],
    "size_sf": ["Size (SF)", "Building Size", "GLA", "Rentable Area"],
    "year_built": ["Year Built", "Built", "Construction Year"],
    "occupancy": ["Occupancy", "Occupancy (%)", "Occupancy Rate"],
    "rent_psf": ["Rent ($/SF)", "Asking Rent", "Rent/SF"],
    "sale_price": ["Sale Price", "Price", "Last Sale Price"],
    "cap_rate": ["Cap Rate", "Cap Rate (%)"],
    "owner": ["Owner", "Owner Name"],
}


def normalize_property_columns(df, field_map=COSTAR_PROPERTY_FIELDS):
    """Rename property-level columns to standardized names."""
    rename = {}
    for std_name, aliases in field_map.items():
        for alias in aliases:
            if alias in df.columns:
                rename[alias] = std_name
                break
    return df.rename(columns=rename)
