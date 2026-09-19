import os, pandas as pd, json
o=pd.read_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','growth_since_15k.csv'))
o=o[(o.t>=-10)&(o.t<=40)]
p=o.pivot(index='t',columns='country',values='growth5')
oth=[c for c in p.columns if c!='China']
med=p[oth].median(axis=1)[p[oth].count(axis=1)>=8]
NAMES={'United States':'USA','United Kingdom':'U.K.'}
CROSS=o.groupby('country').cross_year.first().to_dict()
def ser(name,s):
    s=s.dropna(); d={"name":NAMES.get(name,name),"data":[[int(t),round(float(v),2)] for t,v in s.items()]}
    if name in CROSS: d["xOffset"]=int(CROSS[name])
    return d
m=ser('Median',med); m['color']='#111827'
ch=ser('China',p['China']); ch['color']='#C71E1D'
series=[ser(c,p[c]) for c in oth]+[m,ch]
cfg={"type":"line","xType":"number",
 "headline":"China continues to grow faster than average at similar stage of development",
 "subhead":"Average annual GDP per capita growth over the prior 5 years, by years since reaching $15,000 (2011 int'l $)",
 "source":"Maddison Project Database 2023 (via Our World in Data); author's calculations",
 "sourceUrl":"https://www.rug.nl/ggdc/historicaldevelopment/maddison/releases/maddison-project-database-2023",
 "note":"Year 0 = first year after which GDP per capita stays at or above $15,000 (2011 international dollars). Growth is the trailing 5-year compound rate. China reached $15,000 in 2017; latest data is 2022.",
 "xLabel":"Years since reaching $15,000 GDP per capita","yLabel":"5-year annualized growth (%)",
 "format":{"suffix":"%","decimals":0},"xFormat":{"decimals":0},
 "highlight":["China","Median"],
 "xNice":True,"hoverDecimals":1,"xHover":{"prefix":"+","suffix":" yrs"},"xMin":-10,"xMax":40,"rules":[{"axis":"x","at":0,"label":"$15,000"}],
 "series":series}
json.dump(cfg,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','chart.json'),'w'))
print(med.round(1).loc[[-10,-5,0,5,10,15,20,30,40]].to_dict())
