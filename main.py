import pyasx.data.companies
import json
import datetime


def get_all_companies_name():
    # get all listed companies and show it as string
    results = pyasx.data.companies.get_listed_companies()
    return results


def my_converter(o):
    # Used for date convert issues
    if isinstance(o, datetime.datetime):
        return o.__str__()


def stock_info(ticker):
    # get all listed companies and show it as string
    info = pyasx.data.companies.get_company_info(ticker)
    return json.dumps(info, indent=4, sort_keys=True, default=my_converter)


def store_all_ticker():
    all_companies = get_all_companies_name()
    data = []
    for i in all_companies:
        data.append(i['ticker'])
    return data


def main():
    # utilise data
    data = store_all_ticker()
    # print(data)
    print(stock_info('BHP'))


# main caller
if __name__ == '__main__':
    main()
