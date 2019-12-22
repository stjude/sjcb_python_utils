#!/usr/bin/env python3
"""
Utilities for executing external applications

+--------------------------------------------------------------------------+
| Copyright 2019 St. Jude Children's Research Hospital                     |
|                                                                          |
| Licensed under a modified version of the Apache License, Version 2.0     |
| (the "License") for academic research use only; you may not use this     |
| file except in compliance with the License. To inquire about commercial  |
| use, please contact the St. Jude Office of Technology Licensing at       |
| scott.elmer@stjude.org.                                                  |
|                                                                          |
| Unless required by applicable law or agreed to in writing, software      |
| distributed under the License is distributed on an "AS IS" BASIS,        |
| WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. |
| See the License for the specific language governing permissions and      |
| limitations under the License.                                           |
+--------------------------------------------------------------------------+
"""

import io
import shlex
import subprocess

def run_shell_command(command_string, shell=False, stdout=None, stderr=None):
    """ Executes a command and returns stdout, stderr, return_code.
    Args:
        command_string: Command to be executed
        shell (bool): Whether or not to use shell
        stdout (io.TextIOWrapper?): Redirect stdout for subprocess.run
        stderr (io.TextIOWrapper?): Redirect stderr for subprocess.run
    Returns:
        stdout_str (str): stdout of command as a single string.
        stderr_str (str): stderr of command as a single string.
        return_code (int): integer return code of command.
    """

    # Needed for running 'coverage' with buffering on - if we run with
    # buffering then sys.stdout turns into a StringIO class and can't
    # be passed to subprocess.run
    if not isinstance(stdout, io.TextIOWrapper):
        stdout = subprocess.PIPE
    if not isinstance(stderr, io.TextIOWrapper):
        stderr = subprocess.PIPE

    command = shlex.split(command_string)
    if shell:
        command = command_string
    try:
        proc = subprocess.run(command, stdout=stdout, stderr=stderr,
                              shell=shell)
    except FileNotFoundError:
        stdout = ""
        stderr = "Command '%s' not found"%(command[0])
        return_code = 127
        return (stdout, stderr, return_code)

    stdout_str = ""
    stderr_str = ""
    if proc.stdout:
        stdout_str = proc.stdout.decode('utf-8')
    if proc.stderr:
        stderr_str = proc.stderr.decode('utf-8')
    return_code = proc.returncode

    return (stdout_str, stderr_str, return_code)
