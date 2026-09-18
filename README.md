# Selenium Python Page Object Model

An end-to-end UI test automation project for Amazon search flows. It applies the Page Object Model (POM) to keep page interactions separate from test assertions and supports Chrome and Firefox locally and in GitHub Actions.

## Technology stack

| Technology | Purpose |
| --- | --- |
| Python 3.14+ | Test implementation |
| [uv](https://docs.astral.sh/uv/) | Python version and dependency management |
| [Pytest](https://docs.pytest.org/) | Test runner, fixtures, markers, and parametrization |
| [Selenium](https://www.selenium.dev/) | Browser automation |
| Chrome / Firefox | Browsers under test |
| [Allure](https://allurereport.org/) | Rich test-result reporting and failure attachments |
| `pytest-html` | Self-contained HTML test report |
| GitHub Actions | Continuous integration and scheduled regression runs |

## Prerequisites

Install the following before running tests:

1. **Git**
2. **Python 3.14 or later**. The project declares this minimum version in `pyproject.toml`.
3. **uv**:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   See the [uv installation guide](https://docs.astral.sh/uv/getting-started/installation/) for Windows and alternative installation methods.

4. **Google Chrome** for Chrome test runs. Install the current stable release from [google.com/chrome](https://www.google.com/chrome/).
5. **Allure CLI** to generate and open Allure reports. Install it with a platform package manager, for example:

   ```bash
   # macOS
   brew install allure

   # Windows (Chocolatey)
   choco install allure

   # Linux (Homebrew)
   brew install allure
   ```

   Verify the installation with `allure --version`.

Selenium Manager automatically obtains a compatible WebDriver when needed, so manually downloading ChromeDriver is normally unnecessary. Ensure the installed browser can reach `https://www.amazon.com`.

## Setup

Clone the repository and install the locked dependencies:

```bash
git clone https://github.com/nadiaalexqa/seleniumPythonPOM.git
cd seleniumPythonPOM
uv sync
```

Run every command below through `uv run` so it uses the project's managed Python environment.

## Running tests

### Chrome with a visible browser

```bash
uv run pytest --browser=chrome
```

### Headless Chrome

Use this option for non-interactive environments and CI:

```bash
uv run pytest --browser=chrome --headless
```

The test fixture sets the Chrome window size to `1920x1080` in both modes. It uses Chrome's modern `--headless=new` mode when `--headless` is supplied.

### Targeted suites and alternatives

```bash
# Fast smoke suite
uv run pytest -m smoketest --browser=chrome --headless

# Full regression suite
uv run pytest -m regressiontest --browser=chrome --headless

# Run the suite in Firefox
uv run pytest --browser=firefox --headless

# Run a single test module
uv run pytest tests/test_search.py --browser=chrome --headless
```

Supported Pytest markers are `smoketest` and `regressiontest`. Invalid browser values fail explicitly; use `chrome` or `firefox`.

## Test reports

Each test run writes raw Allure results to `allure-results/` and a self-contained Pytest HTML report to `reports/report.html`. These generated directories are excluded from version control.

After a run, generate and open the Allure report:

```bash
allure serve allure-results
```

For a persistent static report instead:

```bash
allure generate allure-results --clean -o allure-report
```

On a test failure, the suite attaches a browser screenshot to the Allure results. Chrome browser-console logs are also attached when available.

## GitHub Actions

The [QA Pipeline](.github/workflows/qa.yml) runs on Ubuntu using a Chrome/Firefox matrix. Each browser executes the smoke suite and regression suite in headless mode.

| Trigger | When it runs |
| --- | --- |
| Push | Every push to `main` or `master` |
| Pull request | Pull requests targeting `main` or `master` |
| Schedule | Daily at `02:00 UTC` (`0 2 * * *`) |
| Manual | On demand through `workflow_dispatch` |

To run the workflow from the GitHub web UI:

1. Open the repository's **Actions** tab.
2. Select **QA Pipeline**.
3. Click **Run workflow**, choose the branch, then click **Run workflow**.

To trigger it with the GitHub CLI, authenticate with `gh auth login` and run:

```bash
gh workflow run "QA Pipeline" --ref main
```

Open the workflow run in **Actions** to inspect job logs. The pipeline retains browser-specific `allure-results` and Pytest HTML-report artifacts for 14 days, including artifacts from failed runs.

## Project layout

```text
pages/                  Page Objects and reusable browser interactions
tests/                  Pytest tests and shared WebDriver fixture
.github/workflows/      GitHub Actions QA pipeline
pyproject.toml          Project dependencies and Pytest configuration
uv.lock                 Locked dependency versions
```

## Contribution practices

Keep locators and browser actions in Page Objects, add assertions to tests, and mark each new test with the applicable `smoketest` or `regressiontest` marker. Before opening a pull request, run the relevant headless command locally and inspect generated reports when failures occur.
