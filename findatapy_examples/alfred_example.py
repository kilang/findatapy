__author__ = 'saeedamen'  # Saeed Amen

#
# Copyright 2016 Cuemacro
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the
# License. You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and limitations under the License.
#


if __name__ == '__main__':
    try:
        import multiprocessing;

        multiprocessing.freeze_support()
    except:
        pass

    from findatapy.market import Market, MarketDataRequest, MarketDataGenerator

    market = Market(market_data_generator=MarketDataGenerator())

    # get the first release for GDP and also print the release date of that
    md_request = MarketDataRequest(
        start_date="01 Jun 2000",                                                      # start date (download data over past decade)
        data_source='alfred',                                                          # use ALFRED/FRED as data source
        tickers=['US GDP'],                                                            # ticker
        fields=['actual-release', 'release-date-time-full'],                           # which fields to download
        vendor_tickers=['GDP'],                                                        # ticker (FRED)
        vendor_fields=['actual-release', 'release-date-time-full'])                    # which FRED fields to download

    df = market.fetch_market(md_request)

    print(df)

    # compare the close and actual release of US GDP (and the final)
    md_request = MarketDataRequest(
        start_date="01 Jun 2000",                                                      # start date (download data over past decade)
        data_source='alfred',                                                          # use ALFRED/FRED as data source
        tickers=['US GDP'],                                                            # ticker
        fields=['actual-release', 'close'],                                            # which fields to download
        vendor_tickers=['GDP'],                                                        # ticker (FRED)
        vendor_fields=['actual-release', 'close'])                                     # which FRED fields to download

    df = market.fetch_market(md_request)

    from chartpy import Chart, Style

    style = Style(title="US GDP first vs last")

    Chart().plot(df, style=style)

    # get the change NFP SA (need to calculate that from the acutal-release and first-revision)
    md_request = MarketDataRequest(
        start_date="01 Jun 2000",                                                      # start date (download data over past decade)
        data_source='alfred',                                                          # use ALFRED/FRED as data source
        tickers=['US NFP'],                                                            # ticker
        fields=['actual-release', 'first-revision', 'release-date-time-full'],         # which fields to download
        vendor_tickers=['PAYEMS'],                                                     # ticker (FRED)
        vendor_fields=['actual-release', 'first-revision', 'release-date-time-full'])  # which FRED fields to download

    df = market.fetch_market(md_request)

    # calculate the headline change in NFP
    df['US NFP change'] = df['US NFP.actual-release'] - df['US NFP.first-revision'].shift(1)

    print(df)

    from chartpy import Chart, Style
    import pandas

    style = Style(title="US NFP change (actual)")

    df1 = pandas.DataFrame(df['US NFP change'])

    Chart().plot(df1, style=style)
