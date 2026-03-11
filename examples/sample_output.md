# Sample Review Prompt

## Pull Request Title
Refactor payment retry logic

## Summary
This pull request moves payment retry logic into a shared service, updates job scheduling, and adds a retry configuration object used by multiple workers.

## Changed Files
app/services/retry_service.py
app/jobs/process_retry.py
tests/test_retry_service.py

## Additional Context
The system processes background jobs for merchant payouts.

## Requested Output
1. High-Risk Findings
2. Behavioral Regression Risks
3. Missing Tests or Validation
4. Security or Reliability Concerns
5. Documentation or Rollout Gaps
6. Final Review Recommendation

## Review Mode
general
