# Issues Found by Static Analysis

Tools used: Bandit (security), Pylint (code quality), Flake8 (style).

Reports: see `reports/before/` and `reports/after/`.

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| SQL injection (B608) | Security (Medium) | 23, 26 | SQL query is built by joining strings with user input, so input like `x' OR '1'='1` returns all customers | Use parameterized queries with `?` placeholders |
| Weak hash SHA1 (B324) | Security (High) | 48 | SHA1 is a broken hash algorithm and unsuitable for sensitive data | Replace with `hashlib.sha256` |
| Use of exec() (B102 / W0122) | Security (Medium) | 53 | `exec` runs arbitrary code typed by staff, allowing arbitrary execution | Remove `exec`; take a percentage discount number instead |
| Insecure temp file mktemp (B306) | Security (Medium) | 63 | `tempfile.mktemp` is vulnerable to race conditions | Use `tempfile.NamedTemporaryFile` |
| Permissive file permissions 0o777 (B103) | Security (High) | 67 | Receipt file is writable by everyone | Use `0o600` (owner read/write only) |
| Hardcoded password (B105 / B107) | Security (Low) | 70, 71 | Admin password is in source code and used as a default argument | Read password from `ADMIN_PASSWORD` env var and use `hmac.compare_digest` |
| Use of assert (B101) | Security (Low) | 30 | `assert` is removed when Python runs with `-O`, so the check can vanish | Replace with `if` check and `raise ValueError` |
| try/except/pass (B110) | Security (Low) | 41 | Errors are silently swallowed | Remove bare pass, validate plate, and raise `KeyError` |
| Weak random (B311) | Security (Low) | 45 | `random` is predictable, so booking codes can be guessed | Use the `secrets` module (`secrets.randbelow`) |
| Mutable default argument (W0102) | Bug | 16 | `features=[]` is shared across all calls | Default to `None`, then create a new list inside the function |
| Bare except (W0702 / E722) | Bug | 41 | Catches every error including ones that should not be hidden | Validate plate explicitly and raise `KeyError` |
| Unused import (W0611 / F401) | Quality | 2 | `json` is imported but never used | Remove the unused import |
| Naming style (C0103) | Style | 16, 22, 25, 29, 36, 44, 47, 50, 56, 62, 70, 75 | Functions use camelCase and globals are lowercase | Rename functions to snake_case and globals to UPPER_CASE |
| Missing docstrings (C0114 / C0116) | Quality | 1, 16, 22, 25, 29, 36, 44, 47, 50, 56, 62, 70, 75, 82 | No documentation for the module or functions | Add descriptive docstrings to module and every function |
| Comparison to True (C0121 / E712) | Style | 78 | `== True` is unnecessary | Use direct truthiness check `if car["available"]:` |
| File opened without `with` / encoding (R1732 / W1514) | Quality | 64 | File resource leak and missing explicit encoding | Use `with` statement and specify `encoding="utf-8"` |
| String formatting could be f-string (C0209) | Quality | 23, 65 | Old `%` style formatting used | Modernize to f-strings |
| Simplifiable if statement / unnecessary else (R1703 / R1705) | Quality | 57 | Verbose if-return pattern | Replace with `return bool(re.match(...))` |
| Consider iterating with .items() (C0206) | Quality | 77 | Iterating over keys and indexing back into dict | Use `for plate, car in FLEET.items():` |
| Inconsistent return statements (R1710) | Quality | 16, 36 | Function returns a value in some paths but None in others | Always return a consistent value (e.g. 0 km charge) |
| Line too long (C0301 / E501) | Style | 19, 23, 31, 33, 65, 88, 89, 90 | Lines exceed standard length limits | Wrap and break expressions across lines to stay <= 79 characters |
| Expected blank lines (E302 / E305) | Style | 16, 22, 25, 29, 36, 44, 47, 50, 56, 62, 70, 75, 82, 101 | Expected 2 blank lines between top-level functions | Add standard PEP 8 spacing |
| Negative rental days (logic bug) | Bug (not flagged by tools) | 29-35 | End date before start date gives a negative rental cost | Validate `end_dt > start_dt` and raise `ValueError` |
| Double booking (logic bug) | Bug (not flagged by tools) | 29-35 | A car can be booked again while already rented | Check `car["available"]`, reject with `ValueError`, and mark `False` on rent |
| Negative daily rate (logic bug) | Bug (not flagged by tools) | 16-20 | A car can be added with a negative daily rate | Reject rates below 0 with `ValueError` |
| Unknown car plate return (logic bug) | Bug (not flagged by tools) | 36-43 | Returning an unknown car silently does nothing | Check plate existence in fleet and raise `KeyError` |

## Status after fixes
- SQL injection (B608): Fixed in Commit 1 ("Fix Bandit security issues")
- Weak hash SHA1 (B324): Fixed in Commit 1 ("Fix Bandit security issues")
- Use of exec() (B102 / W0122): Fixed in Commit 1 ("Fix Bandit security issues")
- Insecure temp file mktemp (B306): Fixed in Commit 1 ("Fix Bandit security issues")
- Permissive file permissions 0o777 (B103): Fixed in Commit 1 ("Fix Bandit security issues")
- Hardcoded password (B105 / B107): Fixed in Commit 1 ("Fix Bandit security issues")
- Use of assert (B101): Fixed in Commit 1 ("Fix Bandit security issues")
- try/except/pass (B110): Fixed in Commit 1 ("Fix Bandit security issues")
- Weak random (B311): Fixed in Commit 1 ("Fix Bandit security issues")
- Mutable default argument (W0102): Fixed in Commit 2 ("Fix Pylint issues")
- Bare except (W0702 / E722): Fixed in Commit 2 ("Fix Pylint issues")
- Unused import (W0611 / F401): Fixed in Commit 2 ("Fix Pylint issues")
- Naming style (C0103): Fixed in Commit 2 ("Fix Pylint issues")
- Missing docstrings (C0114 / C0116): Fixed in Commit 2 ("Fix Pylint issues")
- Comparison to True (C0121 / E712): Fixed in Commit 2 ("Fix Pylint issues")
- File opened without `with` / encoding (R1732 / W1514): Fixed in Commit 2 ("Fix Pylint issues")
- String formatting could be f-string (C0209): Fixed in Commit 2 ("Fix Pylint issues")
- Simplifiable if statement / unnecessary else (R1703 / R1705): Fixed in Commit 2 ("Fix Pylint issues")
- Consider iterating with .items() (C0206): Fixed in Commit 2 ("Fix Pylint issues")
- Inconsistent return statements (R1710): Fixed in Commit 2 ("Fix Pylint issues")
- Line too long (C0301 / E501): Fixed in Commit 3 ("Fix Flake8 style issues")
- Expected blank lines (E302 / E305): Fixed in Commit 3 ("Fix Flake8 style issues")
- Negative rental days (logic bug): Fixed in Commit 2 ("Fix Pylint issues")
- Double booking (logic bug): Fixed in Commit 2 ("Fix Pylint issues")
- Negative daily rate (logic bug): Fixed in Commit 2 ("Fix Pylint issues")
- Unknown car plate return (logic bug): Fixed in Commit 2 ("Fix Pylint issues")

### Final Tool Results
- **Bandit**: No issues identified (0 issues, clean)
- **Pylint Score**: 10.00/10 (rated at 10.00/10)
- **Flake8**: Clean (0 issues, empty output)
