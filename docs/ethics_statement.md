# Ethics and Policy Statement - PPE Detection System

## Intended Use
This system detects PPE-related objects in worksite images and video frames to support safety monitoring. It is intended as a decision-support tool for safety officers, not as an automated enforcement system.

## Out-of-Scope Use
- Identity recognition or facial recognition.
- Employee productivity scoring.
- Fully automated disciplinary decisions without human review.

## Key Risks and Mitigations

### 1. Privacy and Surveillance Risk
Risk: Camera feeds may capture workers without meaningful awareness or consent.
Mitigations:
- Deploy clear signage at camera-monitored zones.
- Minimize retention (store only alerts and limited audit samples).
- Avoid storing raw full-resolution streams when not required.
- Restrict access to authorized safety personnel only.

### 2. False Positives and False Negatives
Risk: Incorrect detections may trigger unnecessary alerts or miss real safety violations.
Mitigations:
- Require human confirmation before punitive actions.
- Use confidence thresholds and tune by operating context.
- Track false-positive and false-negative rates over time.
- Add periodic retraining with newly collected edge cases.

### 3. Fairness and Domain Shift
Risk: Performance may degrade across lighting, camera angle, weather, PPE style, and site differences.
Mitigations:
- Perform slice analysis by site, shift, lighting condition, and camera viewpoint.
- Expand dataset coverage for underperforming slices.
- Report per-slice metrics in model updates.
- Gate deployment in new sites behind pilot validation.

## Data Governance
- Source: Roboflow PPE Combined v8.
- License: CC BY 4.0 (dataset), MIT (project code).
- PII handling: No identity labeling is used by design.
- Consent: Follow institutional and site policies for camera data usage and notification.

## Human Oversight Policy
- Alerts are advisory only.
- Final safety judgment must involve a trained human reviewer.
- Escalation workflow should include appeal and correction paths.

## Security and Operational Controls
- Log model version, threshold, and timestamp for each alert.
- Maintain strict access control for model outputs.
- Keep a rollback path to prior stable model versions.

## Deployment Limitations
- Not suitable for medical or legal determinations.
- Not guaranteed under severe occlusion or extreme image quality degradation.
- Should not be treated as the sole safety control.

## Monitoring and Review
- Review performance monthly or after major environment changes.
- Re-run slice analysis before each tagged release.
- Update model card and this statement when data or policy changes.
