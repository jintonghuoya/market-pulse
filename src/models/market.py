"""Market-level data models for standardized metrics."""


# Standard field mappings per data source
COSTAR_MARKET_FIELDS = {
    "vacancy_rate": ["Vacancy Rate", "Vacancy Rate (%)", "vacancy_rate"],
    "avg_rent": ["Average Rent", "Avg Rent", "Asking Rent", "avg_rent_psf"],
    "net_absorption": ["Net Absorption", "Net Absorption (SF)", "net_absorption"],
    "new_supply": ["New Supply", "Completions", "New Supply (SF)"],
    "inventory": ["Inventory", "Total Inventory", "Total Stock (SF)"],
    "market": ["Market", "MSA", "Metro Area", "City"],
    "property_type": ["Property Type", "Sector", "Type"],
    "period": ["Date", "Period", "Quarter", "Year"],
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
