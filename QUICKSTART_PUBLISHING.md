# Quick Start: Publishing to PyPI

## First Time Setup (One-Time)

1. **Go to PyPI**: https://pypi.org/manage/account/publishing/
2. **Add Pending Publisher** with these exact values:
   - PyPI Project Name: `polvon`
   - Owner: `thesayfulla`
   - Repository: `polvon`
   - Workflow: `publish-to-pypi.yml`
   - Environment: (leave empty)

## Publishing a New Version

### Quick Method (Recommended)

1. **Update version** in both files:
   - `pyproject.toml`: `version = "X.Y.Z"`
   - `polvon/__init__.py`: `__version__ = "X.Y.Z"`

2. **Commit and push**:
   ```bash
   git add pyproject.toml polvon/__init__.py
   git commit -m "Bump version to X.Y.Z"
   git push
   ```

3. **Create GitHub Release**:
   - Go to: https://github.com/thesayfulla/polvon/releases/new
   - Tag: `vX.Y.Z` (e.g., `v0.1.1`)
   - Title: `Release X.Y.Z`
   - Description: List changes
   - Click "Publish release"

4. **Done!** Package automatically publishes to PyPI.

### Manual Method (For Testing)

1. **Go to Actions**: https://github.com/thesayfulla/polvon/actions
2. **Select** "Publish to PyPI" workflow
3. **Click** "Run workflow"
4. **Choose**:
   - `testpypi` for testing
   - `pypi` for production
5. **Click** "Run workflow"

## Verify Installation

```bash
pip install polvon
polvon --version
```

For detailed instructions, see [PUBLISHING.md](PUBLISHING.md).
