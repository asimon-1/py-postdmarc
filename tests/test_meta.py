"""Test the non-functional aspects of the source code."""
import unittest
import subprocess

MAX_LINE_LENGTH = 88


class BaseTest(unittest.TestCase):
    """Provide base test case class."""

    def setUp(self):
        """Call before initiation of each test."""
        pass

    def tearDown(self):
        """Call after each test completion."""
        pass

    def run_module(self, module, *args):
        """Call the specified module, passing through any arguments."""
        module = [str(module)]
        args = [str(arg) for arg in args]

        cmd = ["python", "-m"] + module + args

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=False,
            shell=False,
        )

        out, err = process.communicate()
        if process.returncode != 0:
            msgs = []
            if err:
                err_decoded = err.decode().rstrip()
                msgs.append(
                    f"{module} exited (code {process.returncode}) and has "
                    f"unexpected output on stderr:\n{err_decoded}"
                )
            if out:
                out_decoded = out.decode().rstrip()
                msgs.append(f"{module} found issues:\n{out_decoded}")
            if not msgs:
                msgs.append(
                    f"{module} exited (code {process.returncode}) and has "
                    f"no output on stdout or stderr."
                )
            self.fail("\n".join(msgs))


class TestStyle(BaseTest):
    """Ensure adherence to code style standards."""

    def test_pep8(self):
        """Ensure adherance to PEP8 code style standards.

        Ignored Error Codes:
        E501 : Line too long (covered by other test)
        W503 : Line break occurred before a binary operator (incompatible with Black)
        E800 : Found commented out code (covered by other test)
        F403 : 'from module import *' used (covered by other test)
        """
        self.run_module("flake8", "--select=E,W,F", "--ignore=E501,W503,E800,F403")

    def test_line_length(self):
        """Ensure that all lines of code have length <= MAX_LINE_LENGTH.

        Selected Error Codes:
        E501 : Line too long
        """
        self.run_module(
            "flake8", "--select=E501", f"--max-line-length={MAX_LINE_LENGTH}"
        )

    def test_formatting(self):
        """Ensure that code formatting matches the Black rules."""
        self.run_module("black", ".", "--check", "--line-length", MAX_LINE_LENGTH)

    def test_docstrings(self):
        """Ensure that docstrings meet PEP257 standards.

        Selected Error Codes:
        D100 : Missing docstring in public module
        D101 : Missing docstring in public class
        D102 : Missing docstring in public method
        D103 : Missing docstring in public function
        D104 : Missing docstring in public package
        D105 : Missing docstring in magic method
        D106 : Missing docstring in public nested class
        D107 : Missing docstring in __init__
        D300 : Use triple double quotes
        D301 : Use r" if any backslashes in a docstring
        """
        self.run_module(
            "pydocstyle",
            "--match-dir=^((?!tests).)*$",
            "--select=D100,D101,D102,D103,D104,D105,D106,D107,D300,D301",
        )

    def test_dead_code(self):
        """Check for code that is not used.

        Selected Error Codes:
        F401 : Module imported but unused
        E800 : Found commented out code
        """
        self.run_module("flake8", "--select=F401,E800")


class TestSecurity(BaseTest):
    """Test for security-related requirements."""

    def test_wildcard_import(self):
        """Check for wildcard imports like "from module import *".

        Selected Error Codes:
        F403 : from module import *
        """
        self.run_module("flake8", "--select=F403")

    def test_safe_load(self):
        """Check that YAML and Pickle objects are loaded safely.

        Selected Error Codes:
        B301 : pickle
        B506 : yaml_load
        """
        self.run_module("bandit", ".", "-r", "--tests=B301,B506")

    def test_no_unsafe_execution(self):
        """Check that no unsafe methods of code execution are used.

        Selected Error Codes:
        B102 : exec_used
        B307 : eval
        B322 : input (Python 2)
        B601 : paramiko_calls
        B602 : subprocess_popen_with_shell_equals_true
        B603 : subprocess_without_shell_equals_true
        B604 : any_other_function_with_shell_equals_true
        B605 : start_process_with_a_shell
        B606 : start_process_with_no_shell
        B607 : start_process_with_partial_path
        B608 : hardcoded_sql_expressions
        """
        self.run_module(
            "bandit",
            ".",
            "-r",
            "-ll",
            "--tests=B102,B307,B322,B601,B602,B603,B604,B605,B606,B607,B608",
        )
