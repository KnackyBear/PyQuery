import sys, getopt
import requests
import csv
import re



class Query:
    def __init__(self):
        self.csv = None
        self.request = None
        self.vars = []
        self.hasHeaders = True

    def _getopt(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hc:r:", ["help", "csv=", "request=", "no-header"])
        except getopt.GetoptError as err:
            print(err)
            self.usage()
            sys.exit(2)

        for o, a in opts:
            if o == "-h":
                usage()
                sys.exit(2)
            elif o in ("-c", "--csv"):
                self.csv = a
            elif o in ("-r", "--request"):
                self.request = a
            elif o == "--no-header":
                self.hasHeaders = False
            else:
                self.usage()
                sys.exit(2)

    def _check(self):
        if self.csv == None or self.csv == '' or self.request == None or self.request == '':
            print("  [!] csv and request are required.")
            self.usage()
            sys.exit(2)
        
        if not self.hasHeaders and not self.request.__contains__("{0}"):
            print("  [!] No variable defined in formatted request !")
            print("Ex:")
            print("       https://duckduckgo.com/?q={0}, where {0} is the variable used in the first column of the csv file.")
            sys.exit(3)

        if self.hasHeaders and not self.request.__contains__("{") and not self.request.__contains__("}"):
            print("  [!] No variable defined in formatted request !")
            print("Ex:")
            print("       https://duckduckgo.com/?q={myheader}, where {myheader} is the variable used in the column of the csv file with the header 'myheader'.")
            sys.exit(3)

    def _get_vars_from_request(self):
        r1 = re.findall(r"{[A-Za-z0-9]+}", self.request)
        r2 = [rex[1:-1] for rex in r1]
        print("  [*] Variables found in request : %s" % r2)
        self.vars = r2

    def usage(self):
        print("Usage : python query.py --csv=/path/to/csv --request=your_formatted_request")

    def execute(self):
        self._getopt()
        self._check()

        with open(self.csv, 'r', newline='', encoding='utf-8', errors='ignore') as f:
            inputs = csv.reader(f)
            if self.hasHeaders:
                headers = next(inputs, None)
                if headers == None:
                    print("  [!] CSV file empty.")
                    sys.exit(4)
                else:
                    self._get_vars_from_request()
                    sorted_headers = headers
                    sorted_headers.sort()
                    self.vars.sort()
                    if sorted_headers != self.vars:
                        print("  [!] Headers from csv file and headers from request are different !")
                        print("  [-] CSV : %s " % sorted_headers)
                        print("  [-] Vars : %s" % self.vars)
                        sys.exit(4)
                    else:
                        for row in inputs:
                            fmt = {headers[i]:row[i] for i in range(len(headers))}
                            print("-- %s" % fmt)
                            print("-- %s" % self.request)
                            req = self.request.format(fmt)
                            print(" [-] %s" % req)
            else:
                for row in inputs:
                    fmt= "'"+"','".join(row)+"'"
                    print("-- %s" % fmt)
                    print("-- %s" % self.request)
                    req = self.request.format(eval(fmt))
                    print(" [-] %s" % req)

def main():
    query = Query()
    query.execute()

if __name__ == "__main__":
    main()