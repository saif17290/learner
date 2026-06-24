# learner
Beginner-friendly Python ETL example project.

Run steps (PowerShell):

1. Create a virtual environment

```powershell
python -m venv .venv
```

2. Activate the virtual environment

```powershell
. .\.venv\Scripts\Activate.ps1
```

3. Install dependencies

```powershell
pip install -r requirements.txt
```

4. Run the ETL script

```powershell
python -m src.etl
```

5. Run tests

```powershell
pytest
```

Files and folders created by the scaffold:
- `src/` - package with `etl.py` and `__init__.py`
- `tests/` - pytest tests
- `data/raw/`, `data/processed/` - data folders
- `db/`, `docs/` - placeholders for database and docs
- `.gitignore`, `requirements.txt`

