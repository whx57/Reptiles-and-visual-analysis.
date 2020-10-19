#一 导包
import requests
import re
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


#二 爬取
#伪装
headers ={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
}
resp=requests.get('https://ncov.dxy.cn/ncovh5/view/pneumonia')
# print(resp.text)
#解决中文乱码
resp.encoding ='utf-8'
#保存源代码
os.chdir(r'F:\项目\5120194671-吴熙-新冠疫情可视化分析')
# print(os.getcwd())
file = open('code.txt',mode='w',encoding='utf-8')
file.write(resp.text)

#3提取
province=re.findall('{"provinceName":"(.*?)","provinceShortName":"(.*?)","currentConfirmedCount":(.*?),"confirmedCount":(.*?),"suspectedCount":(.*?),"curedCount":(.*?),"deadCount":(.*?),"',resp.text)
# print(province)
country=re.findall('"provinceName":"(.*?)","provinceShortName":"","cityName":"","currentConfirmedCount":(.*?),"confirmedCount":(.*?),"confirmedCountRank":.*?,"suspectedCount":(.*?),"curedCount":(.*?),"deadCount":(.*?),"deadCountRank":.*?,"deadRate":"(.*?)","deadRateRank":.*?,',resp.text)
# print(country)
sccity0=re.findall('(?<=四川)(.*?)(?=浙江省)(.*?)',resp.text)
# print(sccity0)
for i in sccity0:
    sccity0=''.join(i)
# print(sccity0)
sccity=re.findall('"cityName":"(.*?)","currentConfirmedCount":(.*?),"confirmedCount":(.*?),"suspectedCount":(.*?),"curedCount":(.*?),"deadCount":(.*?),',sccity0)
# print(sccity)

#4数据处理
dfprovince=pd.DataFrame(province)
dfprovince.columns=["provinceName","provinceShortName","currentConfirmedCount","confirmedCount","suspectedCount","curedCount","deadCount"]
# dfprovince
dfcountry=pd.DataFrame(country)
dfcountry.columns=["provinceName","currentConfirmedCount","confirmedCount","suspectedCount","curedCount","deadCount","deadRate"]
# dfcountry
sccity=pd.DataFrame(sccity)
sccity.columns=["cityName","currentConfirmedCount","confirmedCount","suspectedCount","curedCount","deadCount"]


####各省数据处理
for i in dfprovince["confirmedCount"]:
    i=int(i)
dfprovince["confirmedCount"]=[int(x) for x in dfprovince["confirmedCount"]]
dfprovince["currentConfirmedCount"]=[int(x) for x in dfprovince["currentConfirmedCount"]]
dfprovince["curedCount"]=[int(x) for x in dfprovince["curedCount"]]
dfprovince["deadCount"]=[int(x) for x in dfprovince["deadCount"]]
dfprovince1=dfprovince
dfprovince1=dfprovince1.sort_values(axis = 0,ascending = False,by='confirmedCount',inplace=False)
# print(type(dfprovince["confirmedCount"][1]))


####country 的数据处理

dfcountry["currentConfirmedCount"]=[int(x) for x in dfcountry["currentConfirmedCount"]]
i=1
sum0=0
countryy=[]
for ji in dfcountry["currentConfirmedCount"]:
    if i==10:
        break
    sum0+=ji
    countryy.append(ji)
    i+=1
labels=[]
i=1
for ji in dfcountry['provinceName']:
    if i==10:
        break
    labels.append(ji)
    i+=1
sum1=sum(dfcountry["currentConfirmedCount"])
sum2=sum1-sum0
labels.append('其他国家')
countryy.append(sum2)
print(countryy)
print(labels)
Dfcountry

####sccity 的数据处理
sccityname=np.array(sccity['cityName'])
sccity["confirmedCount"]=[int(x) for x in sccity["confirmedCount"]]
sccity["curedCount"]=[int(x) for x in sccity["curedCount"]]
sccity["currentConfirmedCount"]=[int(x) for x in sccity["currentConfirmedCount"]]
sccity["deadCount"]=[int(x) for x in sccity["deadCount"]]
x1=np.array(sccity['confirmedCount'])
x2=np.array(sccity['curedCount'])
x3=np.array(sccity['currentConfirmedCount'])
x4=np.array(sccity['deadCount'])
print(sccityname)
Sccity

#5可视化
### 一中国各省疫情变化
prox1=np.array(dfprovince['provinceShortName'])
prox2=np.array(dfprovince1['provinceShortName'])
proy1=np.array(dfprovince1['confirmedCount'])
proy2=np.array(dfprovince['currentConfirmedCount'])
proy3=np.array(dfprovince1['curedCount'])
proy4=np.array(dfprovince1['deadCount'])
# print(prox1)
# print(proy1)
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.figure(figsize=(25, 15))
plt.bar(prox1, proy2,label='8月中国各省现存确诊患者')
plt.legend(loc='best',fontsize=30)
plt.title('2020 8月中国各省疫情', loc='center',fontsize=30)
plt.grid(True, axis='both')

plt.figure(figsize=(25, 15))
x = np.arange(len(prox2))
plt.bar(x+0.6, proy4,width=0.33,label='死亡总人数',color='black')
plt.bar(x+0.3, proy3,width=0.33,label='治疗总人数',tick_label=prox2,color='green')
plt.bar(x, proy1,width=0.33,label='患病总人数',color='red')
plt.legend(fontsize =30)
plt.title('各省疫情情况', loc='center',fontsize =30)

#世界各国疫情
plt.pie(countryy,labels=labels,autopct='%1.1f%%',shadow=False,startangle=150,radius=3.5)
plt.title('世界各国疫情')

#四川省各市疫情
plt.figure(figsize=(25, 15))
plt.bar(sccityname, x1,width=0.9,label='总确诊人数',color='r')
plt.bar(sccityname, x2,width=0.9,label='治疗人数',color='lightgreen')
plt.bar(sccityname, x3,width=0.9,label='现存患者人数',color='coral')
plt.bar(sccityname, x4,width=0.9,label='死亡人数',color='k')
plt.legend(fontsize =30)
plt.title('四川省各市疫情', loc='center',fontsize=40)


#####补充 修改省图
plt.figure(figsize=(25, 15))
cx=[]
plt.barh(prox1,proy2,label='低风险地区',color="green")
plt.barh(prox1,proy2,label='中等风险地区',color="y")
plt.barh(prox1,proy2 ,label='高风险地区',color=['r','r','y', 'y','y','y','y','y','y','green','green','green','green','green'])

plt.legend(loc='best',fontsize=30)
plt.title('2020 8月中国各省疫情', loc='center',fontsize=30)
plt.grid(True, axis='both')
for x, y in enumerate(proy2):
    plt.text(y + 0.2, x - 0.1, '%s' % y)

X = [0.5]
XX=[1.5]
Y = [20]
YY=[23]
plt.bar(X, Y, 1, color="green")
plt.bar(XX,YY,1,color="green")