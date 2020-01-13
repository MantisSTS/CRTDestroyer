import requests
import urllib3
import json
import argparse
import sys

class Crtsh:

    crtsh_url = 'https://crt.sh/?q=%25.{}&output=json'
    results = {}
    only_tld = False
    
    def __init__(self, only_tld=False):
        self.only_tld = only_tld
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        pass

    def get_parents(self, domain):
        data = self.get_crt_data(domain)
        for subdomain in data:
            subdomain = '.'.join(domain.rsplit('.')[0:3])
            self.results[subdomain] = []
            
        return self.results

    def get_children(self, domain):
        data = self.get_crt_data(domain)
        for subdomain in data:
            self.results[domain].append(subdomain)
        return self.results


    def get_crt_data(self, url):
        r = requests.get(self.crtsh_url.format(url), verify=False)
        results = []
        try:
            data = json.loads(r.text)
            # Checks if array is empty
            for line in data:
                
                entry = line['name_value'].strip('\\n').strip("*.")
                
                # This is to fix data in the crt.sh results that come back with *.google.com\n*.xyz.google.com\n...
                if '\n' in line['name_value']:
                    lines = line['name_value'].splitlines()
                    for l in lines:
                        self.get_crt_data(l)
                if entry not in results :
                    results.append(entry)
        except Exception as e:
            
            # Maybe actually do something with this
            pass

        return results

    def get_results(self):
        return self.results

class FilterData:

    def __init__(self):
        pass

def parse_args():
    parser = argparse.ArgumentParser('Mantis\'s rewrite of Nahamsec\'s CRTnDestroy')
    parser.add_argument('-d', '--domain', required=True, help='The domain you want to search subdomains for')
    parser.add_argument('-f', '--filter', required=False, nargs='*', help='Search for specific filters, eg. corp,internal,api etc. Use flag this multiple times')
    parser.add_argument('-o', '--only-tld', required=False, default=False, help='Only return the "top-level" items (1-depth of subdomains)')
    parser.add_argument('-r', '--recursion-limit', required=False, type=int, default=1, help='The number of subdomains to go back. Default = 1')
    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = parse_args()

    crt = Crtsh(args.only_tld)
    crt.get_parents(args.domain)
    data = crt.get_results()
    children = []
    if not args.only_tld:
        if args.recursion_limit > 0:
           for item in data:
               children.append(crt.get_children(item))
        else:
            print("Recursion limit cannot be less than 1")
    print(children)
