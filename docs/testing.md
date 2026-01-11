# Testing

Open-AutoTools uses pytest for unit and integration testing with coverage reporting.

## Test Structure

Tests are organized in `tests/` directories within each module. Unit tests are named `test_*_core.py` and integration tests are named `test_*_integration.py`.

## Configuration

Test configuration is defined in `pytest.ini` and coverage settings in `.coveragerc`. Test dependencies are specified in `setup.py` under the `test` extra.

## Running Tests

Use the `autotools test` command to run the test suite. This automatically installs required test dependencies if missing.

Options include running only unit tests, only integration tests, testing specific modules, generating HTML coverage reports, or disabling coverage entirely.

**Note:** When running tests, performance metrics are automatically collected and displayed at the end, showing execution time, memory usage, and other performance indicators.

## Test Dependencies

Test dependencies include pytest, pytest-cov, pytest-sugar, pytest-xdist, and pytest-timeout. Install them via `pip install -e ".[test]"` or they will be automatically installed when running `autotools test`.

## Coverage

The project maintains **100% code coverage** for all modules. Coverage reports exclude test files, virtual environments, and setup files. HTML reports are generated in `htmlcov/` and XML reports in `coverage.xml`.

### Coverage Metrics

-   **Statements**: 100% coverage
-   **Branches**: 100% coverage
-   **Overall**: 100% coverage

All code paths, including edge cases and error handling, are thoroughly tested to ensure reliability and maintainability.
