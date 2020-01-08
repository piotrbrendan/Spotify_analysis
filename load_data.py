import pandas as pd
from collections import namedtuple
import requests
import pathlib2
from io import StringIO
from datetime import date,timedelta

REGION = 'global'
START_DATE = date(2019, 1, 1)
STOP_DATE = date(2019, 12, 31)

DateRange = namedtuple('DateRange','start_date end_date')


def main(week_end_d=START_DATE,
         stop_end_d=STOP_DATE):
    dates_lst = []
    raw_url = 'https://spotifycharts.com/regional/{region}/weekly/{start_d}--{end_d}/download'

    while week_end_d <= stop_end_d:
        # get every Friday of the year
        if week_end_d.weekday() == 4:
            week_start_d = week_end_d - timedelta(days=7)
            dates_lst.append(DateRange(start_date=week_start_d, end_date=week_end_d))
        week_end_d += timedelta(days=1)

    for date_rng in dates_lst:
        start_d = date_rng.start_date.strftime(format='%Y-%m-%d')
        end_d = date_rng.end_date.strftime(format='%Y-%m-%d')
        url = raw_url.format(
            region=REGION,
            start_d=start_d,
            end_d=end_d)

        resp = requests.get(url)
        text = resp.content.decode('utf8')
        df = pd.read_csv(StringIO(text), skiprows=1)
        df['type'] = REGION
        df['week_end_d'] = end_d
        df.to_csv('spotify_top_{end_d}.csv'.format(end_d=end_d), index=False)

    paths = pathlib2.Path('').glob('spotify*.csv')
    pddfs = (pd.read_csv(p) for p in paths)

    df_2019 = pd.concat(pddfs, ignore_index=True)
    df_2019.to_csv('total_spotify_top_2019.csv')


if __name__ == '__main__':
    main()