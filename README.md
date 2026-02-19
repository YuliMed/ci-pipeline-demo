# CI Pipeline Demo

## Assignment Answers

### 1. Why should `kubectl apply` not be used in CI?
`kubectl apply` is imperative and non-declarative—it's like "push this now" vs. "this is the desired state." In CI:
- **Security risk:** You'd expose cluster creds (Kubeconfig) to runners.
- **Drift potential:** Applies can overwrite live state without Git review.

### 2. Why is `latest` a bad Docker tag?
- **Mutable:** `docker pull myapp:latest` could pull v1.2 today, v1.3 tomorrow. No traceability.
- **Rollback issues:** Can't easily revert to "last known good."
- **Cache bloat:** Layers change unpredictably, slowing builds.
- **Best practice:** Always tag with SHA (`:abc123`), semver (`:1.0.0`), or env (`:prod-abc123`). `latest` is for quick demos only.

### 3. What is the difference between CI and CD?
- **CI (Continuous Integration):** Automates *building + testing* code changes. Goal: Catch bugs early via frequent merges . "Integrate often."
- **CD (Continuous Delivery/Deployment):** Automates *releasing* to prod/staging. Triggered by CI success. Includes deploy, rollbacks. "Deliver continuously."


### 4. How does this pipeline support GitOps?
GitOps = "Git is the single source of truth" for infra/apps (declarative YAML in Git → operators apply).
- This pipeline: On push, builds/pushes *immutable image* tagged with SHA.
- In a full GitOps setup: Update your `deployment.yaml` (in a separate "manifests" repo) to reference `myapp:abc123`. ArgoCD/Flux detects the change → deploys.
- Supports "pull-based" deploys: No direct kubectl from CI. Code change → image → Git PR → deploy. Traceable, auditable, reversible.

