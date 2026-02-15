from app.models.entities import MonetizationMetric, VerificationState


def compute_verification_state(metric: MonetizationMetric | None) -> VerificationState:
    if metric is None:
        return VerificationState.NOT_ELIGIBLE
    if metric.suspicious_growth_score > 80:
        return VerificationState.REVOKED
    if metric.posts_count >= 10 and metric.followers_count >= 500 and metric.total_reach >= 50_000:
        return VerificationState.ELIGIBLE
    return VerificationState.NOT_ELIGIBLE
