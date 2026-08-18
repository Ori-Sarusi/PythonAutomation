# 🚀 Python Playwright Test Automation Framework

An end-to-end (E2E) automated testing framework built with **Python**, **Playwright**, and **pytest**, designed following the **Page Object Model (POM)** and **AAA (Arrange, Act, Assert)** patterns.

---

## 📌 Architecture & Design Principles

* **Page Object Model (POM)**: Decoupled test scenarios from UI locators and interactions for high maintainability.
* **AAA Pattern (Arrange, Act, Assert)**: Clean, standardized, and readable test case structure.
* **Pytest Fixtures**: Modular browser lifecycle management and page object injections.
* **Rich Reporting**: Built-in HTML reports with traces, screenshots, and step-by-step logs.
* **CI/CD Ready**: Configurable for headless cross-browser test execution via GitHub Actions.

---

## 🛠️ Tech Stack

* **Language**: Python 3.10+
* **Automation Library**: [Playwright for Python](https://playwright.dev/python/)
* **Test Runner**: [pytest](https://docs.pytest.org/) & [pytest-playwright](https://github.com/microsoft/pytest-playwright)
* **Reporting**: `pytest-html`
* **Configuration**: `python-dotenv`

---

## 📂 Project Structure

```text
├── config/                # Environment configurations & settings
├── pages/                 # Page Object Model (POM) classes
│   ├── base_page.py       # Core wrapper & shared page methods
│   └── ...                # Application-specific page objects
├── tests/                 # Automated test suites
│   ├── conftest.py        # Global Pytest fixtures & setup
│   └── test_*.py          # Test scenarios (AAA pattern)
├── test_data/             # Test data files (JSON / fixtures)
├── utils/                 # Custom utilities & helpers
├── .gitignore             # Git ignore rules
├── pytest.ini             # Pytest CLI flags and reporting configs
├── requirements.txt       # Project dependencies
└── README.md              # Documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
* Python 3.10 or higher installed.

### 2. Setup Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows (PowerShell):
.\.venv\Scripts\Activate.ps1
# Windows (CMD):
.\.venv\Scripts\activate.bat
# macOS / Linux:
source .venv/bin/activate
```

### 3. Install Dependencies & Browsers

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browser binaries (Chromium, Firefox, WebKit)
playwright install
```

### 4. Running Tests

```bash
# Run all tests (headed mode by default via pytest.ini)
pytest

# Run tests in headless mode
pytest --headless

# Run tests on specific browser
pytest --browser chromium
pytest --browser firefox
pytest --browser webkit
```

---

## 📊 Test Reports

After running the tests, an interactive HTML report will be generated inside the `reports/` folder:
* Open `reports/report.html` in your browser to inspect test execution results, execution times, and screenshots.
