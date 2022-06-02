'''
로직 설명 : 
타점 > 
-960틱 CCI 과매도와 과매수를 벗어난 지점
-1분봉 3분봉 5분봉 볼린저밴드 닫힌지점 및 중심선 도달 지점 
'''



import win32com.client
import pythoncom
import pandas as pd 
import numpy as np
import time
from datetime import datetime, date
import schedule
import ta
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
pw='{password}'
cert_pw='{password}'
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
#Tick Data Call
#----------------------------------------------------------
market=["NQM22"]
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
        import time
        time.sleep(0.2)
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
        globals()['t{}'.format(self.third)]=t.drop(columns='Time')
        globals()['t{}'.format(self.third)]=globals()['t{}'.format(self.third)].sort_index(ascending=True)
        globals()['t{}'.format(self.third)].astype(float)
        print('Tick end')
t_600=TickData("F", market[0], 600, 100)
t_600.tick_data()
#----------------------------------------------------------
#각 분봉 호출코드 (필요 분봉: 1, 3, 5)
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
        import time
        time.sleep(0.2)
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
        min=pd.DataFrame(minprice)
        min=min.rename(columns={0:'Date', 1:'Time', 2:'Open', 3:'High', 4:'Low', 5:'Close'})
        min=min.sort_index(ascending=False)
        min['Time']=min['Date']+min['Time']
        min['Time']=min['Time'].astype('str')
        min['Time']=pd.to_datetime(min['Time'])
        min=min.drop(columns=['Date'])
        min.index=min['Time']
        globals()['mt{}'.format(self.second)]=min.drop(columns='Time')
        print("min end")
        import time
        time.sleep(1)
