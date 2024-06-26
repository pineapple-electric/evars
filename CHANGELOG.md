# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.3] - 2024-04-30

### Changed

- Moved package metadata from `setup.cfg` to `pypackage.toml`
- Fixed readme link in package metadata

## [0.1.2] - 2024-04-30

### Added

- Added `dev-requirements.txt` to make development easier

### Changed

- Switched from nose2 to pytest for unit tests
- Updated black and mypy and updated source to make them happy
- Made Pylint happier
- Updated pre-commit hooks

## [0.1.1] - 2022-12-24

### Changed

- Switched from nose to nose2 for unit tests
- Made Pylint happy again
- Updated pre-commit hooks
- Fixed the `CHANGELOG.md` sections

## [0.1.0] - 2022-12-24

### Added

- Added a markdown formatter to pre-commit
- Added an FAQ to the README file

### Changed

- Updated pre-commit hooks
- Updated the copyright date

## [0.0.1] - 2021-03-16

### Added

- The `Environment` class and its `source` method to load variables from
  environment files
- Pre-commit hooks for formatting and linting
- Formatting: black
- Linting: bandit, mypy, pylint
- Tests: 100% coverage

[0.0.1]: https://github.com/pineapple-electric/evars/releases/tag/v0.0.1
[0.1.0]: https://github.com/pineapple-electric/evars/releases/tag/v0.1.0
[0.1.1]: https://github.com/pineapple-electric/evars/releases/tag/v0.1.1
[0.1.2]: https://github.com/pineapple-electric/evars/releases/tag/v0.1.2
[0.1.3]: https://github.com/pineapple-electric/evars/releases/tag/v0.1.3
