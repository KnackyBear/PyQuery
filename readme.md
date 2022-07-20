# PyQuery

A simple multi HTTP Request based on CSV file.

## Pre-requisites

```
pip install -r requirement.txt
```

## How to use

```
python query.py --csv=/path/to/csv --request="your_formatted_request" --no-header --verbose --method=GET
```

| Parameter | Description |
| --- | --- |
| ``--csv`` ``-c`` | Path to the CSV file. This file is use during the formatting process. See below for more details.|
| ``--request`` ``-r`` | Your HTTP request, formatted with your variable (ie {0} {1} ... or ... {var1} {var2} ...). See below for more details about how to format your request. |
| ``--no-header`` | Specify that your CSV file have no header. |
| ``--verbose`` | Add response content to the ouput (default, only status code) |
| ``--method`` | Choose the method of your http request. Only GET, POST, PUT, DELETE and HEAD are accepted. Default is GET. |

## How to format the HTTP request.

### With no-header option

The CSV does not contains any header (first line in the file).
Each row is used to generate a new HTTP request.

You have to use ``{0}`` ``{1}`` ``{2}``... in your request to attach variable from CSV  (the number relates to column in file)

_Example :_

```
https://www.google.com/search?q={0}
```

With the CSV :

|     |
| --- |
| moo |
| foo |
| doo |

will generate the following requests :

| Result |
| --- |
| https://www.google.com/search?q=moo |
| https://www.google.com/search?q=foo |
| https://www.google.com/search?q=doo |

*Warning :* You can have more column in your CSV than number of variables in your request. *Reverse is not possible !*

### Without no-header option

The CSV contains header row (first line of the file).
The first row is used to check consistency between CSV and the formatted request. You must have the same number of variables and name.

You have to use ``{header1}`` ``{header2}`` ``{header3}``... in your request to attach variable from CSV  (the name of the variable relates to each headers in the file)

_Example :_

```
https://www.google.com/search?q={header1}
```

With the CSV :

| header1 |
| --- |
| moo |
| foo |
| doo |

will generate the following requests :

| Result |
| --- |
| https://www.google.com/search?q=moo |
| https://www.google.com/search?q=foo |
| https://www.google.com/search?q=doo |
