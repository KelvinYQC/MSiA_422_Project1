import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

class BabyNames:

    def __init__(self, file_location):
        states = {
            'AK': 'Alaska',
            'AL': 'Alabama',
            'AR': 'Arkansas',
            'AS': 'American Samoa',
            'AZ': 'Arizona',
            'CA': 'California',
            'CO': 'Colorado',
            'CT': 'Connecticut',
            'DC': 'District of Columbia',
            'DE': 'Delaware',
            'FL': 'Florida',
            'GA': 'Georgia',
            'GU': 'Guam',
            'HI': 'Hawaii',
            'IA': 'Iowa',
            'ID': 'Idaho',
            'IL': 'Illinois',
            'IN': 'Indiana',
            'KS': 'Kansas',
            'KY': 'Kentucky',
            'LA': 'Louisiana',
            'MA': 'Massachusetts',
            'MD': 'Maryland',
            'ME': 'Maine',
            'MI': 'Michigan',
            'MN': 'Minnesota',
            'MO': 'Missouri',
            'MP': 'Northern Mariana Islands',
            'MS': 'Mississippi',
            'MT': 'Montana',
            'NA': 'National',
            'NC': 'North Carolina',
            'ND': 'North Dakota',
            'NE': 'Nebraska',
            'NH': 'New Hampshire',
            'NJ': 'New Jersey',
            'NM': 'New Mexico',
            'NV': 'Nevada',
            'NY': 'New York',
            'OH': 'Ohio',
            'OK': 'Oklahoma',
            'OR': 'Oregon',
            'PA': 'Pennsylvania',
            'PR': 'Puerto Rico',
            'RI': 'Rhode Island',
            'SC': 'South Carolina',
            'SD': 'South Dakota',
            'TN': 'Tennessee',
            'TX': 'Texas',
            'UT': 'Utah',
            'VA': 'Virginia',
            'VI': 'Virgin Islands',
            'VT': 'Vermont',
            'WA': 'Washington',
            'WI': 'Wisconsin',
            'WV': 'West Virginia',
            'WY': 'Wyoming'
        }
        newlist = []
        count = 0
        columns = ['state', 'sex', 'year', 'name', 'births']
        for st in states.keys():
            path = file_location + '/' + st + '.TXT'
            try:
                df = pd.read_csv(path, names=columns)
                count += 1
            except:
                continue
            newlist.append(df)
        self.dat = pd.concat(newlist, ignore_index=True)

    # TODO: not sure over here
    def count(self, state, year):
        if state and year:  # return state and year value.
            return sum(self.dat[(self.dat['year'] == year) & (self.dat['state'] == state)]["births"])
        elif state and not year:  # return count of empty values
            return (sum(self.dat[(self.dat['state'] == state)]["births"]))
        elif not state and year:
            return (sum(self.dat["births"]))

    def top10Names(self, state, year):
        # check state and year value
        if state and year:
            unranked_df = self.dat[(self.dat['year'] == year) & (self.dat['state'] == state)]
        elif state and not year:  # return count of empty values
            unranked_df = self.dat[(self.dat['state'] == state)]
        elif not state and year:
            unranked_df = self.dat[(self.dat['year'] == year)]
        else:
            unranked_df = self.dat
        # group by data by name and sex to find sum of births counts
        unranked_df = pd.DataFrame(unranked_df.groupby(["sex", 'name']).sum(['births']).reset_index())
        # rank the data
        unranked_df["ranking"] = unranked_df.groupby("sex")['births'].rank(method='min', ascending=False)
        # choose top 10 data
        df_cleaned = unranked_df[(unranked_df['ranking'] <= 10)][['name', 'sex', 'ranking']]  # select columns
        # pivot the table
        new_table = df_cleaned.pivot_table(index='ranking', columns='sex', values='name', aggfunc=lambda x: x)
        return new_table

    def ChangeOfPopularity(self, fromYear, toYear, top):
        df_from = self.dat[self.dat["year"] == fromYear]
        df_to = self.dat[self.dat["year"] == toYear]

        df1 = df_from[['births', 'name']].groupby(['name']).sum().reset_index()
        df1["name_percentage"] = df1['births'] / df1['births'].sum()
        df2 = df_to[['births', 'name']].groupby(['name']).sum().reset_index()
        df2["name_percentage"] = df2['births'] / df2['births'].sum()
        hashmap = defaultdict(list)

        for name in df1['name']:
            percentIn2 = df2[df2['name'] == name]['name_percentage'].values
            if not percentIn2.any():
                hashmap[name].append(-df1[df1['name'] == name]['name_percentage'].values.item(0))
            else:
                hashmap[name].append((df2[df2['name'] == name]['name_percentage'].values - df1[df1['name'] == name][
                    'name_percentage'].values).item(0))

        for name in df2['name']:
            # if not df1[df1['name'] == name]['name_percentage'].values.any():
            if name not in hashmap.keys():
                hashmap[name].append(df2[df2['name'] == name]['name_percentage'].values.item(0))

        orderingDF = pd.DataFrame.from_dict(hashmap, orient='index', columns=['percentChange'])

        orderingDF = orderingDF.sort_values(by=['percentChange'], ascending=False)
        print('Top ten increased names')
        print(orderingDF.head(top).index.tolist())
        print('Top ten decreased names')
        print(orderingDF.tail(top).index.tolist())
        print('Ten does not move much names')
        orderingDF['doNotmove'] = (orderingDF['percentChange'] - 0).abs()
        orderingDF = orderingDF.sort_values(by=['doNotmove'], ascending=True)
        print(orderingDF.head(top).index.tolist())



    def Top5NamesPerYear(self, year, sex):
        df_male = self.dat[(self.dat["year"] == year) & (self.dat['sex'] == sex)]
        df_male["ranking"] = df_male.groupby(["sex", 'state'])['births'].rank(method='min', ascending=False)
        df_male_5 = df_male[(df_male['ranking'] <= 5)][['state', 'ranking', 'births']]  # select columns
        print(df_male_5)
        # TODO: still need to pivot/flatten the table
        pass

    def NamePopularityPlot(self, name, yearRange, state, sex):
        df1 = self.dat[self.dat["year"].isin(range(*yearRange)) & (self.dat['sex'] == sex) & (self.dat['state'] == state) & (self.dat['name'] == name)]
        df1["name_percentage"] = df1['births'] / df1['births'].sum()
        df1 = df1[['year', 'name_percentage']]
        df1 = df1.set_index(['year'])
        df1.plot(color='Blue')
        plt.show()
        return

    def NameFlip(self, n):
        # TODO: List top n names that filliped over the years. (i.e. from boy name to girl or the reverse). Provide a plot of the names showing the year.
        pass



a = BabyNames('/Users/kelvin/Desktop/MSiA/MSiA_422_python-java/Projects/namesbystate')

name='John'
yearRange=(1910,2020)
state='AK'
sex='M'
print(a.count('',' '))
print(a.top10Names(state, 1910))
print(a.ChangeOfPopularity(1910, 1915, 10))
print(a.NamePopularityPlot(name, yearRange, state, sex))

