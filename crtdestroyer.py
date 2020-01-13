import requests
import urllib3
import json
import argparse

class Crtsh:

    crtsh_url = 'https://crt.sh/?q=%25.{}&output=json'
    results = []
    only_tld = False
    
    def __init__(self, only_tld=False):
        self.only_tld = only_tld
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        pass

    def get_crt_data(self, url):
        r = requests.get(self.crtsh_url.format(url), verify=False)
        try:
            data = json.loads(r.text)
            # Checks if array is empty
            for line in data:
                self.parse_entry(line['name_value'])
        except Exception as e:
            # Maybe actually do something with this
            pass

        return data

    def parse_entry(self, line):
        # Remove any *. instances in the domain

        # Create an alias - hacky
        subdomain = line.strip("*.")

        if self.only_tld:
            subdomain = '.'.join(subdomain.rsplit('.')[0:3])
        

        if subdomain not in self.results:
            print(subdomain)
            self.results.append(subdomain)
        return self.results

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
    args = parser.parse_args()
    return args

if __name__ == '__main__':

    args = parse_args()

    crt = Crtsh(args.only_tld)
    crt.get_crt_data(args.domain)
    data = crt.get_results()

    if not args.only_tld:
        for line in data:
            crt.get_crt_data(line)
        print("\n".join(crt.get_results()))
