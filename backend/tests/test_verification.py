from app.models.entities import MonetizationMetric, VerificationState
from app.services.verification import compute_verification_state


def test_verification_eligible() -> None:
    metric = MonetizationMetric(posts_count=12, followers_count=1000, total_reach=200000, suspicious_growth_score=0)
    assert compute_verification_state(metric) == VerificationState.ELIGIBLE


def test_verification_revoked_on_suspicious_growth() -> None:
    metric = MonetizationMetric(posts_count=500, followers_count=50000, total_reach=4_000_000, suspicious_growth_score=99)
    assert compute_verification_state(metric) == VerificationState.REVOKED
