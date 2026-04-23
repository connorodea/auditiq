from auditiq.services.scoring import (
    DimensionScore,
    calculate_all_scores,
    calculate_overall_score,
    estimate_roi,
    get_maturity_level,
    score_dimension,
)


def test_maturity_levels():
    assert get_maturity_level(0) == "Nascent"
    assert get_maturity_level(29) == "Nascent"
    assert get_maturity_level(30) == "Emerging"
    assert get_maturity_level(54) == "Emerging"
    assert get_maturity_level(55) == "Established"
    assert get_maturity_level(79) == "Established"
    assert get_maturity_level(80) == "Advanced"
    assert get_maturity_level(100) == "Advanced"


def test_score_dimension_all_ones():
    responses = [
        {"answer_score": 1, "weight": 1.0},
        {"answer_score": 1, "weight": 1.0},
        {"answer_score": 1, "weight": 1.0},
    ]
    result = score_dimension("data_readiness", responses)
    assert result.normalized == 25
    assert result.level == "Nascent"


def test_score_dimension_all_fours():
    responses = [
        {"answer_score": 4, "weight": 1.0},
        {"answer_score": 4, "weight": 1.0},
        {"answer_score": 4, "weight": 1.0},
    ]
    result = score_dimension("data_readiness", responses)
    assert result.normalized == 100
    assert result.level == "Advanced"


def test_score_dimension_mixed():
    responses = [
        {"answer_score": 2, "weight": 1.0},
        {"answer_score": 3, "weight": 1.0},
        {"answer_score": 1, "weight": 1.0},
    ]
    result = score_dimension("process_maturity", responses)
    # (2+3+1) / (4+4+4) = 6/12 = 50%
    assert result.normalized == 50
    assert result.level == "Emerging"


def test_score_dimension_weighted():
    responses = [
        {"answer_score": 4, "weight": 2.0},  # Double weight
        {"answer_score": 1, "weight": 1.0},
        {"answer_score": 1, "weight": 1.0},
    ]
    result = score_dimension("tech_infrastructure", responses)
    # (4*2 + 1*1 + 1*1) / (4*2 + 4*1 + 4*1) = 10/16 = 62.5% -> 62
    assert result.normalized == 62
    assert result.level == "Established"


def test_score_dimension_empty():
    result = score_dimension("data_readiness", [])
    assert result.normalized == 0
    assert result.level == "Nascent"


def test_calculate_overall_score():
    dimension_scores = {
        "data_readiness": DimensionScore("data_readiness", 0, 0, 60, "Established"),
        "process_maturity": DimensionScore("process_maturity", 0, 0, 40, "Emerging"),
        "tech_infrastructure": DimensionScore("tech_infrastructure", 0, 0, 80, "Advanced"),
        "team_capability": DimensionScore("team_capability", 0, 0, 50, "Emerging"),
        "strategic_alignment": DimensionScore("strategic_alignment", 0, 0, 70, "Established"),
    }
    # 60*0.25 + 40*0.20 + 80*0.20 + 50*0.20 + 70*0.15
    # = 15 + 8 + 16 + 10 + 10.5 = 59.5 -> 60
    overall = calculate_overall_score(dimension_scores)
    assert overall == 60


def test_calculate_all_scores():
    responses_by_dimension = {
        "data_readiness": [
            {"answer_score": 3, "weight": 1.0},
            {"answer_score": 2, "weight": 1.0},
            {"answer_score": 3, "weight": 1.0},
        ],
        "process_maturity": [
            {"answer_score": 2, "weight": 1.0},
            {"answer_score": 2, "weight": 1.0},
            {"answer_score": 1, "weight": 1.0},
        ],
        "tech_infrastructure": [
            {"answer_score": 3, "weight": 1.0},
            {"answer_score": 3, "weight": 1.0},
            {"answer_score": 2, "weight": 1.0},
        ],
        "team_capability": [
            {"answer_score": 2, "weight": 1.0},
            {"answer_score": 3, "weight": 1.0},
            {"answer_score": 2, "weight": 1.0},
        ],
        "strategic_alignment": [
            {"answer_score": 1, "weight": 1.0},
            {"answer_score": 2, "weight": 1.0},
            {"answer_score": 2, "weight": 1.0},
        ],
    }
    scores = calculate_all_scores(responses_by_dimension)
    assert "overall" in scores
    assert "overall_level" in scores
    assert isinstance(scores["data_readiness"], DimensionScore)


def test_estimate_roi_small_company():
    roi = estimate_roi(40, "retail", "1-10")
    assert roi["estimated_annual_savings_low"] > 0
    assert roi["estimated_annual_savings_high"] > roi["estimated_annual_savings_low"]
    assert roi["estimated_hours_saved_weekly"] > 0
    assert roi["payback_period_months"] >= 2


def test_estimate_roi_large_company():
    roi = estimate_roi(80, "technology", "201-1000")
    # High score = smaller gap = lower estimated savings
    roi_low = estimate_roi(20, "technology", "201-1000")
    assert roi["estimated_annual_savings_high"] < roi_low["estimated_annual_savings_high"]
