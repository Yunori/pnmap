# Pnmap

Pnmap is a script that simplifies the use of nmap.

### Dependencies

> python3
> nmap


###Usage
```
python3 pnmap.py [-h] [--options OPTIONS] [--targets TARGETS]
```
options : nmap options, please see https://nmap.org/book/man-briefoptions.html for more details. Please note than some options will requires you to have root priviledges.
> Ex: --options "-sV -6"

targets: targets  specification, IPv4/v6 address, CIDR. Do not forget to use the "-6" option to scan IPv6 addresses.
> Ex: --targets 192.168.0.0/24

There are 3 types of targets:
- Random IP, with the "-iR [num]" option (within the "--options" argument)
- File containing targets, with the "-iL [filename]" option (within the "--options" argument)
- Address(es), in the "--targets" argument

You need to specify at least one type of target.

###Nmap scripts, and vulnerability scanning
To use nmap scripts, you need to specify the "--script" option in the "--options" argument.
There is a list of default scripts included with nmap at https://nmap.org/nsedoc/index.html.
```
python3 pnmap.py -opt "-sV --script=banner" -t 127.0.0.1
```
If you want to do vulnerability scans, I advise you to use:
- vulscan https://github.com/scipag/vulscanet
- nmap-vulners https://github.com/vulnersCom/nmap-vulners

```
python3 pnmap.py -opt "-sV --script=vulners/vulners" -t 127.0.0.1
python3 pnmap.py -opt "-sV --script=vulscan/vulscan" -t 127.0.0.1
```

###Scan report
At the end of the scan, pnmap will automaticaly generate a report.
You can open it with your browser. Chrome might block the file, I advise you to read it with Firefox. See [link](https://stackoverflow.com/questions/3828898/can-chrome-be-made-to-perform-an-xsl-transform-on-a-local-file).

![](https://raw.githubusercontent.com/Yunori/pnmap/main/ReportScreenshot.png)

