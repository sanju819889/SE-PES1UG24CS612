\# Lab 5: Static Code Analysis — Issues and Fixes



\## Project: IT Helpdesk Ticket Allocator



The original Python program was analyzed using Pylint, Bandit, and Flake8. The following issues were identified and addressed.



| Issue | Type | Original Line(s) | Description | Fix Approach |

|---|---|---:|---|---|

| Unsafe subprocess execution | Security — High | 38 | `shell=True` allowed shell command injection through hostname input. | Used an argument list and disabled shell execution. |

| Hardcoded administrator password | Security | 8 | The administrator password was stored directly in the source code. | Read the password from the `HELPDESK\_ADMIN\_PASSWORD` environment variable. |

| Broad exception handling | Security / Quality | 23–24 | A bare `except` silently ignored every exception. | Raised a clear error when the requested ticket does not exist. |

| Mutable default argument | Bug | 10 | The default `audit\_trail=\[]` could share state between calls. | Used `None` and initialized a new list when needed. |

| Invalid urgency accepted | Bug | 49 | Negative urgency values such as `-7` were accepted. | Validated that urgency is an integer between 1 and 5. |

| Unsafe file handling | Quality | 41–43 | The file was opened without an encoding and was not managed using a context manager. | Used `with open(..., encoding="utf-8")`. |

| Missing documentation | Code quality | Multiple | Functions and the module lacked docstrings. | Added explanatory docstrings. |

| Incorrect naming and formatting | Style | Multiple | Naming conventions, blank lines, long lines and other style issues violated coding standards. | Improved naming, formatting and function structure. |

| Unused variable | Code quality | 47 | The variable `t2` was assigned but never used. | Removed the unused assignment. |



\## Verification Results



\- \*\*Pylint:\*\* Improved from 5.53/10 to 9.70/10.

\- \*\*Bandit:\*\* The original high-severity `shell=True` finding was eliminated. Three low-severity warnings remained in the observed final run.

\- \*\*Flake8:\*\* No violations were reported in the observed final run.



The final analysis reports should be retained as evidence of these results.



