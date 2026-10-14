# Lab 5: Static Code Analysis — Issues Identified and Fixed

**Student:** Kruthika C B  
**SRN:** PES1UG24CS670  
**Course:** B.Tech CSE  
**Repository:** [L5_06_it_helpdesk](https://github.com/KruthikaCB/L5_06_it_helpdesk)  
**File analyzed:** `helpdesk_system.py`

## Objective

The objective of this activity was to identify and fix issues in the assigned Python program using Pylint, Bandit, and Flake8. The issues were documented, fixes were applied, and the tools were rerun to verify the improvements.

## Issue Table

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Hardcoded administrator password | Security | Verify in original file | The administrator password was directly written in the source code. Anyone with access to the source could discover it. | Replaced the hardcoded password with an environment variable, `HELPDESK_ADMIN_PASSWORD`, so the secret is configured outside the source code. |
| Unsafe shell command execution | Security | Verify in original file | The program constructed a shell command using a hostname. Shell-based command execution can introduce command-injection risks when input is not handled safely. | Removed the unused ping functionality and the associated `subprocess` import because the functionality was not needed in the updated program. |
| Mutable default argument | Reliability / Bug | Verify in original file | A list used as a default argument could be shared between function calls, causing unintended data to persist. | Changed the default to `None` and initialized a new list inside the function when no audit trail is supplied. |
| Missing urgency validation | Input validation | Verify in original file | Ticket urgency was not adequately restricted to the expected range, allowing invalid values such as negative urgency. | Added validation to accept only integer urgency values from 1 to 5 and raise `ValueError` for invalid input. |
| Overly broad exception handling | Reliability | Verify in original file | A broad exception handler can hide the specific cause of an error and make debugging difficult. | Replaced broad exception handling with more appropriate error handling where required. |
| Inconsistent naming and missing documentation | Code quality / Maintainability | Verify in original file | Non-standard naming and missing docstrings made functions harder to understand and maintain. | Renamed `unresolvedHighPriority` to `unresolved_high_priority` and added docstrings to the relevant functions. |
| Unsafe file-handling pattern | Reliability / Maintainability | Verify in original file | Manually opening and closing a file can leave it open if an error occurs before the close operation. | Used a `with open(..., encoding="utf-8")` context manager when writing the ticket data to JSON. |
| PEP 8 style violations | Style | Multiple lines; verify original report | Flake8 reported formatting and style violations in the original program. | Reformatted the code and reran Flake8 to verify that no violations were reported. |

## Verification Results

The static analysis tools were rerun after the fixes.

| Tool | Before | After |
|---|---|---|
| Pylint | 5.53/10 | 10.00/10 |
| Bandit | 1 high-severity and 3 low-severity findings | No issues identified |
| Flake8 | 14 reported violations | No output; exit code 0 |

The before-and-after reports are preserved in the repository:

- `pylint_before.txt`
- `pylint_after.txt`
- `bandit_before.txt`
- `bandit_after.txt`
- `flake8_before.txt`
- `flake8_after.txt`

These results show that the final code passed the recorded checks from all three tools. The line numbers in this table should be filled in or checked against the original source and reports before submission.