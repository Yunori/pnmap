#!/usr/bin/python3

import argparse
import asyncio
import re


async def _read_stream(stream, cb):
    """
        Wait for an event on stdout/stderr, read the line, and send it to our lambda functions
    """

    while True:
        line = await stream.readline()
        if line:
            cb(line.strip().decode())
        else:
            break


async def _stream_subprocess(cmd, stdout_cb, stderr_cb):
    """
        Launch an nmap process with asyncio, redirect stdout/stderr to PIPE, and read them asynchronously
    """
    process = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)

    await asyncio.wait([
        _read_stream(process.stdout, stdout_cb),
        _read_stream(process.stderr, stderr_cb),
    ])
    return await process.wait()


def execute(cmd, stdout_cb, stderr_cb):
    """
        Execution of a loop that will read the events till the process dies
    """
    loop = asyncio.get_event_loop()
    rc = loop.run_until_complete(
        _stream_subprocess(
            cmd,
            stdout_cb,
            stderr_cb
        ))
    loop.close()
    return rc


def main():
    """
        Argument parsing
    """
    parser = argparse.ArgumentParser("Python Nmap Launcher")

    parser.add_argument("--options", "-opt",
                        default="",
                        help="nmap arguments")
    parser.add_argument("--targets", "-t",
                        default="",
                        help="targets specification")

    args = parser.parse_args()
    targets = args.targets

    """
        Look for targets in the "options argument, if the "targets" argument is empty
    """
    if args.targets == "":
        regex = r"-i[L|R]\s(\S+)"
        matches = re.search(regex, args.options)
        if matches is None:
            parser.error(
                'You need to specify at least one target, with the -t or -opt "-iL [filename]" or' +
                '-opt "-iR [numbers of IP]" argument\n' +
                '[EXAMPLES]\npnmap.py -t 192.168.0.0/24\npnmap.py -opt "-iL targets.txt"\npnmap.py -opt "-iR 100"')

    """
        Execution of nmap with the following arguments:
        -v 1 -> Verbose level 1, displays detailed information about timing, flags, protocol details, etc 
        --stats-every 2 -> shows scanning status every 2 seconds
        -oX scan.xml -> export the scan results to scan.xml
        --stylesheet https://..... -> use nmap-bootstrap as a template for the report
        args.options -> nmap arguments
        targets -> target(s) address(es)
        
        lambda functions are used to show the output of the nmap process
    """
    execute(
        'nmap -v 1 --stats-every 2 -oX scan.xml --stylesheet ' +
        'https://raw.githubusercontent.com/honze-net/nmap-bootstrap-xsl/master/nmap-bootstrap.xsl ' +
        args.options + ' ' + targets,
        lambda x: print("%s" % x),
        lambda x: print("ERROR: %s" % x))


if __name__ == "__main__":
    main()
