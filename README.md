# CI Pipeline Demo — GitHub Actions & Docker

A hands-on DevOps project demonstrating an automated CI pipeline for a Python Flask application using GitHub Actions, pytest, Docker, and Docker Hub.

The pipeline validates application changes, builds a container image, and publishes branch-specific Docker images after successful tests.

## CI Pipeline Architecture

```text
Push / Pull Request
        |
        v
GitHub Actions
        |
        v
Run Python Tests (pytest)
        |
        +---- Failed → Stop
        |
        v
Tests Passed
        |
        +---- Pull Request / Other Branch → Finish
        |
        +---- Push to main or dev
                    |
                    v
             Build Docker Image
                    |
                    v
             Push to Docker Hub
                    |
                    v
             SHA-based Image Tag
```

## Technologies

- GitHub Actions — CI automation
- Python 3.12 — application runtime
- Flask — sample web application
- pytest — automated testing
- Docker — containerization
- Docker Hub — image registry
- actionlint — workflow validation

## Project Structure

```text
ci-pipeline-demo/
├── .github/
│   └── workflows/
│       └── ci.yaml
├── tests/
│   └── test_flask_app.py
├── .dockerignore
├── Dockerfile
├── app.py
├── requirements.txt
└── README.md
```

## How the Pipeline Works

### 1. Automated testing

The pipeline runs on pushes to branches and on pull requests.

It installs Python dependencies and executes automated tests using pytest.

If tests fail, the Docker publishing job does not run.

### 2. Docker build and publishing

Docker images are published only after successful tests on pushes to `main` or `dev`.

Other branches and pull requests can run tests without publishing images.

### 3. Branch-based image tagging

| Branch | Docker image tag |
|---|---|
| `main` | `prod-<commit-sha>` |
| `dev` | `dev-<commit-sha>` |
| Other branches | No image published |

Commit-SHA-based tags improve traceability by linking published images to their source commits.

## Container Security

The Docker configuration includes:

- Python 3.12 slim base image
- Non-root application user (`appuser`, UID 10001)
- `.dockerignore` to exclude unnecessary files
- Only required application files copied into the runtime image
- Python bytecode generation disabled
- Pip installation without a download cache

The GitHub Actions workflow uses restricted repository permissions and GitHub Secrets for Docker Hub authentication.

A local Gitleaks scan of the repository's Git history reported no findings during project review.

## Run Locally

### Build the image

```bash
docker build -t ci-pipeline-demo:local .
```

### Start the container

```bash
docker run -d --rm --name ci-pipeline-test -p 5000:5000 ci-pipeline-demo:local
```

### Test the application

```bash
curl -i http://localhost:5000/
```

Expected response:

```text
HTTP/1.1 200 OK

Hello from CI Pipeline! 🚀
```

### Verify non-root execution

```bash
docker exec ci-pipeline-test id
```

Verified user:

```text
uid=10001(appuser) gid=10001(appuser) groups=10001(appuser)
```

### Stop the container

```bash
docker stop ci-pipeline-test
```

## Automated Tests

The project includes a pytest test using Flask's test client.

The test verifies that the root endpoint responds with HTTP 200 and contains the expected greeting.

Tests passed locally using Python 3.12 inside Docker.

## CI Verification Evidence

The pipeline was successfully tested on the `dev` branch.

**Successful GitHub Actions run:**

[CI Pipeline — Run #16](https://github.com/YuliMed/ci-pipeline-demo/actions/runs/44287770294)

**Docker build and publishing job:**

[Build and Publish Docker Image](https://github.com/YuliMed/ci-pipeline-demo/actions/runs/44287770294/job/134744867889)

Verified results:

| Check | Result |
|---|---|
| Python tests | Passed |
| Docker image build | Passed |
| Docker Hub publishing | Passed |
| Local HTTP test | 200 OK |
| Non-root container | Verified |
| actionlint | Passed |
| Gitleaks scan | No findings |

## Project Scope

This project focuses on continuous integration and container image publishing.

It does not automatically deploy the application to Kubernetes or a production environment.

The branch-based image tags could be used by a separate deployment or GitOps workflow.

## Future Improvements

- Add dependency vulnerability scanning
- Add automated Docker image smoke tests to CI
- Pin GitHub Actions to commit SHAs
- Add dependency update automation
- Expand application test coverage

## Key Learning Outcomes

- Building GitHub Actions workflows
- Running automated tests before publishing images
- Managing job dependencies and branch conditions
- Publishing traceable Docker images
- Using GitHub Secrets for registry authentication
- Improving Docker container security
- Validating CI workflows and collecting execution evidence

