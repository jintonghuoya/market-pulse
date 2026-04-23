"""Market-level data models for standardized metrics."""


# Standard field mappings per data source
COSTAR_MARKET_FIELDS = {
    # Identifiers
    "period": ["Period"],
    "market": ["Market", "MSA", "Metro Area", "City"],
    "submarket": ["Submarket"],
    "property_type": ["Property Type", "Sector", "Type"],
    "geography_name": ["Geography Name"],
    # Core hospitality metrics
    "occupancy": ["Occupancy"],
    "occupancy_yoy": ["Occupancy Chg (YOY)"],
    "adr": ["ADR"],
    "adr_yoy": ["ADR Chg (YOY)"],
    "revpar": ["RevPAR"],
    "revpar_yoy": ["RevPAR Chg (YOY)"],
    "demand": ["Demand"],
    "demand_yoy": ["Demand Chg (YOY)"],
    "supply": ["Supply"],
    "supply_yoy": ["Supply Chg (YOY)"],
    "revenue": ["Revenue"],
    "revenue_yoy": ["Revenue Chg (YOY)"],
    # Investment metrics
    "cap_rate": ["Market Cap Rate"],
    "cap_rate_growth": ["Market Cap Rate Growth"],
    "sale_price_per_room": ["Market Sale Price/Room"],
    "sale_price_growth": ["Market Sale Price/Room Growth"],
    "asset_value": ["Asset Value"],
    # Inventory
    "existing_buildings": ["Existing Buildings"],
    "inventory_rooms": ["Inventory Rooms"],
    "under_construction_rooms": ["Under Construction Rooms"],
    # 12-month rolling
    "occupancy_12m": ["12 Mo Occupancy"],
    "adr_12m": ["12 Mo ADR"],
    "revpar_12m": ["12 Mo RevPAR"],
    "demand_12m": ["12 Mo Demand"],
    "supply_12m": ["12 Mo Supply"],
}


def normalize_columns(df, field_map=COSTAR_MARKET_FIELDS):
    """Rename columns to standardized names based on field mapping.

    Returns DataFrame with normalized column names.
    """
    rename = {}
    for std_name, aliases in field_map.items():
        for alias in aliases:
            if alias in df.columns:
                rename[alias] = std_name
                break
    return df.rename(columns=rename)
