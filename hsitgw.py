'''
모니터링을 위해 분봉조건에 해당하는 코드를 전부 흩뿌렸다. 
'''

import win32com.client
import pythoncom
import pandas as pd 
import numpy as np
import time
from datetime import datetime, date
import schedule
#----------------------------------------------------------
#로그인 코드
#----------------------------------------------------------
class XASessionEventHandler:
    login_state=0
    def OnLogin(selfself, code, msg):
        if code =="0000":
            print("로그인 성공")
            XASessionEventHandler.login_state= 1
        else:
            print("로그인 실패")
class XAQueryEventHandlerO3106:
    query_state =0
    def OnReceiveData(self, code):
        XAQueryEventHandlerO3106.query_state = 1
id='lshblue3'
pw='godhfma1'
cert_pw='soheeya132@'
instXASession = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEventHandler)
instXASession.ConnectServer("hts.ebestsec.co.kr", 20001)
instXASession.Login(id, pw, cert_pw, 0, 0)
while XASessionEventHandler.login_state==0:
    pythoncom.PumpWaitingMessages()
#계좌정보 호출 코드
num_account = instXASession.GetAccountListCount()
for i in range(num_account):
    account = instXASession.GetAccountList(i)
    print(account)
#----------------------------------------------------------
#<항셍>
#전일고가, 전일저가, 전일 종가, 당일시가, 중심선
#----------------------------------------------------------
market=["HSIJ22"]
class DayData:
    def __init__(self, market, kind_p):
        self.first=market
        self.second=kind_p
        
    def set_data(self):
        class XAQueryEventHandlerO3108:
            query_state =0
            def OnReceiveData(self, code):
                    XAQueryEventHandlerO3108.query_state = 1
        instXAQueryO3108=win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerO3108)
        instXAQueryO3108.ResFileName="C:\\eBEST\\xingAPI\\Res\\o3108.res"
        instXAQueryO3108.SetFieldData("o3108InBlock", "shcode", 0, self.first)
        instXAQueryO3108.SetFieldData("o3108InBlock", "gubun", 0, self.second)
        instXAQueryO3108.Request(0)
        while XAQueryEventHandlerO3108.query_state == 0:
            pythoncom.PumpWaitingMessages() 
        day_empty=[]
        minprice=[]
        
        yd_s=instXAQueryO3108.GetFieldData("o3108OutBlock", "jisiga", 0)
        day_empty.append(yd_s)
        yd_h=instXAQueryO3108.GetFieldData("o3108OutBlock", "jihigh", 0)
        day_empty.append(yd_h)
        yd_l=instXAQueryO3108.GetFieldData("o3108OutBlock", "jilow", 0)
        day_empty.append(yd_l)
        yd_c=instXAQueryO3108.GetFieldData("o3108OutBlock", "jiclose", 0)
        day_empty.append(yd_c)
        td_s=instXAQueryO3108.GetFieldData("o3108OutBlock", "disiga", 0)
        day_empty.append(td_s)
        td_h=instXAQueryO3108.GetFieldData("o3108OutBlock", "dihigh", 0)
        day_empty.append(td_h)
        td_l=instXAQueryO3108.GetFieldData("o3108OutBlock", "dilow", 0)
        day_empty.append(td_l)
        td_c=instXAQueryO3108.GetFieldData("o3108OutBlock", "diclose", 0)
        day_empty.append(td_c)
        td_center=(float(td_h)+float(td_l))/2
        day_empty.append(td_center)

        day_price=pd.DataFrame(day_empty)
        minprice=day_price.rename(index={0:'Y_Open', 1:'Y_High', 2:'Y_Low', 3:'Y_Close', 4:'Open', 5:'High', 6:'Low', 7:'Close', 8:'MPrice'})
        return minprice
a=0
def day_data():
    ddata=DayData(market[0], 0)
    dayall=ddata.set_data()
    globals()['dayall']=dayall.T
    globals()['a']=globals()['a']+1
    b=datetime.now()
    print(globals()['a'])
    print(b)
    print('Ddata 1 cycle')
day_data()   #1분간격 호출


#----------------------------------------------------------
#<항셍>
#Tick Data Call
#----------------------------------------------------------
class TickData:
    def __init__(self, gubun, market, number, gunsu):
        self.first=gubun
        self.second=market
        self.third=number
        self.forth=gunsu
        
    def tick_data(self):
        pythoncom.CoInitialize()
        class XAQueryEventHandlerO3139:
            query_state =0
            def OnReceiveData(self, code):
                    XAQueryEventHandlerO3139.query_state = 1
        instXAQueryO3139=win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerO3139)
        instXAQueryO3139.ResFileName="C:\\eBEST\\xingAPI\\Res\\o3139.res"
        instXAQueryO3139.SetFieldData("o3139InBlock", "mktgb", 0, self.first)
        instXAQueryO3139.SetFieldData("o3139InBlock", "shcode", 0, self.second)
        instXAQueryO3139.SetFieldData("o3139InBlock", "ncnt", 0, self.third)
        instXAQueryO3139.SetFieldData("o3139InBlock", "qrycnt", 0, self.forth)
        instXAQueryO3139.Request(0)
        while XAQueryEventHandlerO3139.query_state == 0:
            pythoncom.PumpWaitingMessages() 
        count=instXAQueryO3139.GetBlockCount("o3139OutBlock1")
        min_empty=[]
        tickprice=[]
        for i in range(count):
            date=instXAQueryO3139.GetFieldData("o3139OutBlock1", "date", i)
            min_empty.append(date)
            time=instXAQueryO3139.GetFieldData("o3139OutBlock1", "time", i)
            min_empty.append(time)
            o=instXAQueryO3139.GetFieldData("o3139OutBlock1", "open", i)
            min_empty.append(o)
            h=instXAQueryO3139.GetFieldData("o3139OutBlock1", "high", i)
            min_empty.append(h)
            l=instXAQueryO3139.GetFieldData("o3139OutBlock1", "low", i)
            min_empty.append(l)
            c=instXAQueryO3139.GetFieldData("o3139OutBlock1", "close", i)
            min_empty.append(c)
            v=instXAQueryO3139.GetFieldData("o3139OutBlock1", "volume", i)
            min_empty.append(v)
        pythoncom.CoUninitialize()
        
        for j in range(101):
            min_empty[(7*j-7):(7*(j+1)-7)]
            tickprice.append(min_empty[(7*j-7):(7*(j+1)-7)])
        tickprice=tickprice[1:]
        tickprice=pd.DataFrame(tickprice)
        t=tickprice.rename(columns={0:'Date', 1:'Time', 2:'Open', 3:'High', 4:'Low', 5:'Close', 6:'Volume'})
        t['Time']=t['Date']+t['Time']
        t['Time']=t['Time'].astype('str')
        t['Time']=pd.to_datetime(t['Time'])
        t=t.drop(columns=['Date'])
        t.index=t['Time']
        globals()['t120']=t.drop(columns='Time')
        globals()['t120']=globals()['t120'].sort_index(ascending=True)
      

tickdata=TickData("F", "HSIJ22", 120, 100) 
tickdata.tick_data()
#----------------------------------------------------------
#각 분봉 호출코드 (필요 분봉: 1, 3, 5, 30, 60, 90, 120, 150, 240, 360, 480, 960)
#----------------------------------------------------------
class MinuteData:
    def __init__(self, market, minute, number):
        self.first=market
        self.second=minute
        self.third=number
        
    def set_data(self):
        pythoncom.CoInitialize()
        class XAQueryEventHandlerO3103:
            query_state =0
            def OnReceiveData(self, code):
                    XAQueryEventHandlerO3103.query_state = 1
        instXAQueryO3103=win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEventHandlerO3103)
        instXAQueryO3103.ResFileName="C:\\eBEST\\xingAPI\\Res\\o3103.res"
        instXAQueryO3103.SetFieldData("o3103InBlock", "shcode", 0, self.first)
        instXAQueryO3103.SetFieldData("o3103InBlock", "ncnt", 0, self.second)
        instXAQueryO3103.SetFieldData("o3103InBlock", "readcnt", 0, self.third)
        instXAQueryO3103.Request(0)
        while XAQueryEventHandlerO3103.query_state == 0:
            pythoncom.PumpWaitingMessages() 
        count=instXAQueryO3103.GetBlockCount("o3103OutBlock1")
        min_empty=[]
        minprice=[]
        for i in range(count):
            date=instXAQueryO3103.GetFieldData("o3103OutBlock1", "date", i)
            min_empty.append(date)
            time=instXAQueryO3103.GetFieldData("o3103OutBlock1", "time", i)
            min_empty.append(time)
            o=instXAQueryO3103.GetFieldData("o3103OutBlock1", "open", i)
            min_empty.append(o)
            h=instXAQueryO3103.GetFieldData("o3103OutBlock1", "high", i)
            min_empty.append(h)
            l=instXAQueryO3103.GetFieldData("o3103OutBlock1", "low", i)
            min_empty.append(l)
            c=instXAQueryO3103.GetFieldData("o3103OutBlock1", "close", i)
            min_empty.append(c)
        pythoncom.CoUninitialize()
        
        for j in range(101):
            min_empty[(6*j-6):(6*(j+1)-6)]
            minprice.append(min_empty[(6*j-6):(6*(j+1)-6)])
        minprice=minprice[1:]
        minprice=pd.DataFrame(minprice)
        minprice=minprice.rename(columns={0:'Date', 1:'Time', 2:'Open', 3:'High', 4:'Low', 5:'Close'})
        minprice=minprice.sort_index(ascending=False)
        return minprice
