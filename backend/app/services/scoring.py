# scoring.py
from pydantic import BaseModel
from typing import Dict

# Data model representing an area (state or metro) with relevant metrics
class Area(BaseModel):
    '''
    Defines an Area (U.S. state or metro) with relevant metrics
    '''
    name: str
    cost_of_living: float       # cost of living index (lower is better)
    median_rent: float         # median rent for a two-bedroom (lower is better)
    pct_new_renter_structures: float # percentage built after 2000 (higher is better)
    pct_income_spent_on_rent: float # percentage of income spent on rent (lower is better)
    renters_insurance: float    # monthly const of renter's insurance (lower is better)
    vacancy_rate: float         # rental vacancy rate (lower is better)
    pct_grapi_below_threshold: float # percentage paying less than 34.9% gross rent as a percentage of household income (lower is better)
    electricity_bill: float     # average monthly cost of electricity (lower is better)
    job_growth: float           # job growth (higher is better)
    unemployment: float         # unemployment rate (lower is better)
    commute_time: float         # average commute time (lower is better)
    walk_score: float           # walk score (higher is better)
    transit_score: float       # transit score (higher is better)
    bike_score: float          # bike score (higher is better)
    eviction_laws: float       # renter-friendly eviction laws (1 is friendly, 0 is not)
    lead_service_lines: float  # lead service lines per 100,000 people (lower is better)
    

def normalize(value:float, min_val:float, max_val:float, lower_is_better:bool) -> float:
    '''
    Normalize a value to a range of 0-10 based on the min and max values.
    If lower_is_better is True, then lower values are better.
    If lower_is_better is False, then higher values are better.
    '''
    if lower_is_better:
        normalized = (max_val - value) / (max_val - min_val)
    else:
        normalized =  (value - min_val) / (max_val - min_val)
    
    # clamp the value to [0, 1] range and scale to [0, 10]
    normalized = max(0.0, min(normalized, 1.0))
    return normalized * 10
