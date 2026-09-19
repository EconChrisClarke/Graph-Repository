import os, pandas as pd, numpy as np
HERE=os.path.dirname(os.path.abspath(__file__)); DATA=os.path.join(HERE,'..','data')
d=pd.read_csv(os.path.join(DATA,'owid_maddison_gdp_per_capita.csv')).rename(columns={'GDP per capita':'g'})
keep=['United States','Canada','Australia','United Kingdom','France','Germany','Italy','Japan','Spain','Portugal','Greece','Ireland',
 'South Korea','Taiwan','Singapore','Hong Kong','Chile','Poland','Czechia','Hungary','Malaysia','Turkey','Russia','Argentina','Mexico','Thailand','China']
W=5
out=[]
for e in keep:
    s=d[d.Entity==e].set_index('Year').g.sort_index()
    s=s.reindex(range(int(s.index.min()),int(s.index.max())+1)).interpolate()  # fill any gaps
    below=s[s<15000]; cross=int(below.index[-1])+1 if len(below) else int(s.index[0])
    if s.iloc[-1]<15000: print('drop',e); continue
    cagr=(s/s.shift(W))**(1/W)-1
    for y in s.index:
        if not np.isnan(cagr[y]): out.append((e,y,y-cross,cross,s[y],cagr[y]*100))
o=pd.DataFrame(out,columns=['country','year','t','cross_year','gdppc','growth5'])
o.to_csv(os.path.join(DATA,'growth_since_15k.csv'),index=False)
print(o.groupby('country').agg(cross=('cross_year','first'),tmin=('t','min'),tmax=('t','max')).sort_values('cross').to_string())
p=o.pivot(index='t',columns='country',values='growth5')
print(p.loc[[0,2,5,10,15,20,30,40]].round(1).T.to_string())
print(o[o.country=='China'][['year','t','gdppc','growth5']].tail(12).round(2).to_string())
