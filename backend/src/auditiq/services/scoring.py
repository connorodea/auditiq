from dataclasses import dataclass


DIMENSION_WEIGHTS: dict[str, float] = {
    "data_readiness": 0.25,
    "process_maturity": 0.20,
    "tech_infrastructure": 0.20,
    "team_capability": 0.20,
    "strategic_alignment": 0.15,
}

INDUSTRY_BENCHMARKS: dict[str, dict[str, int]] = {
    "healthcare": {"median_overall": 42, "top_quartile": 68},
    "finance": {"median_overall": 58, "top_quartile": 78},
    "retail": {"median_overall": 45, "top_quartile": 65},
    "ecommerce": {"median_overall": 52, "top_quartile": 72},
    "manufacturing": {"median_overall": 35, "top_quartile": 55},
    "professional_services": {"median_overall": 50, "top_quartile": 70},
    "technology": {"median_overall": 65, "top_quartile": 85},
    "education": {"median_overall": 38, "top_quartile": 58},
    "real_estate": {"median_overall": 33, "top_quartile": 52},
    "construction": {"median_overall": 30, "top_quartile": 48},
    "logistics": {"median_overall": 40, "top_quartile": 60},
    "hospitality": {"median_overall": 35, "top_quartile": 55},
    "legal": {"median_overall": 38, "top_quartile": 58},
    "other": {"median_overall": 45, "top_quartile": 65},
}

SIZE_MULTIPLIERS: dict[str, dict[str, int]] = {
    "1-10": {"revenue_base": 500_000, "employee_cost": 60_000},
    "11-50": {"revenue_base": 3_000_000, "employee_cost": 65_000},
    "51-200": {"revenue_base": 15_000_000, "employee_cost": 70_000},
    "201-1000": {"revenue_base": 75_000_000, "employee_cost": 75_000},
    "1000+": {"revenue_base": 500_000_000, "employee_cost": 80_000},
}


@dataclass
class DimensionScore:
    dimension: str
    raw_score: float
    max_possible: float
    normalized: int
    level: str


def get_maturity_level(score: int) -> str:
    if score >= 80:
        return "Advanced"
    elif score >= 55:
        return "Established"
    elif score >= 30:
        return "Emerging"
    return "Nascent"


def score_dimension(
    dimension: str,
    responses: list[dict[str, float]],
) -> DimensionScore:
    """Score a single dimension from its responses.

    Args:
        dimension: The dimension name.
        responses: List of dicts with "answer_score" and "weight" keys.
    """
    if not responses:
        return DimensionScore(
            dimension=dimension,
            raw_score=0,
            max_possible=0,
            normalized=0,
            level="Nascent",
        )

    weighted_sum = sum(r["answer_score"] * r["weight"] for r in responses)
    max_possible = sum(4 * r["weight"] for r in responses)

    normalized = round((weighted_sum / max_possible) * 100) if max_possible > 0 else 0
    level = get_maturity_level(normalized)

    return DimensionScore(
        dimension=dimension,
        raw_score=weighted_sum,
        max_possible=max_possible,
        normalized=normalized,
        level=level,
    )


def calculate_overall_score(dimension_scores: dict[str, DimensionScore]) -> int:
    """Weighted average across all dimensions."""
    total = sum(
        ds.normalized * DIMENSION_WEIGHTS.get(dim, 0.0)
        for dim, ds in dimension_scores.items()
    )
    return round(total)


def calculate_all_scores(
    responses_by_dimension: dict[str, list[dict[str, float]]],
) -> dict[str, DimensionScore | int | str]:
    """Calculate all dimension scores and overall score.

    Args:
        responses_by_dimension: Dict mapping dimension name to list of
            {"answer_score": int, "weight": float} dicts.

    Returns:
        Dict with dimension names mapping to DimensionScore objects,
        plus "overall" (int) and "overall_level" (str).
    """
    dimension_scores: dict[str, DimensionScore] = {}
    for dim in DIMENSION_WEIGHTS:
        dim_responses = responses_by_dimension.get(dim, [])
        dimension_scores[dim] = score_dimension(dim, dim_responses)

    overall = calculate_overall_score(dimension_scores)

    result: dict[str, DimensionScore | int | str] = dict(dimension_scores)
    result["overall"] = overall
    result["overall_level"] = get_maturity_level(overall)
    return result


def estimate_roi(
    overall_score: int,
    industry: str,
    company_size: str,
) -> dict[str, int | str]:
    """Estimate ROI based on scores, industry, and company size."""
    gap = 100 - overall_score
    efficiency_gain_pct = (gap / 100) * 0.15

    base = SIZE_MULTIPLIERS.get(company_size, SIZE_MULTIPLIERS["11-50"])

    return {
        "estimated_annual_savings_low": round(base["revenue_base"] * efficiency_gain_pct * 0.02),
        "estimated_annual_savings_high": round(base["revenue_base"] * efficiency_gain_pct * 0.08),
        "estimated_hours_saved_weekly": round(gap * 0.3),
        "payback_period_months": max(2, round(12 - (overall_score / 10))),
    }


def get_industry_benchmark(industry: str) -> dict[str, int]:
    return INDUSTRY_BENCHMARKS.get(industry, INDUSTRY_BENCHMARKS["other"])
