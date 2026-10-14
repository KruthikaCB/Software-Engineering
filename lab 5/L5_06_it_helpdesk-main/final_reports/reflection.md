# Lab 5: Static Code Analysis — Reflection

**Student:** Kruthika C B  
**SRN:** PES1UG24CS670  
**Course:** B.Tech CSE  
**Repository:** [L5_06_it_helpdesk](https://github.com/KruthikaCB/L5_06_it_helpdesk)

## 1. What is static code analysis, and why is it important?

Static code analysis is the process of examining source code without executing the program. It helps identify potential bugs, security vulnerabilities, code-quality problems, and style violations. Finding these issues early makes software more reliable, secure, readable, and maintainable.

## 2. What is the difference between Pylint, Bandit, and Flake8?

The three tools focus on different aspects of Python code:

- **Pylint:** Checks code quality, naming conventions, documentation, and other programming practices. It also provides a code-quality score.
- **Bandit:** Identifies potentially insecure coding patterns and security-related issues.
- **Flake8:** Checks Python style and formatting, including violations of PEP 8 conventions.

Using all three tools provides a broader assessment than relying on only one tool.

## 3. What issues did you identify and fix?

The original `helpdesk_system.py` contained several issues, including a hardcoded administrator password, unsafe shell-command execution, a mutable default argument, insufficient urgency validation, naming and documentation problems, and file-handling improvements that were needed.

I moved the administrator password configuration to an environment variable, removed the unused ping functionality, changed the mutable default argument to `None`, added urgency validation, improved naming and documentation, and used a context manager for file handling. I also corrected the reported style violations.

## 4. How did you verify that the fixes worked?

I reran Pylint, Bandit, and Flake8 after modifying the program and preserved the before-and-after reports in the repository.

The recorded results were:

- Pylint improved from **5.53/10 to 10.00/10**.
- Bandit reported **no issues** in the final scan.
- Flake8 produced no output, with an exit code of **0**, indicating no reported violations.

These results provided evidence that the updated program satisfied the checks performed by the three tools.

## 5. What did you learn from this lab?

I learned that different static analysis tools identify different categories of problems. Security issues, code-quality problems, and style violations all matter, but they require different types of fixes.

I also learned the importance of reviewing tool findings, making targeted changes, and rerunning the tools to verify the results. Keeping the original and final reports makes the improvement measurable and provides evidence of the work performed.

## 6. How does static analysis improve maintainability and security?

Static analysis helps developers identify risky patterns before they become larger problems. For example, moving secrets out of source code reduces the risk of exposing credentials, while validating inputs helps prevent invalid data from entering the program. Consistent naming, documentation, and file handling make the code easier to understand and maintain.

Static analysis does not guarantee that a program is completely secure or free of bugs, but it is a useful part of a broader software-quality process.

## Conclusion

This lab provided practical experience using Pylint, Bandit, and Flake8 to analyze and improve a Python program. The updated code achieved a Pylint score of 10.00/10, had no issues identified by the final Bandit scan, and had no reported Flake8 violations. The preserved reports and Git commits provide evidence of the changes and verification.