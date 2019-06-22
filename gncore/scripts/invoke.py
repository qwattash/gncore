# Copyright (c) 2019 Alfredo Mazzinghi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Invoke program")
    parser.add_argument("--stdout",
                        help="Redirect stdout to the given file")
    parser.add_argument("--pipe", nargs="+", action="append", default=[],
                        help="Pipe the command to the next. %OPT% sequences are replaced by '-'.")
    parser.add_argument("command", nargs="+",
                        help="The main command to run. %OPT% sequences are replaced by '-'.")
    args = parser.parse_args()

    commands = [args.command] + args.pipe

    if args.stdout:
        out = open(args.stdout, "w+")
    else:
        out = None
    
    procs = []
    piped = None
    for idx, command in enumerate(commands):
        command = map(lambda c: c.replace("%OPT%", "-"), command)

        if idx == len(commands) - 1:
            stdout = out
        else:
            stdout = subprocess.PIPE
        proc = subprocess.Popen(command, stdin=piped, stdout=stdout)
        procs.append(proc)
        piped = proc.stdout
    proc.wait()

if __name__ == "__main__":
    main()
