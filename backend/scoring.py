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
    median_rent: float         # median rent for a one-bedroom (lower is better)
    pct_new_renter_structures: float # number of apartments delivered in the last 12 months (higher is better)
    pct_income_spent_on_rent: float # percentage of income spent on rent (lower is better)
    renters_insurance: float    # monthly const of renter's insurance (lower is better)
    vacancy_rate: float         # rental vacancy rate (lower is better)
    pct_grapi_below_threshold: float # percentage paying less than 34.9% gross rent as a percentage of household income (lower is better)
    electricity_bill: float     # average monthly cost of electricity (lower is better)
    job_growth: float           # job growth (higher is better)
    unemployment: float         # unemployment rate (lower is better)
    commute_time: float         # average commute time in minutes (lower is better)
    walk_score: float           # walk score (higher is better)
    transit_score: float       # transit score (higher is better)
    bike_score: float          # bike score (higher is better)
    eviction_laws: float       # renter-friendly eviction laws (1 is friendly, 0 is not)

def normalize(value:float, min_val:float, max_val:float, lower_is_better:bool) -> float:
    '''
    Normalize a value to a range of 0-10 based on min and max values, and whether lower values are better.
    '''
    if lower_is_better:
        normalized = (max_val - value) / (max_val - min_val)
    else:
        normalized =  (value - min_val) / (max_val - min_val)
    
    # clamp the value to [0, 1] range and scale to [0, 10]
    normalized = max(0.0, min(normalized, 1.0))
    return normalized * 10

# Normalization parameters based on real-world data ranges
normalization_params: Dict[str, Dict[str, float or bool]] = {
    "cost_of_living": {"min": 70, "max": 160, "lower_is_better": True},
    "median_rent": {"min": 1000, "max": 4000, "lower_is_better": True},
    "pct_new_renter_structures": {"min": 0, "max": 100000, "lower_is_better": False},
    "pct_income_spent_on_rent": {"min": 0, "max": 50, "lower_is_better": True},
    "renters_insurance": {"min": 0, "max": 50, "lower_is_better": True},
    "vacancy_rate": {"min": 0, "max": 11, "lower_is_better": True},
    "pct_grapi_below_threshold": {"min": 0, "max": 100, "lower_is_better": False},   
    "electricity_bill": {"min": 0, "max": 300, "lower_is_better": True},
    "job_growth": {"min": -5, "max": 10, "lower_is_better": False},
    "unemployment": {"min": 2, "max": 12, "lower_is_better": True},
    "commute_time": {"min": 10, "max": 120, "lower_is_better": True},
    "walk_score": {"min": 0, "max": 100, "lower_is_better": False},
    "transit_score": {"min": 0, "max": 100, "lower_is_better": False},
    "bike_score": {"min": 0, "max": 100, "lower_is_better": False},
    "eviction_laws": {"min": 0, "max": 1, "lower_is_better": False},
}

# Weights for each metric (sum to 1 for simplicity)
weights: Dict[str, float] = {
    "cost_of_living": 0.1,
    "median_rent": 0.1,
    "pct_new_renter_structures": 0.1,
    "pct_income_spent_on_rent": 0.1,
    "renters_insurance": 0.05,
    "vacancy_rate": 0.05,
    "pct_grapi_below_threshold": 0.1,
    "electricity_bill": 0.05,
    "job_growth": 0.1,
    "unemployment": 0.1,
    "commute_time": 0.05,
    "walk_score": 0.05,
    "transit_score": 0.05,
    "bike_score": 0.05,
    "eviction_laws": 0.05,
}

TOTAL_WEIGHT = sum(weights.values())

def calculate_score(area: Area) -> float:
    '''
    Calculate the composite score for an area based on the weighted normalized metrics.
    '''
    total = 0.0
    for metric, weight in weights.items():
        raw_value = getattr(area, metric)
        params = normalization_params[metric]
        metric_score = normalize(raw_value, params["min"], params["max"], params["lower_is_better"])
        total += weight * metric_score
    
    composite_score = total / TOTAL_WEIGHT
    return composite_score


if __name__ == "__main__":
    # Example usage - Orlando, FL
    orl_fl = Area(
        name="Orlando",
        cost_of_living=102.3,
        median_rent=1581,
        pct_new_renter_structures=10000,
        pct_income_spent_on_rent=33.33,
        renters_insurance=22,
        vacancy_rate=10.9,
        pct_grapi_below_threshold=39,
        electricity_bill=276,
        job_growth=1.2,
        unemployment=2.8,
        commute_time=27.5,
        walk_score=41,
        transit_score=55,
        bike_score=26,
        eviction_laws=0,
    )
    orl_fl_score = calculate_score(orl_fl)
    print(f"The composite score to rent in {orl_fl.name} is {orl_fl_score:.2f} / 10")

    # Example usage - National Average for US Cities, USA
    # Average renter makes $54,712 per year
    # Average rent is $1,462 per month
    usa = Area(
        name="US Cities",
        cost_of_living=70.4,
        median_rent=1462,
        pct_new_renter_structures=44000, #https://www.statista.com/statistics/590728/number-of-new-apartments-us/
        pct_income_spent_on_rent=32,
        renters_insurance=23,
        vacancy_rate=6.9,
        pct_grapi_below_threshold=52.5,
        electricity_bill=116,
        job_growth=2,
        unemployment=4,
        commute_time=26,
        walk_score=48,
        transit_score=55,
        bike_score=25,
        eviction_laws=1,
    )
    usa_score = calculate_score(usa)
    print(f"As a reference, the composite score to rent in {usa.name} is {usa_score:.2f} / 10")