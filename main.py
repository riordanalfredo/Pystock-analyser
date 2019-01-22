import pyasx.data.companies
import json
import datetime


def main():
    # results = pyasx.data.companies.get_listed_companies()
    # print(json.dumps(results, indent=4, sort_keys=True))

    print(stock_info('CBA'))


def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def stock_info(ticker):
    info = pyasx.data.companies.get_company_info(ticker)
    return json.dumps(info, indent=4, sort_keys=True, default=myconverter)

if __name__ == '__main__':
    main()