minute=[1, 5, 30, 240]
def loop_data():
    for i in minute:
        globals()['mt{}'.format(i)]=MinuteData(market[0], i, 100)
        globals()['mt{}'.format(i)]=globals()['mt{}'.format(i)].set_data()
        globals()['mt{}'.format(i)]['Time']=globals()['mt{}'.format(i)]['Date']+globals()['mt{}'.format(i)]['Time']
        globals()['mt{}'.format(i)]['Time']=globals()['mt{}'.format(i)]['Time'].astype('str')
        globals()['mt{}'.format(i)]['Time']=pd.to_datetime(globals()['mt{}'.format(i)]['Time'])
        globals()['mt{}'.format(i)]=globals()['mt{}'.format(i)].drop(columns=['Date'])
        globals()['mt{}'.format(i)].index=globals()['mt{}'.format(i)]['Time']
        globals()['mt{}'.format(i)]=globals()['mt{}'.format(i)].drop(columns='Time')                 
        time.sleep(1)
loop_data()
schedule.every(0.1).seconds.do(tickdata.tick_data)
schedule.every(1).minutes.do(loop_data)
schedule.every(1).minutes.do(day_data)
import pyautogui
import pyperclip

globals()['cur_enter_price']=0
globals()['states']=0
globals()['hsi_cur']=0
while True:
    schedule.run_pending()
    
    #기준선 전처리

    bb=[]
    ma=[12, 20]
    mul=[0.3, 1.8, 2.25]
    allocate_num=[2, 3, 4]
    minute=[1, 5, 30, 240]
    cur_price=dayall["Close"][0]
    round_down_buy=float(cur_price)-float(cur_price)%100+10
    round_down_sell=float(cur_price)-float(cur_price)%100-10
    round_up_buy=float(cur_price)-float(cur_price)%100+100+10
    round_up_sell=float(cur_price)-float(cur_price)%100+100-10
    yh_buy=float(dayall['Y_High'])+10
    yh_sell=float(dayall['Y_High'])-10
    yl_buy=float(dayall['Y_Low'])+10
    yl_sell=float(dayall['Y_Low'])-10
    yc_buy=float(dayall['Y_Close'])+10
    yc_sell=float(dayall['Y_Close'])-10
    do_buy=float(dayall['Open'])+10
    do_sell=float(dayall['Open'])-10
    dm_buy=float(dayall['MPrice'])+10
    dm_sell=float(dayall['MPrice'])-10

    #Case A 분봉 가공
    for i in minute:  
        globals()['mt{}'.format(i)].iloc[-1]["Close"]=t120['Close'][-1] 
        if float(t120['Close'][-1]) > float(globals()['mt{}'.format(i)].iloc[-1]["High"]):
            globals()['mt{}'.format(i)].iloc[-1]["High"]=t120['Close'][-1]
        elif float(t120['Close'][-1]) < float(globals()['mt{}'.format(i)].iloc[-1]["Low"]): 
            globals()['mt{}'.format(i)].iloc[-1]["Low"]=t120['Close'][-1]
        for t in allocate_num:
            globals()['mt{}'.format(t*i)] = pd.DataFrame()
            globals()['mt{}'.format(t*i)]['Open'] = globals()['mt{}'.format(i)].Open.resample('{}T'.format(i*t)).first()
            globals()['mt{}'.format(t*i)]['Close'] = globals()['mt{}'.format(i)].Close.resample('{}T'.format(i*t)).last()
            globals()['mt{}'.format(t*i)]['High'] = globals()['mt{}'.format(i)].High.resample('{}T'.format(i*t)).max()
            globals()['mt{}'.format(t*i)]['Low'] = globals()['mt{}'.format(i)].High.resample('{}T'.format(i*t)).min()
            globals()['mt{}'.format(t*i)]=globals()['mt{}'.format(t*i)].dropna(axis=0)
            globals()['mt{}'.format(t*i)].iloc[-1]["Close"]=t120['Close'][-1] 
            if float(t120['Close'][-1]) > float(globals()['mt{}'.format(t*i)].iloc[-1]["High"]):
                globals()['mt{}'.format(t*i)].iloc[-1]["High"]=t120['Close'][-1]
            elif float(t120['Close'][-1]) < float(globals()['mt{}'.format(t*i)].iloc[-1]["Low"]): 
                globals()['mt{}'.format(t*i)].iloc[-1]["Low"]=t120['Close'][-1]                        
            for j in ma:
                globals()['mt{}_{}'.format(t*i, j)]=globals()['mt{}'.format(t*i)]['Close'].rolling(window=j).mean()
                globals()['mt{}_{}'.format(i, j)]=globals()['mt{}'.format(i)]['Close'].rolling(window=j).mean()
                for k in mul:                 
                    globals()['mt{}_{}_{}_upper'.format(t*i, j, int(k))]=globals()['mt{}_{}'.format(t*i, j)]+k*globals()['mt{}'.format(t*i)]['Close'].rolling(window=j).std()                                        
                    globals()['bb'].append([name for name in globals() if globals()[name] is globals()['mt{}_{}_{}_upper'.format(t*i, j, int(k))]])
                    globals()['mt{}_{}_{}_lower'.format(t*i, j, int(k))]=globals()['mt{}_{}'.format(t*i, j)]-k*globals()['mt{}'.format(t*i)]['Close'].rolling(window=j).std()                    
                    globals()['bb'].append([name for name in globals() if globals()[name] is globals()['mt{}_{}_{}_lower'.format(t*i, j, int(k))]])
                    globals()['mt{}_{}_{}_lower'.format(t*i, j, int(k))].sort_index(ascending=False)
                    globals()['mt{}_{}_{}_upper'.format(i, j, int(k))]=globals()['mt{}_{}'.format(i, j)]+k*globals()['mt{}'.format(i)]['Close'].rolling(window=j).std()                    
                    globals()['bb'].append([name for name in globals() if globals()[name] is globals()['mt{}_{}_{}_upper'.format(i, j, int(k))]])
                    globals()['mt{}_{}_{}_lower'.format(i, j, int(k))]=globals()['mt{}_{}'.format(i, j)]-k*globals()['mt{}'.format(i)]['Close'].rolling(window=j).std()                    
                    globals()['bb'].append([name for name in globals() if globals()[name] is globals()['mt{}_{}_{}_lower'.format(i, j, int(k))]])
                    globals()['mt{}_{}_{}_lower'.format(i, j, int(k))].sort_index(ascending=False) 
    price=['round_down_', 'round_up_', 'yh_', 'yl_', 'yc_', 'do_', 'dm_']
    buy=[]
    sell=[]
    for i in price:
        buy.append(globals()['{}buy'.format(i)])
        sell.append(globals()['{}sell'.format(i)])
    #조건 및 조건을 프로그램과 연동
    #밴드차트 
    upperline=t120['High'].rolling(window=16).max()
    lowerline=t120['Low'].rolling(window=16).min()
    midline=(upperline+lowerline)/2
    t120=pd.DataFrame(t120)
    m1=mt1
    m3=mt3
        #3분봉, 1분봉 볼벤 세팅
    m3_mean=m3['Close'].rolling(window=20).mean()
    m1_mean=m1['Close'].rolling(window=20).mean()
    for k in mul:                 
        globals()['mt3_{}_upper'.format(int(k))]=m3_mean+k*m3['Close'].rolling(window=20).std()                                        
        globals()['mt3_{}_lower'.format(int(k))]=m3_mean-k*m3['Close'].rolling(window=20).std()                    
        globals()['mt1_{}_upper'.format(int(k))]=m1_mean+k*m1['Close'].rolling(window=20).std()                    
        globals()['mt1_{}_lower'.format(int(k))]=m1_mean-k*m1['Close'].rolling(window=20).std()      
    #조건 정리
    min_kind=[5, 10, 15, 20, 30, 60, 90, 120, 240, 480, 960]
    for a in min_kind:
        for b in ma:
            #buy----------------------------------------------------------
            globals()['buybb_btw{}_{}'.format(a, b)]=round(globals()['mt{}_{}_2_lower'.format(a, b)][-1], 2) <= float(globals()['mt{}'.format(a)].iloc[-1]['Low']) <= round(globals()['mt{}_{}_1_lower'.format(a, b)][-1], 2)
            #Low값이 볼린저밴드 하단선 구간안에 있는지 판단. (1)
            globals()['buybb_1n2cndl{}_{}'.format(a, b)]=round(globals()['mt{}_{}_1_lower'.format(a, b)][-1], 2) >= round(globals()['mt{}_{}_1_lower'.format(a, b)][-2], 2)
            globals()['buybb_2n3cndl{}_{}'.format(a, b)]=round(globals()['mt{}_{}_1_lower'.format(a, b)][-2], 2) >= round(globals()['mt{}_{}_1_lower'.format(a, b)][-3], 2)
            #2봉전대비 1봉전 볼밴 하단선과 3봉전 대비 2봉전 볼밴 하단선이 닫혔는지 확인 (2, 3)
            globals()['buyma_btw{}_{}'.format(a, b)]=round(globals()['mt{}_{}_0_lower'.format(a, b)][-1], 2) <= float(globals()['mt{}'.format(a)].iloc[-1]['Low']) <= round(globals()['mt{}_{}_0_upper'.format(a, b)][-1], 2)
            #Low값이 볼린저밴드 중심선 구간안에 있는지 판단. (4)
            globals()['buybb_upcon{}_{}'.format(a, b)]=any((round(globals()['mt{}_{}_1_upper'.format(a, b)][-15:],2) <= globals()['mt{}'.format(a)]['High'][-15:].astype(float)))
            #15봉 안에서 볼린저밴드 상단값이 상승하고 있는지 확인 (5)
            globals()['buybb_cnlim{}_{}'.format(a, b)]=all((round(globals()['mt{}_{}_0_lower'.format(a, b)][-15:],2) <= globals()['mt{}'.format(a)]['Low'][-15:].astype(float)))
            #Low값이 15봉 안에서 중심선 Low 마지노선을 벗어났는지 확인 (6)
            #sell---------------------------------------------------------
            globals()['sellbb_btw{}_{}'.format(a, b)]=round(globals()['mt{}_{}_2_upper'.format(a, b)][-1], 2) >= float(globals()['mt{}'.format(a)].iloc[-1]['High']) >= round(globals()['mt{}_{}_1_upper'.format(a, b)][-1], 2)
            #High값이 볼린저밴드 상단선 구간안에 있는지 판단. (1)
            globals()['sellbb_1n2cndl{}_{}'.format(a, b)]=round(globals()['mt{}_{}_1_upper'.format(a, b)][-1], 2) <= round(globals()['mt{}_{}_1_upper'.format(a, b)][-2], 2)
            globals()['sellbb_2n3cndl{}_{}'.format(a, b)]=round(globals()['mt{}_{}_1_upper'.format(a, b)][-2], 2) <= round(globals()['mt{}_{}_1_upper'.format(a, b)][-3], 2)
            #2봉전대비 1봉전 볼밴 상단선과 3봉전 대비 2봉전 볼밴 상단선이 닫혔는지 확인 (2, 3)
            globals()['sellma_btw{}_{}'.format(a, b)]=round(globals()['mt{}_{}_0_lower'.format(a, b)][-1], 2) <= float(globals()['mt{}'.format(a)].iloc[-1]['High']) <= round(globals()['mt{}_{}_0_upper'.format(a, b)][-1], 2)
            #High값이 볼린저밴드 중심선 구간안에 있는지 판단. (4)
            globals()['sellbb_lwcon{}_{}'.format(a, b)]=any((round(globals()['mt{}_{}_1_lower'.format(a, b)][-15:],2) >= globals()['mt{}'.format(a)]['Low'][-15:].astype(float)))
            #15봉 안에서 볼린저밴드 하단값이 하락하고 있는지 확인 (5)
            globals()['sellbb_cnlim{}_{}'.format(a, b)]=all((round(globals()['mt{}_{}_0_upper'.format(a, b)][-15:],2) >= globals()['mt{}'.format(a)]['High'][-15:].astype(float)))
            #High값이 15봉 안에서 중심선 High 마지노선을 벗어났는지 확인 (6)
    #buy
    buybb_btw1=round(mt1_2_lower[-1], 2) <= float(m1.iloc[-1]['Low']) <= round(mt1_1_lower[-1], 2)
    buybb_btw3=round(mt3_2_lower[-1], 2) <= float(m3.iloc[-1]['Low']) <= round(mt3_1_lower[-1], 2)
    #1분봉과 3분봉의 Low값이 볼린저밴드 하단선 구간안에 있는지 판단. (1)
    buybb_1n2cndl1=round(mt1_1_lower[-1], 2) >= round(mt1_1_lower[-2], 2)
    buybb_2n3cndl1=round(mt1_1_lower[-2], 2) >= round(mt1_1_lower[-3], 2)
    buybb_1n2cndl3=round(mt3_1_lower[-1], 2) >= round(mt3_1_lower[-2], 2)
    buybb_2n3cndl3=round(mt3_1_lower[-2], 2) >= round(mt3_1_lower[-3], 2)
    #1분봉과 3분봉의 2봉전대비 1봉전 볼밴 하단선과 3봉전 대비 2봉전 볼밴 하단선이 닫혔는지 확인 (2, 3)
    buyma_btw1=round(mt1_0_lower[-1], 2) <= float(m1.iloc[-1]['Low']) <= round(mt1_0_upper[-1], 2)
    buyma_btw3=round(mt3_0_lower[-1], 2) <= float(m3.iloc[-1]['Low']) <= round(mt3_0_upper[-1], 2)
    #1분봉과 3분봉의 Low값이 볼린저밴드 중심산 구간안에 있는지 판단. (4)
    buybb_upcon1=any((round(mt1_1_upper[-15:],2) <= m1['High'][-15:].astype(float)))
    buybb_upcon3=any((round(mt3_1_upper[-15:],2) <= m3['High'][-15:].astype(float)))
    #1분봉과 3분봉이 15봉 안에서 볼린저밴드 상단값이 상승하고 있는지 확인 (5)
    buybb_cnlim1=all((round(mt1_0_lower[-15:],2) <= m1['Low'][-15:].astype(float)))
    buybb_cnlim3=all((round(mt3_0_lower[-15:],2) <= m3['Low'][-15:].astype(float)))
    #1분봉과 3분봉의 Low값이 15봉 안에서 중심선 Low 마지노선을 벗어났는지 확인 (6)
    buyban_lwupcon=any(upperline[-20:].astype(float) == t120['High'][-20:].astype(float))
    #밴드차트에서 20봉 이내에 상단선 값이 갱신된 적이 있는지 확인 (7)
    buyban_lwentcon=((lowerline-5)[-1] <= float(t120['Low'][-1])) and (float(t120['Low'][-1]) <= (lowerline+5)[-1])
    #밴드차트에서 현재의 하단선구간에 저가가 위치해 있는지 확인
    buyban_lwcon=lowerline[-1]-lowerline[-2]>=0
    #밴드차트에서 현재의 하단선이 1봉전 하단선의 값과 동일하거나 더 큰지를 비교 (8)
    buyban_cnupcon=any((upperline[-20:]-list(upperline[-21:-1]))>0)
    #밴드차트에서 20봉 이내에 상단선이 상승한 적이 있는지 확인 (9)
    buyban_cncon=((midline-5)[-1] <= float(t120['Low'][-1]))==(float(t120['Low'][-1]) <= (midline+5)[-1])
    #밴드차트에서 현재의 Low값이 중심선 구간(중심선 가격+-5)에 위치해 있는지 확인 (10)
    buyban_cnlim=all((midline-5)[-15:] <= t120['Low'][-15:].astype(float))
    #밴드차트에서 15봉 이내에 중심선 하단 마지노선을 Low값이 벗어난 적이 있는지를 확인 (11)

    #sell
    sellbb_btw1=round(mt1_2_upper[-1], 2) >= float(m1.iloc[-1]['High']) >= round(mt1_1_upper[-1], 2)
    sellbb_btw3=round(mt3_2_upper[-1], 2) <= float(m3.iloc[-1]['High']) <= round(mt3_1_upper[-1], 2)
    sellbb_1n2cndl1=round(mt1_1_upper[-1], 2) <= round(mt1_1_upper[-2], 2)
    sellbb_2n3cndl1=round(mt1_1_upper[-2], 2) <= round(mt1_1_upper[-3], 2)
    sellbb_1n2cndl3=round(mt3_1_upper[-1], 2) <= round(mt3_1_upper[-2], 2)
    sellbb_2n3cndl3=round(mt3_1_upper[-2], 2) <= round(mt3_1_upper[-3], 2)
    sellma_btw1=round(mt1_0_lower[-1], 2) <= float(m1.iloc[-1]['High']) <= round(mt1_0_upper[-1], 2)
    sellma_btw3=round(mt3_0_lower[-1], 2) <= float(m3.iloc[-1]['High']) <= round(mt3_0_upper[-1], 2)
    sellbb_lwcon1=any((round(mt1_1_lower[-15:],2) >= m1['Low'][-15:].astype(float)))
    sellbb_lwcon3=any((round(mt3_1_lower[-15:],2) >= m3['Low'][-15:].astype(float)))
    sellbb_cnlim1=all((round(mt1_0_upper[-15:],2) >= m1['High'][-15:].astype(float)))
    sellbb_cnlim3=all((round(mt3_0_upper[-15:],2) >= m3['High'][-15:].astype(float)))
    sellban_lwupcon=any(lowerline[-20:].astype(float) == t120['Low'][-20:].astype(float))
    sellban_lwcon=upperline[-1]-upperline[-2]>=0
    sellban_lwentcon=((upperline-5)[-1] <= float(t120['Low'][-1]))==(float(t120['Low'][-1]) <= (upperline+5)[-1])
    sellban_cnupcon=any((lowerline[-21:-1:]-list(lowerline[-20:]))>0)
    sellban_cncon=((midline-5)[-1] <= float(t120['High'][-1])) and (float(t120['High'][-1]) <= (midline+5)[-1])
    sellban_cnlim=all((midline+5)[-15:] >= t120['High'][-15:].astype(float))
    #매수
    #5분
    m5buy=(buybb_btw5_12 and (buybb_1n2cndl5_12 or buybb_2n3cndl5_12)) or \
    (buyma_btw5_12 and buybb_upcon5_12 and buybb_cnlim5_12) or \
    (buybb_btw5_20 and (buybb_1n2cndl5_20 or buybb_2n3cndl5_20)) or \
    (buyma_btw5_20 and buybb_upcon5_20 and buybb_cnlim5_20)
    #10분
    m10buy=(buybb_btw10_12 and (buybb_1n2cndl10_12 or buybb_2n3cndl10_12)) or \
    (buyma_btw10_12 and buybb_upcon10_12 and buybb_cnlim10_12) or \
    (buybb_btw10_20 and (buybb_1n2cndl10_20 or buybb_2n3cndl10_20)) or \
    (buyma_btw10_20 and buybb_upcon10_20 and buybb_cnlim10_20)
    #15분
    m15buy=(buybb_btw15_12 and (buybb_1n2cndl15_12 or buybb_2n3cndl15_12)) or \
    (buyma_btw15_12 and buybb_upcon15_12 and buybb_cnlim15_12) or \
    (buybb_btw15_20 and (buybb_1n2cndl15_20 or buybb_2n3cndl15_20)) or \
    (buyma_btw15_20 and buybb_upcon15_20 and buybb_cnlim15_20)
    #20분
    m20buy=(buybb_btw20_12 and (buybb_1n2cndl20_12 or buybb_2n3cndl20_12)) or \
    (buyma_btw20_12 and buybb_upcon20_12 and buybb_cnlim20_12) or \
    (buybb_btw20_20 and (buybb_1n2cndl20_20 or buybb_2n3cndl20_20)) or \
    (buyma_btw20_20 and buybb_upcon20_20 and buybb_cnlim20_20)
    #30분
    m30buy=(buybb_btw30_12 and (buybb_1n2cndl30_12 or buybb_2n3cndl30_12)) or \
    (buyma_btw30_12 and buybb_upcon30_12 and buybb_cnlim30_12) or \
    (buybb_btw30_20 and (buybb_1n2cndl30_20 or buybb_2n3cndl30_20)) or \
    (buyma_btw30_20 and buybb_upcon30_20 and buybb_cnlim30_20)
    #60분
    m60buy=(buybb_btw60_12 and (buybb_1n2cndl60_12 or buybb_2n3cndl60_12)) or \
    (buyma_btw60_12 and buybb_upcon60_12 and buybb_cnlim60_12) or \
    (buybb_btw60_20 and (buybb_1n2cndl60_20 or buybb_2n3cndl60_20)) or \
    (buyma_btw60_20 and buybb_upcon60_20 and buybb_cnlim60_20)
    #90분
    m90buy=(buybb_btw90_12 and (buybb_1n2cndl90_12 or buybb_2n3cndl90_12)) or \
    (buyma_btw90_12 and buybb_upcon90_12 and buybb_cnlim90_12) or \
    (buybb_btw90_20 and (buybb_1n2cndl90_20 or buybb_2n3cndl90_20)) or \
    (buyma_btw90_20 and buybb_upcon90_20 and buybb_cnlim90_20)
    #120분
    m120buy=(buybb_btw120_12 and (buybb_1n2cndl120_12 or buybb_2n3cndl120_12)) or \
    (buyma_btw120_12 and buybb_upcon120_12 and buybb_cnlim120_12) or \
    (buybb_btw120_20 and (buybb_1n2cndl120_20 or buybb_2n3cndl120_20)) or \
    (buyma_btw120_20 and buybb_upcon120_20 and buybb_cnlim120_20)
    #240분
    m240buy=(buybb_btw240_12 and (buybb_1n2cndl240_12 or buybb_2n3cndl240_12)) or \
    (buyma_btw240_12 and buybb_upcon240_12 and buybb_cnlim240_12) or \
    (buybb_btw240_20 and (buybb_1n2cndl240_20 or buybb_2n3cndl240_20)) or \
    (buyma_btw240_20 and buybb_upcon240_20 and buybb_cnlim240_20)
    #480분
    m480buy=(buybb_btw480_12 and (buybb_1n2cndl480_12 or buybb_2n3cndl480_12)) or \
    (buyma_btw480_12 and buybb_upcon480_12 and buybb_cnlim480_12) or \
    (buybb_btw480_20 and (buybb_1n2cndl480_20 or buybb_2n3cndl480_20)) or \
    (buyma_btw480_20 and buybb_upcon480_20 and buybb_cnlim480_20)
    #960분
    m960buy=(buybb_btw960_12 and (buybb_1n2cndl960_12 or buybb_2n3cndl960_12)) or \
    (buyma_btw960_12 and buybb_upcon960_12 and buybb_cnlim960_12) or \
    (buybb_btw960_20 and (buybb_1n2cndl960_20 or buybb_2n3cndl960_20)) or \
    (buyma_btw960_20 and buybb_upcon960_20 and buybb_cnlim960_20)
    #매도
    #5분
    m5sell=(sellbb_btw5_12 and (sellbb_1n2cndl5_12 or sellbb_2n3cndl5_12)) or \
    (sellma_btw5_12 and sellbb_lwcon5_12 and sellbb_cnlim5_12) or \
    (sellbb_btw5_20 and (sellbb_1n2cndl5_20 or sellbb_2n3cndl5_20)) or \
    (sellma_btw5_20 and sellbb_lwcon5_20 and sellbb_cnlim5_20)
    #10분
    m10sell=(sellbb_btw10_12 and (sellbb_1n2cndl10_12 or sellbb_2n3cndl10_12)) or \
    (sellma_btw10_12 and sellbb_lwcon10_12 and sellbb_cnlim10_12) or \
    (sellbb_btw10_20 and (sellbb_1n2cndl10_20 or sellbb_2n3cndl10_20)) or \
    (sellma_btw10_20 and sellbb_lwcon10_20 and sellbb_cnlim10_20)
    #15분
    m15sell=(sellbb_btw15_12 and (sellbb_1n2cndl15_12 or sellbb_2n3cndl15_12)) or \
    (sellma_btw15_12 and sellbb_lwcon15_12 and sellbb_cnlim15_12) or \
    (sellbb_btw15_20 and (sellbb_1n2cndl15_20 or sellbb_2n3cndl15_20)) or \
    (sellma_btw15_20 and sellbb_lwcon15_20 and sellbb_cnlim15_20)
    #20분
    m20sell=(sellbb_btw20_12 and (sellbb_1n2cndl20_12 or sellbb_2n3cndl20_12)) or \
    (sellma_btw20_12 and sellbb_lwcon20_12 and sellbb_cnlim20_12) or \
    (sellbb_btw20_20 and (sellbb_1n2cndl20_20 or sellbb_2n3cndl20_20)) or \
    (sellma_btw20_20 and sellbb_lwcon20_20 and sellbb_cnlim20_20)
    #30분
    m30sell=(sellbb_btw30_12 and (sellbb_1n2cndl30_12 or sellbb_2n3cndl30_12)) or \
    (sellma_btw30_12 and sellbb_lwcon30_12 and sellbb_cnlim30_12) or \
    (sellbb_btw30_20 and (sellbb_1n2cndl30_20 or sellbb_2n3cndl30_20)) or \
    (sellma_btw30_20 and sellbb_lwcon30_20 and sellbb_cnlim30_20)
    #60분
    m60sell=(sellbb_btw60_12 and (sellbb_1n2cndl60_12 or sellbb_2n3cndl60_12)) or \
    (sellma_btw60_12 and sellbb_lwcon60_12 and sellbb_cnlim60_12) or \
    (sellbb_btw60_20 and (sellbb_1n2cndl60_20 or sellbb_2n3cndl60_20)) or \
    (sellma_btw60_20 and sellbb_lwcon60_20 and sellbb_cnlim60_20)
    #90분
    m90sell=(sellbb_btw90_12 and (sellbb_1n2cndl90_12 or sellbb_2n3cndl90_12)) or \
    (sellma_btw90_12 and sellbb_lwcon90_12 and sellbb_cnlim90_12) or \
    (sellbb_btw90_20 and (sellbb_1n2cndl90_20 or sellbb_2n3cndl90_20)) or \
    (sellma_btw90_20 and sellbb_lwcon90_20 and sellbb_cnlim90_20)
    #120분
    m120sell=(sellbb_btw120_12 and (sellbb_1n2cndl120_12 or sellbb_2n3cndl120_12)) or \
    (sellma_btw120_12 and sellbb_lwcon120_12 and sellbb_cnlim120_12) or \
    (sellbb_btw120_20 and (sellbb_1n2cndl120_20 or sellbb_2n3cndl120_20)) or \
    (sellma_btw120_20 and sellbb_lwcon120_20 and sellbb_cnlim120_20)
    #240분
    m240sell=(sellbb_btw240_12 and (sellbb_1n2cndl240_12 or sellbb_2n3cndl240_12)) or \
    (sellma_btw240_12 and sellbb_lwcon240_12 and sellbb_cnlim240_12) or \
    (sellbb_btw240_20 and (sellbb_1n2cndl240_20 or sellbb_2n3cndl240_20)) or \
    (sellma_btw240_20 and sellbb_lwcon240_20 and sellbb_cnlim240_20)
    #480분
    m480sell=(sellbb_btw480_12 and (sellbb_1n2cndl480_12 or sellbb_2n3cndl480_12)) or \
    (sellma_btw480_12 and sellbb_lwcon480_12 and sellbb_cnlim480_12) or \
    (sellbb_btw480_20 and (sellbb_1n2cndl480_20 or sellbb_2n3cndl480_20)) or \
    (sellma_btw480_20 and sellbb_lwcon480_20 and sellbb_cnlim480_20)
    #960분
    m960sell=(sellbb_btw960_12 and (sellbb_1n2cndl960_12 or sellbb_2n3cndl960_12)) or \
    (sellma_btw960_12 and sellbb_lwcon960_12 and sellbb_cnlim960_12) or \
    (sellbb_btw960_20 and (sellbb_1n2cndl960_20 or sellbb_2n3cndl960_20)) or \
    (sellma_btw960_20 and sellbb_lwcon960_20 and sellbb_cnlim960_20)
    #기준선 조건 (매수)
    buy_limit=[b-30 for b in buy]
    buy_limit_con=[float(buy_limit[f]) <= float(mt1.iloc[-1]['Low']) <=float(buy[f]) for f in range(len(buy_limit))] 
    #기준선 조건 (매도)
    sell_limit=[b+30 for b in sell]
    sell_limit_con=[float(sell[f]) <= float(mt1.iloc[-1]['High']) <=float(sell_limit[f]) for f in range(len(sell_limit))]


    #추세판별
    short_trend=mt1['Close'].rolling(window=20).mean()
    long_trend=mt1['Close'].rolling(window=60).mean()
    if states==1 or states==0 or states==-1:
        #Case A 매수조건
        if ((m5buy or m10buy or m15buy or m20buy or m30buy or m60buy or m90buy or m120buy or m240buy or m480buy or m960buy) and \
            any(buy_limit_con))==True:
            hsi_cur=float(t120['Close'][-1]) # 매수 시점의 가격을 언제든지 불러올 수 있도록 변수에 넣어서 저장 *상태메세지와 비교 대조하며 작동상황을 확인하기 위해 작성
            states=5                         
            pyautogui.click(x=3319, y=568, duration=0.1) # 혹시 걸려있을 mit나 지정가 취소 X3
            pyautogui.click(x=3560, y=612, duration=0.1) 
            pyautogui.click(x=3560, y=612, duration=0.1)                
            pyautogui.click(x=3265, y=137, duration=0.2) # {매수수량 2개로 설정
            pyautogui.click(x=3530, y=328, duration=0.2) # 매수버튼 클릭}                       
            # **상태메세지를 매수일 때로 변경(상태메세지 : 5로 변경)                 
            pyperclip.copy("Case A 매수신호 발생. 매수진입 \n\n" +
            '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
            '\n'+'현재상태 : '+str(states)+
            '\n' +'현재가격 : '+t120['Close'][-1]+
            '\n'+'진입방향 : 상방')
            pyautogui.click(x=1982, y=340)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter')                
            # 매수 상태 및 가격, 현재 시간 등을 어딘가에 기록(상태메세지 : Case A 매수신호 발생. 매수진입)
        #Case A 매도조건
        elif ((m5sell or m10sell or m15sell or m20sell or m30sell or m60sell or m90sell or m120sell or m240sell or m480sell or m960sell) and \
            any(sell_limit_con))==True:
            states=-5 # **상태메세지를 매도일 때로 변경(상태메세지 : -5로 변경)
            hsi_cur=float(t120['Close'][-1]) # 매도 시점의 가격을 언제든지 불러올 수 있도록 변수에 넣어서 저장 *상태메세지와 비교 대조하며 작동상황을 확인하기 위해 작성
            pyautogui.click(x=3319, y=568, duration=0.1) # 혹시 걸려있을 mit나 지정가 취소 X3
            pyautogui.click(x=3560, y=612, duration=0.1) 
            pyautogui.click(x=3560, y=612, duration=0.1)                
            pyautogui.click(x=3265, y=137, duration=0.2) # {매수수량 2개로 설정
            pyautogui.click(x=3187, y=413, duration=0.02) # 매도버튼 클릭}                        
            # 매도 상태 및 가격, 현재 시간 등을 어딘가에 기록(상태메세지 : Case A 매도신호 발생. 매도진입)
            pyperclip.copy("Case A 매도신호 발생. 매도진입 \n\n" +
            '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
            '\n'+'현재상태 : '+str(states)+
            '\n' +'현재가격 : '+t120['Close'][-1]+
            '\n'+'진입방향 : 하방')
            pyautogui.click(x=1982, y=340)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter')   
        elif (short_trend[-1]>=long_trend[-1]) == True:
            #정배열
            states=1
            #Case D 매수조건       
            if (((buybb_btw1 and (buybb_1n2cndl1 or buybb_2n3cndl1)) or \
            (buybb_btw3 and (buybb_1n2cndl3 or buybb_2n3cndl3))) or \
            ((buyma_btw1 and buybb_upcon1 and buybb_cnlim1) or \
            (buyma_btw3 and buybb_upcon3 and buybb_cnlim3))) and \
            ((buyban_lwupcon and buyban_lwcon and buyban_lwentcon) or \
            (buyban_cnupcon and buyban_cncon and buyban_cnlim)) == True:
                states=3 # **상태메세지를 매수일 때로 변경(상태메세지 : 3으로 변경)              
                hsi_cur=float(t120['Close'][-1]) # 매수 시점의 가격을 언제든지 불러올 수 있도록 변수에 넣어서 저장 *상태메세지와 비교 대조하며 작동상황을 확인하기 위해 작성
                pyautogui.click(x=3319, y=568, duration=0.1) # 혹시 걸려있을 mit나 지정가 취소 X3
                pyautogui.click(x=3560, y=612, duration=0.1) 
                pyautogui.click(x=3560, y=612, duration=0.1)                
                pyautogui.click(x=3265, y=137, duration=0.2) # {매수수량 2개로 설정
                pyautogui.click(x=3530, y=328, duration=0.02) # 매수버튼 클릭}                    
                # 매수 상태 및 가격, 현재 시간 등을 어딘가에 기록(상태메세지 : Case D 매수신호 발생. 매수진입)
                pyperclip.copy("Case D 매수신호 발생. 매수진입 \n\n" +
                '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
                '\n'+'현재상태 : '+str(states)+
                '\n' +'현재가격 : '+t120['Close'][-1]+
                '\n'+'진입방향 : 상방')
                pyautogui.click(x=1982, y=340)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.hotkey('enter') 
            else:
                pass    
        elif (long_trend[-1]>short_trend[-1])==True:
            #역배열
            states=-1 
            #Case D 매도조건   
            if (((sellbb_btw1 and (sellbb_1n2cndl1 or sellbb_2n3cndl1)) or \
            (sellbb_btw3 and (sellbb_1n2cndl3 or sellbb_2n3cndl3))) or \
            ((sellma_btw1 and sellbb_lwcon1 and sellbb_cnlim1) or \
            (sellma_btw3 and sellbb_lwcon3 and sellbb_cnlim3))) and \
            ((sellban_lwupcon and sellban_lwcon and sellban_lwentcon) or \
            (sellban_cnupcon and sellban_cncon and sellban_cnlim)) == True:
                states=-3 # **상태메세지를 매도일 때로 변경(상태메세지 : -3으로 변경)
                hsi_cur=float(t120['Close'][-1]) # 매도 시점의 가격을 언제든지 불러올 수 있도록 변수에 넣어서 저장 *상태메세지와 비교 대조하며 작동상황을 확인하기 위해 작성
                pyautogui.click(x=3319, y=568, duration=0.1) # 혹시 걸려있을 mit나 지정가 취소 X3
                pyautogui.click(x=3560, y=612, duration=0.1) 
                pyautogui.click(x=3560, y=612, duration=0.1)                
                pyautogui.click(x=3265, y=137, duration=0.2) # {매수수량 2개로 설정
                pyautogui.click(x=3187, y=413, duration=0.02) # 매도버튼 클릭}                 
                # 매도 상태 및 가격, 현재 시간 등을 어딘가에 기록(상태메세지 : Case D 매도신호 발생. 매도진입)
                pyperclip.copy("Case D 매도신호 발생. 매도진입 \n\n" +
                '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
                '\n'+'현재상태 : '+str(states)+
                '\n' +'현재가격 : '+t120['Close'][-1]+
                '\n'+'진입방향 : 하방')
                pyautogui.click(x=1982, y=340)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.hotkey('enter') 
            else:
                pass             
        else:
            pass               
    elif states==3 or states==5:            
        if ((m5sell or m10sell or m15sell or m20sell or m30sell or m60sell or m90sell or m120sell or m240sell or m480sell or m960sell) and \
        any(sell_limit_con)) and (t120['High'][-1] >= hsi_cur+35) ==True:
            pyautogui.click(x=3316, y=166, duration=0.2) # Case A 매도로 올청산버튼 실행
            pyautogui.press('enter')  
            pyautogui.click(x=3319, y=568, duration=0.1) # 혹시 걸려있을 mit나 지정가 취소 X3
            pyautogui.click(x=3560, y=612, duration=0.1) 
            pyautogui.click(x=3560, y=612, duration=0.1)             
            states = 0 # **상태메세지를 0 으로 변경
            # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : Case A 반대매도신호 발생(수량2). 올청산)
            pyperclip.copy("Case A 반대매도신호 발생(수량2). 올청산 \n\n" +
            '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
            '\n'+'현재상태 : '+str(states)+
            '\n' +'현재가격 : '+t120['Close'][-1])
            pyautogui.click(x=1982, y=340)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter')                               
        #수익이 60틱(Hangseng)을 초과하는지 확인 (진입가격기준 + 60을 해서 고가가 이보다 크다는 것을 확인.(1분봉정도의 분봉으로 구간(3)고가 확인))
        elif (t120['High'].rolling(window=1).max()[-1] >= hsi_cur+65)==True:                
            # 수량을 1개로 변경 
            pyautogui.click(x=3245, y=135, duration=0.2)
            # 시장가로 매도청산
            pyautogui.click(x=3187, y=413, duration=0.02) 
            # **수량이 하나 작아졌다는 표시로 상태메세지에 기록((상태메세지를 Case A면 4로, Case D면 2로) 변경)
            if states==5:
                states=4
                # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : (5면 Case A, 3이면 Case D) 1차수익청산지점 도달. 1단위 수량 매도청산)
                pyperclip.copy("Case A 1차수익청산지점 도달. 1단위 수량 매도청산 \n\n" +
                '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
                '\n'+'현재상태 : '+str(states)+
                '\n' +'현재가격 : '+t120['Close'][-1]+
                '\n'+'진입방향 : 상방')
                pyautogui.click(x=1982, y=340)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.hotkey('enter')
            elif states==3:
                states=2
                # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : (5면 Case A, 3이면 Case D) 1차수익청산지점 도달. 1단위 수량 매도청산)
                pyperclip.copy("Case D 1차수익청산지점 도달. 1단위 수량 매도청산 \n\n" +
                '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
                '\n'+'현재상태 : '+str(states)+
                '\n' +'현재가격 : '+t120['Close'][-1]+
                '\n'+'진입방향 : 상방')
                pyautogui.click(x=1982, y=340)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.hotkey('enter')
            else:
                pass
        # 손절 틱수에 도달한지를 파악 (1분봉 정도의 분봉으로 구간(10)저가 확인. 항셍의 경우 손절 30틱이므로 진입가격 기준 -30인지 확인.)                
        elif (mt1['Low'].rolling(window=10).min()[-1] <= hsi_cur-27) ==True:                 
            # **상태메세지에 기록(상태메세지를 0으로 변경)
            states=0
            # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : 손절)
            pyperclip.copy("손절 \n\n" +
            '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
            '\n'+'현재상태 : '+str(states)+
            '\n' +'현재가격 : '+t120['Close'][-1])
            pyautogui.click(x=1982, y=340)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter')   
        else:
            pass             
    elif states==2 or states==4:
        if (((m5sell or m10sell or m15sell or m20sell or m30sell or m60sell or m90sell or m120sell or m240sell or m480sell or m960sell) and \
        any(sell_limit_con)) and (t120['High'][-1] >= hsi_cur+35)) == True:
            pyautogui.click(x=3316, y=166, duration=0.2) # Case A 매도로 올청산버튼 실행
            pyautogui.press('enter')  
            pyautogui.click(x=3319, y=568, duration=0.1) # 혹시 걸려있을 mit나 지정가 취소 X3
            pyautogui.click(x=3560, y=612, duration=0.1) 
            pyautogui.click(x=3560, y=612, duration=0.1)            
            states = 0 # **상태메세지를 0 으로 변경
            # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : Case A 반대매도신호 발생(수량1). 올청산)
            pyperclip.copy("Case A 반대매도신호 발생(수량1). 올청산 \n\n" +
            '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
            '\n'+'현재상태 : '+str(states)+
            '\n' +'현재가격 : '+t120['Close'][-1])
            pyautogui.click(x=1982, y=340)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter') 
    
        #볼린저밴드 1분봉 상단선이 닫힌 지점을 현재가가 도달했을 경우
        elif ((round(mt1_1_upper[-1], 2) <= round(mt1_1_upper[-2], 2)) and (float(m1.iloc[-1]['High']) >= round(mt1_1_upper[-1], 2)))==True:
            # 매도로 올청산버튼 실행
            pyautogui.click(x=3316, y=166, duration=0.2)
            pyautogui.press('enter')  
            pyautogui.click(x=3319, y=568, duration=0.1) # 혹시 걸려있을 mit나 지정가 취소 X3
            pyautogui.click(x=3560, y=612, duration=0.1) 
            pyautogui.click(x=3560, y=612, duration=0.1)             
            states = 0 # **상태메세지를 0 으로 변경
            # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : Case A 반대매도신호 발생(수량1). 올청산)
            pyperclip.copy("현재 1분 상단선 매도신호발생. 올청산 \n\n" +
            '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
            '\n'+'현재상태 : '+str(states)+
            '\n' +'현재가격 : '+t120['Close'][-1])
            pyautogui.click(x=1982, y=340)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter') 
        #볼린저밴드 1분봉 하단선을 벗어난 지점에 현재가가 도달했을 경우       
        elif (mt1_2_lower.rolling(window=20).max()[-1] > m1.rolling(window=5).min().iloc[-1]['Low'])== True: 
            # 매도로 올청산버튼 실행
            pyautogui.click(x=3316, y=166, duration=0.2)
            pyautogui.press('enter')  
            pyautogui.click(x=3319, y=568, duration=0.1) # 혹시 걸려있을 mit나 지정가 취소 X3
            pyautogui.click(x=3560, y=612, duration=0.1) 
            pyautogui.click(x=3560, y=612, duration=0.1)             
            states = 0 # **상태메세지를 0 으로 변경
            # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : 현재 1분봉 하단선 이탈. 매도로 올청산)
            pyperclip.copy("현재 1분봉 하단선 이탈. 매도로 올청산 \n\n" +
            '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
            '\n'+'현재상태 : '+str(states)+
            '\n' +'현재가격 : '+t120['Close'][-1])
            pyautogui.click(x=1982, y=340)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter')                 
        #진입가 기준 120틱 봉(3봉전~0봉전) 저점이 3틱 위에 있을 경우
        elif (t120['Low'].rolling(window=3).min()[-1] <= hsi_cur+3)==True:
            # 매도로 올청산버튼 실행
            pyautogui.click(x=3316, y=166, duration=0.2) 
            pyautogui.press('enter')  
            pyautogui.click(x=3319, y=568, duration=0.1) # 혹시 걸려있을 mit나 지정가 취소 X3
            pyautogui.click(x=3560, y=612, duration=0.1) 
            pyautogui.click(x=3560, y=612, duration=0.1)             
            states = 0 # **상태메세지를 0 으로 변경
            # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : 현재가, 진입가 부근 접근. 매도로 올청산)
            pyperclip.copy("현재가, 진입가 부근 접근. 매도로 올청산 \n\n" +
            '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
            '\n'+'현재상태 : '+str(states)+
            '\n' +'현재가격 : '+t120['Close'][-1])
            pyautogui.click(x=1982, y=340)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter')             
        else:
            pass 
    elif states==-3 or states==-5 :
        if (((m5buy or m10buy or m15buy or m20buy or m30buy or m60buy or m90buy or m120buy or m240buy or m480buy or m960buy) and \
        any(buy_limit_con)) and (t120['Low'][-1] <= hsi_cur-35)) ==True:
            #매수로 올청산버튼 실행
            pyautogui.click(x=3316, y=166, duration=0.2)
            pyautogui.press('enter')  
            pyautogui.click(x=3319, y=568, duration=0.1) # 혹시 걸려있을 mit나 지정가 취소 X3
            pyautogui.click(x=3560, y=612, duration=0.1) 
            pyautogui.click(x=3560, y=612, duration=0.1)               
            states = 0 # **상태메세지를 0 으로 변경
            # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : Case A 반대매수신호 발생(수량2). 올청산)
            pyperclip.copy("Case A 반대매수신호 발생(수량2). 올청산 \n\n" +
            '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
            '\n'+'현재상태 : '+str(states)+
            '\n' +'현재가격 : '+t120['Close'][-1])
            pyautogui.click(x=1982, y=340)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter')
        #수익이 60틱(Hangseng)을 초과하는지 확인 (진입가격기준 - 60을 해서 저가가 이보다 작다는 것을 확인.(1분봉정도의 분봉으로 구간(3)저가 확인))                                        
        elif  (t120['Low'].rolling(window=1).min()[-1] <= hsi_cur-65)==True:
            # 수량을 1개로 변경 
            pyautogui.click(x=3245, y=135, duration=0.2)
            # 시장가로 매수청산
            pyautogui.click(x=3530, y=328, duration=0.2)
            # **수량이 하나 작아졌다는 표시로 상태메세지에 기록((상태메세지를 Case A면 4로, Case D면 2로) 변경)
            if states==-5:
                states=-4
                # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : (-5면 Case A, -3이면 Case D) 1차수익청산지점 도달. 1단위 수량 매수청산)
                pyperclip.copy("Case A 1차수익청산지점 도달. 1단위 수량 매수청산 \n\n" +
                '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
                '\n'+'현재상태 : '+str(states)+
                '\n' +'현재가격 : '+t120['Close'][-1]+
                '\n'+'진입방향 : 하방')
                pyautogui.click(x=1982, y=340)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.hotkey('enter')
            elif states==-3:
                states=-2
                # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : (5면 Case A, 3이면 Case D) 1차수익청산지점 도달. 1단위 수량 매수청산)
                pyperclip.copy("Case D 1차수익청산지점 도달. 1단위 수량 매도청산 \n\n" +
                '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
                '\n'+'현재상태 : '+str(states)+
                '\n' +'현재가격 : '+t120['Close'][-1]+
                '\n'+'진입방향 : 하방')
                pyautogui.click(x=1982, y=340)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.hotkey('enter')
            else:
                pass
        # 손절 틱수에 도달한지를 파악 (1분봉 정도의 분봉으로 구간(10)고가 확인. 항셍의 경우 손절 30틱이므로 진입가격 기준 +30인지 확인.)                
        elif (mt1['High'].rolling(window=10).max()[-1] >= hsi_cur+27) ==True:                 
            # **상태메세지에 기록(상태메세지를 0으로 변경)
            states=0
            # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : 손절)
            pyperclip.copy("손절 \n\n" +
            '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
            '\n'+'현재상태 : '+str(states)+
            '\n' +'현재가격 : '+t120['Close'][-1])
            pyautogui.click(x=1982, y=340)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter')   
        else:
            pass                                 
    elif states==-2 or states==-4:
        if (((m5buy or m10buy or m15buy or m20buy or m30buy or m60buy or m90buy or m120buy or m240buy or m480buy or m960buy) and \
        any(buy_limit_con)) and (t120['Low'][-1] <= hsi_cur-35)) ==True:
            #매수로 올청산 버튼 실행
            pyautogui.click(x=3316, y=166, duration=0.2)
            pyautogui.press('enter')  
            pyautogui.click(x=3319, y=568, duration=0.1) # 혹시 걸려있을 mit나 지정가 취소 X3
            pyautogui.click(x=3560, y=612, duration=0.1) 
            pyautogui.click(x=3560, y=612, duration=0.1)            
            states = 0 # **상태메세지를 0 으로 변경
            # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : Case A 반대매수신호 발생(수량1). 올청산)
            pyperclip.copy("Case A 반대매수신호 발생(수량1). 올청산 \n\n" +
            '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
            '\n'+'현재상태 : '+str(states)+
            '\n' +'현재가격 : '+t120['Close'][-1])
            pyautogui.click(x=1982, y=340)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter') 
    
        #볼린저밴드 1분봉 하단선이 닫힌 지점을 현재가가 도달했을 경우
        elif ((round(mt1_1_lower[-1], 2) >= round(mt1_1_lower[-2], 2)) and (float(m1.iloc[-1]['Low']) <= round(mt1_1_lower[-1], 2)))==True:
            # 매도로 올청산버튼 실행
            pyautogui.click(x=3316, y=166, duration=0.2)
            pyautogui.press('enter')  
            pyautogui.click(x=3319, y=568, duration=0.1) # 혹시 걸려있을 mit나 지정가 취소 X3
            pyautogui.click(x=3560, y=612, duration=0.1) 
            pyautogui.click(x=3560, y=612, duration=0.1)              
            states = 0 # **상태메세지를 0 으로 변경
            # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : Case A 반대매수신호 발생(수량1). 올청산)
            pyperclip.copy("현재 1분 하단선 매수신호발생. 올청산 \n\n" +
            '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
            '\n'+'현재상태 : '+str(states)+
            '\n' +'현재가격 : '+t120['Close'][-1])
            pyautogui.click(x=1982, y=340)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter') 
        #볼린저밴드 1분봉 상단선을 벗어난 지점에 현재가가 도달했을 경우       
        elif (mt1_2_upper.rolling(window=20).min()[-1] < m1.rolling(window=5).max().iloc[-1]['High'])== True: 
            # 매수로 올청산버튼 실행
            pyautogui.click(x=3316, y=166, duration=0.2)
            pyautogui.press('enter')  
            pyautogui.click(x=3319, y=568, duration=0.1) # 혹시 걸려있을 mit나 지정가 취소 X3
            pyautogui.click(x=3560, y=612, duration=0.1) 
            pyautogui.click(x=3560, y=612, duration=0.1)                 
            states = 0 # **상태메세지를 0 으로 변경
            # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : 현재 1분봉 상단선 이탈. 매수로 올청산)
            pyperclip.copy("현재 1분봉 상단선 이탈. 매수로 올청산 \n\n" +
            '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
            '\n'+'현재상태 : '+str(states)+
            '\n' +'현재가격 : '+t120['Close'][-1])
            pyautogui.click(x=1982, y=340)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter')                 
        #진입가 기준 120틱 봉(3봉전~0봉전) 고점이 3틱 위에 있을 경우
        elif (t120['High'].rolling(window=3).max()[-1] >= hsi_cur-3)==True:
            # 매수로 올청산버튼 실행
            pyautogui.click(x=3316, y=166, duration=0.2)
            pyautogui.press('enter')  
            pyautogui.click(x=3319, y=568, duration=0.1) # 혹시 걸려있을 mit나 지정가 취소 X3
            pyautogui.click(x=3560, y=612, duration=0.1) 
            pyautogui.click(x=3560, y=612, duration=0.1)               
            states = 0 # **상태메세지를 0 으로 변경
            # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : 현재가, 진입가 부근 접근. 매수로 올청산)
            pyperclip.copy("현재가, 진입가 부근 접근. 매수로 올청산 \n\n" +
            '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
            '\n'+'현재상태 : '+str(states)+
            '\n' +'현재가격 : '+t120['Close'][-1])
            pyautogui.click(x=1982, y=340)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter')             
        else:
            pass 
    else:
        pass                    


    #매도
    #3분
    print(((sellbb_btw5_12 and (sellbb_1n2cndl5_12 or sellbb_2n3cndl5_12)) or \
    (sellma_btw5_12 and sellbb_lwcon5_12 and sellbb_cnlim5_12) or \
    (sellbb_btw5_12 and (sellbb_1n2cndl5_12 or sellbb_2n3cndl5_12)) or \
    (sellma_btw5_12 and sellbb_lwcon5_12 and sellbb_cnlim5_12)),
    ((sellbb_btw10_12 and (sellbb_1n2cndl10_12 or sellbb_2n3cndl10_12)) or \
    (sellma_btw10_12 and sellbb_lwcon10_12 and sellbb_cnlim10_12) or \
    (sellbb_btw10_12 and (sellbb_1n2cndl10_12 or sellbb_2n3cndl10_12)) or \
    (sellma_btw10_12 and sellbb_lwcon10_12 and sellbb_cnlim10_12)),
    ((sellbb_btw15_12 and (sellbb_1n2cndl15_12 or sellbb_2n3cndl15_12)) or \
    (sellma_btw15_12 and sellbb_lwcon15_12 and sellbb_cnlim15_12) or \
    (sellbb_btw15_12 and (sellbb_1n2cndl15_12 or sellbb_2n3cndl15_12)) or \
    (sellma_btw15_12 and sellbb_lwcon15_12 and sellbb_cnlim15_12)),
    ((sellbb_btw20_12 and (sellbb_1n2cndl20_12 or sellbb_2n3cndl20_12)) or \
    (sellma_btw20_12 and sellbb_lwcon20_12 and sellbb_cnlim20_12) or \
    (sellbb_btw20_12 and (sellbb_1n2cndl20_12 or sellbb_2n3cndl20_12)) or \
    (sellma_btw20_12 and sellbb_lwcon20_12 and sellbb_cnlim20_12)),
    ((sellbb_btw30_12 and (sellbb_1n2cndl30_12 or sellbb_2n3cndl30_12)) or \
    (sellma_btw30_12 and sellbb_lwcon30_12 and sellbb_cnlim30_12) or \
    (sellbb_btw30_12 and (sellbb_1n2cndl30_12 or sellbb_2n3cndl30_12)) or \
    (sellma_btw30_12 and sellbb_lwcon30_12 and sellbb_cnlim30_12)),
    ((sellbb_btw60_12 and (sellbb_1n2cndl60_12 or sellbb_2n3cndl60_12)) or \
    (sellma_btw60_12 and sellbb_lwcon60_12 and sellbb_cnlim60_12) or \
    (sellbb_btw60_12 and (sellbb_1n2cndl60_12 or sellbb_2n3cndl60_12)) or \
    (sellma_btw60_12 and sellbb_lwcon60_12 and sellbb_cnlim60_12)),
    ((sellbb_btw90_12 and (sellbb_1n2cndl90_12 or sellbb_2n3cndl90_12)) or \
    (sellma_btw90_12 and sellbb_lwcon90_12 and sellbb_cnlim90_12) or \
    (sellbb_btw90_12 and (sellbb_1n2cndl90_12 or sellbb_2n3cndl90_12)) or \
    (sellma_btw90_12 and sellbb_lwcon90_12 and sellbb_cnlim90_12)),
    ((sellbb_btw120_12 and (sellbb_1n2cndl120_12 or sellbb_2n3cndl120_12)) or \
    (sellma_btw120_12 and sellbb_lwcon120_12 and sellbb_cnlim120_12) or \
    (sellbb_btw120_12 and (sellbb_1n2cndl120_12 or sellbb_2n3cndl120_12)) or \
    (sellma_btw120_12 and sellbb_lwcon120_12 and sellbb_cnlim120_12)),
    ((sellbb_btw240_12 and (sellbb_1n2cndl240_12 or sellbb_2n3cndl240_12)) or \
    (sellma_btw240_12 and sellbb_lwcon240_12 and sellbb_cnlim240_12) or \
    (sellbb_btw240_12 and (sellbb_1n2cndl240_12 or sellbb_2n3cndl240_12)) or \
    (sellma_btw240_12 and sellbb_lwcon240_12 and sellbb_cnlim240_12)),
    ((sellbb_btw480_12 and (sellbb_1n2cndl480_12 or sellbb_2n3cndl480_12)) or \
    (sellma_btw480_12 and sellbb_lwcon480_12 and sellbb_cnlim480_12) or \
    (sellbb_btw480_12 and (sellbb_1n2cndl480_12 or sellbb_2n3cndl480_12)) or \
    (sellma_btw480_12 and sellbb_lwcon480_12 and sellbb_cnlim480_12)),
    ((sellbb_btw960_12 and (sellbb_1n2cndl960_12 or sellbb_2n3cndl960_12)) or \
    (sellma_btw960_12 and sellbb_lwcon960_12 and sellbb_cnlim960_12) or \
    (sellbb_btw960_12 and (sellbb_1n2cndl960_12 or sellbb_2n3cndl960_12)) or \
    (sellma_btw960_12 and sellbb_lwcon960_12 and sellbb_cnlim960_12)))
    print("매도 5분, 10분, 15분, 20분, 30분, 60분, 90분, 120분, 240분, 480분, 960분 \n")
    #매수
    print(((buybb_btw5_12 and (buybb_1n2cndl5_12 or buybb_2n3cndl5_12)) or \
    (buyma_btw5_12 and buybb_upcon5_12 and buybb_cnlim5_12) or \
    (buybb_btw5_20 and (buybb_1n2cndl5_20 or buybb_2n3cndl5_20)) or \
    (buyma_btw5_20 and buybb_upcon5_20 and buybb_cnlim5_20)),
    
    ((buybb_btw10_12 and (buybb_1n2cndl10_12 or buybb_2n3cndl10_12)) or \
    (buyma_btw10_12 and buybb_upcon10_12 and buybb_cnlim10_12) or \
    (buybb_btw10_20 and (buybb_1n2cndl10_20 or buybb_2n3cndl10_20)) or \
    (buyma_btw10_20 and buybb_upcon10_20 and buybb_cnlim10_20)),
    ((buybb_btw15_12 and (buybb_1n2cndl15_12 or buybb_2n3cndl15_12)) or \
    (buyma_btw15_12 and buybb_upcon15_12 and buybb_cnlim15_12) or \
    (buybb_btw15_20 and (buybb_1n2cndl15_20 or buybb_2n3cndl15_20)) or \
    (buyma_btw15_20 and buybb_upcon15_20 and buybb_cnlim15_20)),
    ((buybb_btw20_12 and (buybb_1n2cndl20_12 or buybb_2n3cndl20_12)) or \
    (buyma_btw20_12 and buybb_upcon20_12 and buybb_cnlim20_12) or \
    (buybb_btw20_20 and (buybb_1n2cndl20_20 or buybb_2n3cndl20_20)) or \
    (buyma_btw20_20 and buybb_upcon20_20 and buybb_cnlim20_20)),
    ((buybb_btw30_12 and (buybb_1n2cndl30_12 or buybb_2n3cndl30_12)) or \
    (buyma_btw30_12 and buybb_upcon30_12 and buybb_cnlim30_12) or \
    (buybb_btw30_20 and (buybb_1n2cndl30_20 or buybb_2n3cndl30_20)) or \
    (buyma_btw30_20 and buybb_upcon30_20 and buybb_cnlim30_20)),
    ((buybb_btw60_12 and (buybb_1n2cndl60_12 or buybb_2n3cndl60_12)) or \
    (buyma_btw60_12 and buybb_upcon60_12 and buybb_cnlim60_12) or \
    (buybb_btw60_20 and (buybb_1n2cndl60_20 or buybb_2n3cndl60_20)) or \
    (buyma_btw60_20 and buybb_upcon60_20 and buybb_cnlim60_20)),
    ((buybb_btw90_12 and (buybb_1n2cndl90_12 or buybb_2n3cndl90_12)) or \
    (buyma_btw90_12 and buybb_upcon90_12 and buybb_cnlim90_12) or \
    (buybb_btw90_20 and (buybb_1n2cndl90_20 or buybb_2n3cndl90_20)) or \
    (buyma_btw90_20 and buybb_upcon90_20 and buybb_cnlim90_20)),
    ((buybb_btw120_12 and (buybb_1n2cndl120_12 or buybb_2n3cndl120_12)) or \
    (buyma_btw120_12 and buybb_upcon120_12 and buybb_cnlim120_12) or \
    (buybb_btw120_20 and (buybb_1n2cndl120_20 or buybb_2n3cndl120_20)) or \
    (buyma_btw120_20 and buybb_upcon120_20 and buybb_cnlim120_20)),
    
    ((buybb_btw240_12 and (buybb_1n2cndl240_12 or buybb_2n3cndl240_12)) or \
    (buyma_btw240_12 and buybb_upcon240_12 and buybb_cnlim240_12) or \
    (buybb_btw240_20 and (buybb_1n2cndl240_20 or buybb_2n3cndl240_20)) or \
    (buyma_btw240_20 and buybb_upcon240_20 and buybb_cnlim240_20)),
    ((buybb_btw480_12 and (buybb_1n2cndl480_12 or buybb_2n3cndl480_12)) or \
    (buyma_btw480_12 and buybb_upcon480_12 and buybb_cnlim480_12) or \
    (buybb_btw480_20 and (buybb_1n2cndl480_20 or buybb_2n3cndl480_20)) or \
    (buyma_btw480_20 and buybb_upcon480_20 and buybb_cnlim480_20)),
    
    ((buybb_btw960_12 and (buybb_1n2cndl960_12 or buybb_2n3cndl960_12)) or \
    (buyma_btw960_12 and buybb_upcon960_12 and buybb_cnlim960_12) or \
    (buybb_btw960_20 and (buybb_1n2cndl960_20 or buybb_2n3cndl960_20)) or \
    (buyma_btw960_20 and buybb_upcon960_20 and buybb_cnlim960_20)))
    print("매수 5분, 10분, 15분, 20분, 30분, 60분, 90분, 120분, 240분, 480분, 960분 \n")
    print(buy, "\n Round Figure. Buy limit line \n")
    print(buy_limit_con, "\n Round Figure Buy condition \n")
    print(sell, "\n Round Figure. Sell limit line \n")
    print(sell_limit_con, "\n Round Figure Sell condition \n")
    print("tick high: "+ t120["High"][-1])
    print(t120["Close"][-2:], "tick close")
    print("condition end")
    print(mt1.iloc[-1]['Close'], "1min")
    print(mt5.iloc[-1]['Close'], "5min")
    print(mt3.iloc[-1], "3min")    
    print(mt960.iloc[-1], "960min")
    print(t120.iloc[-1])
    print("\n", hsi_cur, "\n")
    print("\n 현재상태 : ", states, "\n")
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
