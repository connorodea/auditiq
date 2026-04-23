import pytest


@pytest.fixture
def sample_responses():
    """Sample responses for testing scoring."""
    return {
        "data_readiness": [
            {"answer_score": 2, "weight": 1.0},
            {"answer_score": 3, "weight": 1.0},
            {"answer_score": 2, "weight": 1.0},
        ],
        "process_maturity": [
            {"answer_score": 1, "weight": 1.0},
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
            {"answer_score": 2, "weight": 1.0},
            {"answer_score": 1, "weight": 1.0},
        ],
        "strategic_alignment": [
            {"answer_score": 1, "weight": 1.0},
            {"answer_score": 2, "weight": 1.0},
            {"answer_score": 1, "weight": 1.0},
        ],
    }