min1=MinuteData(market[0], 1, 100)
min3=MinuteData(market[0], 3, 100)
min5=MinuteData(market[0], 5, 100)
min1.set_data()  #1분에 한번씩 호출
min3.set_data()
min5.set_data()
schedule.every(1).minute.do(min1.set_data)
schedule.every(1).minute.do(min3.set_data)
schedule.every(1).minute.do(min5.set_data)
schedule.every(0.1).seconds.do(t_600.tick_data)
import pyperclip
import pyautogui
globals()['states']=0
globals()['p_cur']=0
globals()['loss_open']=0
globals()['loss_stack']=0
profit_stack=0
while True:
    schedule.run_pending() 
    mul=[1.5]   
    tick_kind=[600]
    #볼린저밴드 조건 제작
    for j in tick_kind:    
        for k in mul:                 
            globals()['t{}_{}_upper'.format(j, int(k))]=globals()["t{}".format(j)]['Close'].rolling(window=20).mean()+k*globals()["t{}".format(j)]['Close'].rolling(window=20).std()                                        
            globals()['t{}_{}_lower'.format(j, int(k))]=globals()["t{}".format(j)]['Close'].rolling(window=20).mean()-k*globals()["t{}".format(j)]['Close'].rolling(window=20).std()    
    #CCI 
    
    cci600_p20=ta.trend.cci(low=t600["Low"].astype(float), high=t600["High"].astype(float), close=t600["Close"].astype(float), window=20, constant=0.015).dropna(axis=False)
    cci600=ta.trend.cci(low=t600["Low"].astype(float), high=t600["High"].astype(float), close=t600["Close"].astype(float), window=9, constant=0.015).dropna(axis=False)
    #볼린저밴드 제작
    ma=[12, 20]
    mul=[0.2, 1.8]

    #볼린저밴드 가격 업데이트
    min_kind=[1, 3, 5]
    for i in min_kind:
        if float(t600['Close'][-1]) >= float(globals()['mt{}'.format(i)].iloc[-1]["High"]):
            globals()['mt{}'.format(i)].iloc[-1]["High"]=t600['Close'][-1]
            globals()['mt{}'.format(i)].iloc[-1]["Close"]=t600['Close'][-1]
        elif float(t600['Close'][-1]) <= float(globals()['mt{}'.format(i)].iloc[-1]["Low"]): 
            globals()['mt{}'.format(i)].iloc[-1]["Low"]=t600['Close'][-1]
            globals()['mt{}'.format(i)].iloc[-1]["Close"]=t600['Close'][-1]
        else:
            globals()['mt{}'.format(i)].iloc[-1]["Close"]=t600['Close'][-1]  
    #5분봉, 3분봉, 1분봉 볼벤 세팅
    m5_mean=mt5['Close'].rolling(window=20).mean()
    m3_mean=mt3['Close'].rolling(window=20).mean()
    m1_mean=mt1['Close'].rolling(window=20).mean()
    for k in mul:         
        globals()['mt5_{}_upper'.format(int(k))]=m5_mean+k*mt5['Close'].rolling(window=20).std()                                        
        globals()['mt5_{}_lower'.format(int(k))]=m5_mean-k*mt5['Close'].rolling(window=20).std()              
        globals()['mt3_{}_upper'.format(int(k))]=m3_mean+k*mt3['Close'].rolling(window=20).std()                                        
        globals()['mt3_{}_lower'.format(int(k))]=m3_mean-k*mt3['Close'].rolling(window=20).std()                    
        globals()['mt1_{}_upper'.format(int(k))]=m1_mean+k*mt1['Close'].rolling(window=20).std()                    
        globals()['mt1_{}_lower'.format(int(k))]=m1_mean-k*mt1['Close'].rolling(window=20).std()   
    #매도조건함수
    def sellcondition(cci600):
        sellconlist=[]
        for i in min_kind:
            
            #볼린저밴드 상단 닫혔을 때 조건
            globals()["sellbb_btw{}".format(i)]=float(globals()["mt{}".format(i)].iloc[-1]['High']) >= round(globals()["mt{}_1_upper".format(i)][-1], 2)
            globals()["sellbb_1n2cndl{}".format(i)]=round(globals()["mt{}_1_upper".format(i)][-1], 2) <= round(globals()["mt{}_1_upper".format(i)][-2], 2)
            globals()["sellbb_2n3cndl{}".format(i)]=round(globals()["mt{}_1_upper".format(i)][-2], 2) <= round(globals()["mt{}_1_upper".format(i)][-3], 2)
            #볼린저밴드 하단이 열릴 때 조건
            globals()["sellma_btw{}".format(i)]=round(globals()["mt{}_0_lower".format(i)][-1], 2) <= float(globals()["mt{}".format(i)].iloc[-1]['High']) <= round(globals()["mt{}_0_upper".format(i)][-1], 2)
            globals()["sellbb_lwcon{}".format(i)]=any((round(globals()["mt{}_1_lower".format(i)][-15:],2) >= globals()["mt{}".format(i)]['Low'][-15:].astype(float)))
            #600틱 CCI 조건
            cciupover=cci600>=100
            cciup_over=any(cciupover[-3:]==True) and (cci600[-3]>=100 and cci600[-2]<100)
            #조건취합
            sell_con= (globals()["sellbb_btw{}".format(i)] and (globals()["sellbb_1n2cndl{}".format(i)] or globals()["sellbb_2n3cndl{}".format(i)]) or \
                (globals()["sellma_btw{}".format(i)] and globals()["sellbb_lwcon{}".format(i)])) and \
                    cciup_over
            
            print(sell_con)
            sellconlist.append(sell_con) 
        sell=any(sellconlist)
        
        return sell    
    #매수진입조건 함수
    def buycondition(cci600):
        buyconlist=[]
        for i in min_kind:
            #볼린저밴드 하단 닫혔을 때 조건
            globals()["buybb_btw{}".format(i)]=float(globals()["mt{}".format(i)].iloc[-1]['Low']) <= round(globals()["mt{}_1_lower".format(i)][-1], 2)
            globals()["buybb_1n2cndl{}".format(i)]=round(globals()["mt{}_1_lower".format(i)][-1], 2) >= round(globals()["mt{}_1_lower".format(i)][-2], 2)
            globals()["buybb_2n3cndl{}".format(i)]=round(globals()["mt{}_1_lower".format(i)][-2], 2) >= round(globals()["mt{}_1_lower".format(i)][-3], 2)
            #볼린저밴드 상단 열렸을 때 중심선 조건
            globals()["buyma_btw{}".format(i)]=round(globals()["mt{}_0_lower".format(i)][-1], 2) <= float(globals()["mt{}".format(i)].iloc[-1]['Low']) <= round(globals()["mt{}_0_upper".format(i)][-1], 2)
            globals()["buybb_upcon{}".format(i)]=any((round(globals()["mt{}_1_upper".format(i)][-15:],2) <= globals()["mt{}".format(i)]['High'][-15:].astype(float)))
            #600틱 CCI 조건
            ccidnover=cci600<=-100
            ccidn_over=any(ccidnover[-3:]==True) and (cci600[-3]<=-100 and cci600[-2]>-100)
            #조건취합
            buy_con=((globals()["buybb_btw{}".format(i)] and (globals()["buybb_1n2cndl{}".format(i)] or globals()["buybb_2n3cndl{}".format(i)])) or \
                (globals()["buybb_upcon{}".format(i)] and globals()["buyma_btw{}".format(i)])) and ccidn_over
            
            print(buy_con)
            buyconlist.append(buy_con)
        print("-------------------------------")
        buy=any(buyconlist)
        return buy    
    sellenter=sellcondition(cci600)
    buyenter=buycondition(cci600)
    #진입 조건 (프로그램 연계)
        #매수조건     
    if states==0:  
        if (buyenter==True):
            states=1 # **상태메세지를 매수일 때로 변경(상태메세지 : 1로 변경)              
            p_cur=float(t600['Close'][-1]) # 매수 시점의 가격을 언제든지 불러올 수 있도록 변수에 넣어서 저장 *상태메세지와 비교 대조하며 작동상황을 확인하기 위해 작성
            loss_open=float(t600['Open'][-1]) #손실방어를 위한 시가저장
            pyautogui.click(x=3407, y=165, duration=0.02) # 청산버튼 클릭            
            pyautogui.click(x=3555, y=167, duration=0.02) # 매수버튼 클릭        
            # 매수 상태 및 가격, 현재 시간 등을 어딘가에 기록(상태메세지 : Tick Danta 매수신호 발생. 매수진입)
            pyperclip.copy("Nasdaq Tick Danta 매수신호 발생. 매수진입 \n\n" +
            '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
            '\n'+'현재상태 : '+str(states)+
            '\n' +'현재가격 : '+t600['Close'][-1]+
            '\n'+'진입방향 : 상방')
            pyautogui.click( x=2050, y=346)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter')
            time.sleep(0.3)
        #(매도조건)             
        elif (sellenter==True):
            states=-1 # **상태메세지를 매도일 때로 변경(상태메세지 : -1로 변경)
            p_cur=float(t600['Close'][-1]) # 매도 시점의 가격을 언제든지 불러올 수 있도록 변수에 넣어서 저장 *상태메세지와 비교 대조하며 작동상황을 확인하기 위해 작성
            loss_open=float(t600['Open'][-1]) #손실방어를 위한 시가저장
            pyautogui.click(x=3407, y=165, duration=0.02) # 청산버튼 클릭            
            pyautogui.click(x=3171, y=167, duration=0.02) # 매도버튼 클릭                  
            # 매도 상태 및 가격, 현재 시간 등을 어딘가에 기록(상태메세지 : Tick Danta 매도신호 발생. 매도진입)
            pyperclip.copy("Nasdaq Tick Danta 매도신호 발생. 매도진입 \n\n" +
            '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
            '\n'+'현재상태 : '+str(states)+
            '\n' +'현재가격 : '+t600['Close'][-1]+
            '\n'+'진입방향 : 하방')
            pyautogui.click( x=2050, y=346)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.hotkey('enter')  
            time.sleep(0.3)  
    else:
    #진입상태일 때        
        if states == 1:
            # 손절 확인부터
            if (t600['Low'].rolling(window=1).min()[-1] <= p_cur-16) ==True: 
                # **상태메세지에 기록(상태메세지를 0으로 변경)
                states=0                                
                # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : 손절)
                loss_stack=loss_stack+1
                pyperclip.copy("Nasdaq Buy 진입 손절 \n\n" +
                '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
                '\n'+'현재상태 : '+str(states)+
                '\n' +'현재가격 : '+t600['Close'][-1])
                pyautogui.click( x=2050, y=346)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.hotkey('enter')
                time.sleep(0.3)
            #매도 스위칭. 역방향 진입자리 발생  
            elif (sellenter==True):
                states=-1 # **상태메세지를 매도일 때로 변경(상태메세지 : -1로 변경)
                p_cur=float(t600['Close'][-1]) # 매도 시점의 가격을 언제든지 불러올 수 있도록 변수에 넣어서 저장 *상태메세지와 비교 대조하며 작동상황을 확인하기 위해 작성
                profit_stack=profit_stack+1
                loss_open=float(t600['Open'][-1]) #손실방어를 위한 시가저장
                pyautogui.click(x=3407, y=165, duration=0.02) # 청산버튼 클릭 
                pyautogui.click(x=3171, y=167, duration=0.02) # 매도버튼 클릭                  
                # 매도 상태 및 가격, 현재 시간 등을 어딘가에 기록(상태메세지 : Tick Danta 매도신호 발생. 매도진입)
                pyperclip.copy("Switching. Nasdaq Tick Danta 매도신호 발생. 매도진입 \n\n" +
                '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
                '\n'+'현재상태 : '+str(states)+
                '\n' +'현재가격 : '+t600['Close'][-1]+
                '\n'+'진입방향 : 하방')
                pyautogui.click( x=2050, y=346)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.hotkey('enter') 
                time.sleep(0.3)                       
            elif ((cci600_p20[-3]>cci600_p20[-2]) and (cci600_p20[-3]>=100))==True: 
                # 매도 상태 및 가격, 현재 시간 등을 어딘가에 기록(상태메세지 : 반대매도신호 발생 올청산)
                profit_stack=profit_stack+1
                states=0  
                pyautogui.click(x=3407, y=165, duration=0.02) # 청산버튼 클릭                       
                pyperclip.copy("Nasdaq 반대 매도신호 발생. Buy Position 익절 \n\n" + 
                '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
                '\n'+'현재상태 : '+str(states)+
                '\n' +'현재가격 : '+t600['Close'][-1]+
                '\n'+'내용 : 익절청산')
                pyautogui.click( x=2050, y=346)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.hotkey('enter')
                time.sleep(0.3)
                    
        elif states == -1:
            if (t600['High'].rolling(window=1).min()[-1] >= p_cur+16) ==True: 
                # **상태메세지에 기록(상태메세지를 0으로 변경)
                states=0  
                #손절이 나면 스택을 쌓는다.
                loss_stack=loss_stack+1                
                # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : Sell 진입 손절)
                pyperclip.copy("Nasdaq Sell 진입 손절 \n\n" +
                '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
                '\n'+'현재상태 : '+str(states)+
                '\n' +'현재가격 : '+t600['Close'][-1])
                pyautogui.click( x=2050, y=346)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.hotkey('enter')
                time.sleep(0.3)
            #매수 스위칭. 역방향 진입자리 발생  
            elif (buyenter==True):
                states=1 # **상태메세지를 매수일 때로 변경(상태메세지 : 1로 변경)              
                p_cur=float(t600['Close'][-1]) # 매수 시점의 가격을 언제든지 불러올 수 있도록 변수에 넣어서 저장 *상태메세지와 비교 대조하며 작동상황을 확인하기 위해 작성
                loss_open=float(t600['Open'][-1]) #손실방어를 위한 시가저장
                profit_stack=profit_stack+1
                pyautogui.click(x=3407, y=165, duration=0.02) # 청산버튼 클릭 
                pyautogui.click(x=3555, y=167, duration=0.02) # 매수버튼 클릭        
                # 매수 상태 및 가격, 현재 시간 등을 어딘가에 기록(상태메세지 : Tick Danta 매수신호 발생. 매수진입)
                pyperclip.copy("Switching. Nasdaq Tick Danta 매수신호 발생. 매수진입 \n\n" +
                '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
                '\n'+'현재상태 : '+str(states)+
                '\n' +'현재가격 : '+t600['Close'][-1]+
                '\n'+'진입방향 : 상방')
                pyautogui.click( x=2050, y=346)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.hotkey('enter') 
                time.sleep(0.3)                                    
            elif ((cci600_p20[-3]<cci600_p20[-2]) and (cci600_p20[-3]<=-100))==True:   
                # 매도 상태 및 가격, 현재 시간 등을 어딘가에 기록(상태메세지 : 반대매도신호 발생 올청산)
                profit_stack=profit_stack+1                
                states=0 
                pyautogui.click(x=3407, y=165, duration=0.02) # 청산버튼 클릭             
                pyperclip.copy("Nasdaq 반대 매수신호 발생. Sell Position 익절 \n\n" +
                '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
                '\n'+'현재상태 : '+str(states)+
                '\n' +'현재가격 : '+t600['Close'][-1]+
                '\n'+'내용 : 익절청산')
                pyautogui.click( x=2050, y=346)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.hotkey('enter') 
                time.sleep(0.3)                         

    print("현재 진입상태 :", states)
    print("CCI :", cci600[-1]) 
    print("CCI period 20 :", cci600_p20[-1]) 
    print("현재 진입 가격 :", p_cur)  
    print("-------------------------------")    
    # print("(1, 3, 5분봉순) 틱과의 조건만족여부 매수조건 list :", buycondition)
    # print("-------------------------------")
    # print("(1, 3, 5분봉순) 틱과의 조건만족여부 매도조건 list :", sellcondition)
    print("1분 종가 :", mt1["Close"][-1])
    print("3분 종가 :", mt3["Close"][-1])    
    print("5분 종가 :", mt5["Close"][-1]) 
    print("-------------------------------")
    print("Profit Stack :", profit_stack)
    print("Loss Stack :", loss_stack)
    print(t600["Close"].iloc[-1])
    print('현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


