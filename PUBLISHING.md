# Publishing Polvon to PyPI

This guide explains how to publish the Polvon package to PyPI (Python Package Index).

## Overview

Polvon uses GitHub Actions for automated publishing to PyPI with trusted publishing (no API tokens required).

## Prerequisites

### 1. Configure Trusted Publishing on PyPI

Before you can publish, you need to set up trusted publishing on PyPI:

1. **Create a PyPI account** (if you don't have one):
   - Go to https://pypi.org/account/register/
   - Complete the registration process

2. **Configure Trusted Publishing**:
   - Go to https://pypi.org/manage/account/publishing/
   - Click "Add a new pending publisher"
   - Fill in:
     - **PyPI Project Name**: `polvon`
     - **Owner**: `thesayfulla`
     - **Repository name**: `polvon`
     - **Workflow name**: `publish-to-pypi.yml`
     - **Environment name**: (leave empty)
   - Click "Add"

3. **For TestPyPI** (optional, for testing):
   - Go to https://test.pypi.org/manage/account/publishing/
   - Repeat the same process as above

### 2. Verify Package Configuration

Before publishing, ensure:
- Version number in `pyproject.toml` and `polvon/__init__.py` are updated
- `README.md` is up to date
- `LICENSE` file exists
- All tests pass

## Publishing Methods

### Method 1: Automatic Publishing via GitHub Release (Recommended)

This is the easiest method and is triggered automatically when you create a release:

1. **Update version number**:
   ```bash
   # Edit pyproject.toml and polvon/__init__.py
   # Change version = "0.1.0" to your new version
   ```

2. **Commit and push changes**:
   ```bash
   git add pyproject.toml polvon/__init__.py
   git commit -m "Bump version to X.Y.Z"
   git push
   ```

3. **Create a GitHub Release**:
   - Go to https://github.com/thesayfulla/polvon/releases/new
   - Create a new tag (e.g., `v0.1.0`)
   - Enter release title and description
   - Click "Publish release"

4. **Monitor the workflow**:
   - The workflow will automatically build and publish to PyPI
   - Check progress at https://github.com/thesayfulla/polvon/actions

### Method 2: Manual Publishing via Workflow Dispatch

For testing or manual control:

1. **Go to GitHub Actions**:
   - Navigate to https://github.com/thesayfulla/polvon/actions
   - Select "Publish to PyPI" workflow

2. **Run workflow**:
   - Click "Run workflow"
   - Choose environment:
     - **testpypi**: For testing (publishes to test.pypi.org)
     - **pypi**: For production release
   - Click "Run workflow"

### Method 3: Local Publishing (Manual)

For manual publishing from your local machine:

1. **Install dependencies**:
   ```bash
   pip install build twine
   ```

2. **Build the package**:
   ```bash
   python -m build
   ```

3. **Verify the build**:
   ```bash
   twine check dist/*
   ```

4. **Publish to TestPyPI** (for testing):
   ```bash
   twine upload --repository testpypi dist/*
   ```

5. **Publish to PyPI** (production):
   ```bash
   twine upload dist/*
   ```

   Note: This method requires PyPI API tokens configured in `~/.pypirc`

## Testing the Published Package

After publishing, verify the package:

### From PyPI:
```bash
pip install polvon
polvon --version
```

### From TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ polvon
polvon --version
```

## Version Management

### Semantic Versioning

Polvon follows [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., 0.1.0)
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Updating Version

Update version in **both** files:

1. `pyproject.toml`:
   ```toml
   version = "X.Y.Z"
   ```

2. `polvon/__init__.py`:
   ```python
   __version__ = "X.Y.Z"
   ```

## Troubleshooting

### "Project name already exists"
- The package name is already taken on PyPI
- Choose a different name or contact the current owner

### "Trusted publishing not configured"
- Follow the "Configure Trusted Publishing" steps above
- Ensure the repository and workflow names match exactly

### "Build failed"
- Check the GitHub Actions logs
- Verify all tests pass locally
- Ensure `pyproject.toml` is valid

### "Twine check warnings"
- Some warnings from newer setuptools are false positives
- The package will still work if it installs correctly locally

## Additional Resources

- [PyPI Package Publishing](https://packaging.python.org/tutorials/packaging-projects/)
- [Trusted Publishing Guide](https://docs.pypi.org/trusted-publishers/)
- [Semantic Versioning](https://semver.org/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
