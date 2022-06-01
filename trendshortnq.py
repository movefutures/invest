'''
로직 설명: 
타점 >
-960틱 밴드차트를 이용하여 방향성을 확인
-중심선을 기준으로 하방이면 위, 상방이면 아래 구간을 PRZ로 설정
-20틱으로 방향성에 따라 진입지점을 설정(고점저항 저점저항을 세부 PRZ로 지정)  
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
t_20=TickData("F", "NQM22", 20, 100)        
t_120=TickData("F", "NQM22", 120, 100)
t_600=TickData("F", "NQM22", 600, 100)
t_20.tick_data()
t_120.tick_data()
t_600.tick_data()
schedule.every(0.1).seconds.do(t_20.tick_data)
schedule.every(0.1).seconds.do(t_120.tick_data)
schedule.every(0.1).seconds.do(t_600.tick_data)
import pyperclip
import pyautogui
globals()['states']=0
globals()['trend_states']=0
globals()['p_cur']=0
globals()['loss_open']=0
globals()['loss_stack']=0
while True:
    schedule.run_pending() 
    mul=[1.5]   
    tick_kind=[120]
    #볼린저밴드 조건 제작
    for j in tick_kind:    
        for k in mul:                 
            globals()['t{}_{}_upper'.format(j, int(k))]=globals()["t{}".format(j)]['Close'].rolling(window=20).mean()+k*globals()["t{}".format(j)]['Close'].rolling(window=20).std()                                        
            globals()['t{}_{}_lower'.format(j, int(k))]=globals()["t{}".format(j)]['Close'].rolling(window=20).mean()-k*globals()["t{}".format(j)]['Close'].rolling(window=20).std()    
    #밴드차트
    upperline=t600['High'].rolling(window=10).max()
    lowerline=t600['Low'].rolling(window=10).min()
    midline=(upperline+lowerline)/2
    upperline20=t20['High'].rolling(window=12).max()
    lowerline20=t20['Low'].rolling(window=12).min()
    midline20=(upperline+lowerline)/2    
    #CCI 
    
    cci20_600=ta.trend.cci(low=t600["Low"].astype(float), high=t600["High"].astype(float), close=t600["Close"].astype(float), window=20, constant=0.015).dropna(axis=False)
    cci600=ta.trend.cci(low=t600["Low"].astype(float), high=t600["High"].astype(float), close=t600["Close"].astype(float), window=9, constant=0.015).dropna(axis=False)
    cci20=ta.trend.cci(low=t20["Low"].astype(float), high=t20["High"].astype(float), close=t20["Close"].astype(float), window=9, constant=0.015).dropna(axis=False)
    #저항딛는 구간
    uppermin20=upperline20.rolling(window=40).min()
    lowermax20=lowerline20.rolling(window=40).max()
    #추세판별함수 
    #당시의 틱이 상승내지 하락이며 이전에 두번의 상승 및 하락이 추가로 진행되어야 함.
    def trendcon(upperline, lowerline):
        trendstates=0
        trconup=[]
        trcondn=[]
        #상승추세
        for i in range(10):    
            if upperline[-i]>upperline[-(i+1)]:
                trconup.append(1)
        for i in range(10):    
            if lowerline[-i]<lowerline[-(i+1)]:
                trcondn.append(1)
        sumup=sum(trconup)    
        print("상승추세 스텍 : ", sumup)
        sumdn=sum(trcondn)
        print("하락추세 스텍 : ", sumdn)
        if sumup>=3 :
            trendstates=1
        elif sumdn>=3 :
            trendstates=-1
        return trendstates
    trendstates=trendcon(upperline, lowerline)
    if trendstates>=1:
        trend_states=trendstates
    elif trendstates<=-1:
        trend_states=trendstates
    #청산 조건 함수 (필요항목 : 밴드차트 중심선, 600틱, CCI, 120틱 상하단)
    #매수진입청산 조건
    def sellcon(midline, cci600, t600, t120, t120_1_upper):
        #중심선 라인을 기준으로 위로 돌파 해 있는지 여부를 확인(매수청산)
        midcrossup=midline<t600["High"].astype(float)
        
        #매수청산
        cciupover=cci600>=100
        cciup_over=any(cciupover[-3:]==True)
        #청산 조건 1
        uplinehigh=t120["High"].astype(float)>t120_1_upper
        #청산 조건 2
        upinclose=t120["Close"].astype(float)>t120_1_upper
        #청산 3
        upoutclose=t120["Close"].astype(float)<t120_1_upper
        #조건 취합 
        sell_con=any(midcrossup[-2:]==True) and \
            cciup_over and uplinehigh[-3] and \
                upinclose[-3] and \
                    upoutclose[-2]
        return sell_con
    #매도진입청산 조건
    def buycon(midline, cci600, t600, t120, t120_1_lower):
        #중심선 라인을 기준으로 아래로 빠져있는지의 여부를 확인(매도청산)
        midcrssdn=midline>t600["Low"].astype(float)
        
        #매도청산
        ccidnover=cci600<=-100
        ccidn_over=any(ccidnover[-3:]==True)
        #청산조건 1
        dnlinelow=t120["Low"].astype(float)<t120_1_lower
        #청산조건 2
        dninclose=t120["Close"].astype(float)<t120_1_lower
        #청산조건 3
        dnoutclose=t120["Close"].astype(float)>t120_1_lower
        #조건 취합
        buy_con=any(midcrssdn[-2:]==True) and \
            ccidn_over and dnlinelow[-3] and \
                dninclose[-3] and \
                    dnoutclose[-2]
        return buy_con
    #매도 진입조건
    def sellentercon(midline, midline20, cci20, t600, t20, upperline20, lowerline20):
        #중심선 라인을 기준으로 위로 돌파 해 있는지 여부를 확인(매도 & 매수청산)
        midcrossup=midline<t600["High"].astype(float)
        
        #600틱 조건
        cciupover=cci600>=100
        cciup_over=any(cciupover[-3:]==True)
        #20틱 구간 설정
        lowermax20=lowerline20.rolling(window=40).max()
        sellzone=pd.DataFrame([-5<=(lowermax20[i]-upperline20[i])<=10 for i in range(len(t20["High"]))]).set_index(t20["High"].index)[0]
    
        #20틱 진입조건
        sellccicon=cci20.astype(float)[-20:]>=100   
        
        #조건 취합 
        sell_con=any(midcrossup[-2:]==True) and \
            cciup_over and sellzone[-2] and \
                    sellccicon[-2]
        return sell_con
    #매수 진입조건
    def buyentercon(midline, midline20, cci20, t600, t20, upperline20, lowerline20):
        #중심선 라인을 기준으로 아래로 빠져있는지의 여부를 확인(매수 & 매도청산)
        midcrssdn=midline>t600["Low"].astype(float)
        
        #600틱 조건
        ccidnover=cci600<=-100
        ccidn_over=any(ccidnover[-3:]==True)
        #20틱 구간설정
        uppermin20=upperline20.rolling(window=40).min()
        buyzone=pd.DataFrame([-10<=(uppermin20[i]-lowerline20[i])<=5 for i in range(len(t20["Low"]))]).set_index(t20["Low"].index)[0]
        #20틱 진입조건
        buyccicon=cci20.astype(float)[-20:]<=-100    
        #조건 취합
        buy_con=any(midcrssdn[-2:]==True) and \
            ccidn_over and buyzone[-2] and \
                    buyccicon[-2]
        return buy_con
    sellenter=sellentercon(midline, midline20, cci20, t600, t20, upperline20, lowerline20)
    buyenter=buyentercon(midline, midline20, cci20, t600, t20, upperline20, lowerline20)
    sell_cutcon=sellcon(midline, cci20_600, t600, t120, t120_1_upper)
    buy_cutcon=buycon(midline, cci20_600, t600, t120, t120_1_lower)
    #진입 조건 (프로그램 연계)
    #매수
    if trend_states==1 and states==0:
        #매수조건       
        if (buyenter==True):
            states=1 # **상태메세지를 매수일 때로 변경(상태메세지 : 1로 변경)              
            p_cur=float(t600['Close'][-1]) # 매수 시점의 가격을 언제든지 불러올 수 있도록 변수에 넣어서 저장 *상태메세지와 비교 대조하며 작동상황을 확인하기 위해 작성
            loss_open=float(t600['Open'][-1]) #손실방어를 위한 시가저장
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
       
    #(매도조건)               
    elif trend_states==-1 and states==0:
        #매도조건   
        if (sellenter==True):
            states=-1 # **상태메세지를 매도일 때로 변경(상태메세지 : -1로 변경)
            p_cur=float(t600['Close'][-1]) # 매도 시점의 가격을 언제든지 불러올 수 있도록 변수에 넣어서 저장 *상태메세지와 비교 대조하며 작동상황을 확인하기 위해 작성
            loss_open=float(t600['Open'][-1]) #손실방어를 위한 시가저장
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
              
    else:
    #진입상태일 때        
        if states == 1:
            # 손절 확인부터
            if (t600['Low'].rolling(window=1).min()[-1] <= p_cur-14) ==True: 
                # **상태메세지에 기록(상태메세지를 0으로 변경)
                states=0                                
                # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : 손절)
                # 5봉 이내에서 손절이 나면 스택을 쌓는다.
                if any(t600["Open"].astype(float)[-5:]==loss_open):
                    loss_stack=loss_stack+1
                pyperclip.copy("Nasdaq Buy 진입 손절 \n\n" +
                '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
                '\n'+'현재상태 : '+str(states)+
                '\n' +'현재가격 : '+t600['Close'][-1])
                pyautogui.click( x=2050, y=346)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.hotkey('enter') 
                        
            elif sell_cutcon==True: 
                # 매도 상태 및 가격, 현재 시간 등을 어딘가에 기록(상태메세지 : 반대매도신호 발생 올청산)
                states=0  
                loss_stack=0 # Loss stack 초기화
                pyautogui.click(x=3407, y=165, duration=0.02) # 청산버튼 클릭                       
                pyperclip.copy("Nasdaq 반대 매도신호 발생. Buy Position 익절 \n\n" + 
                '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
                '\n'+'현재상태 : '+str(states)+
                '\n' +'현재가격 : '+t600['Close'][-1]+
                '\n'+'내용 : 익절청산')
                pyautogui.click( x=2050, y=346)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.hotkey('enter')
                    
        elif states == -1:
            if (t600['High'].rolling(window=1).min()[-1] >= p_cur+14) ==True: 
                # **상태메세지에 기록(상태메세지를 0으로 변경)
                states=0  
                # 5봉 이내에서 손절이 나면 스택을 쌓는다.
                if any(t600["Open"].astype(float)[-5:]==loss_open):
                    loss_stack=loss_stack+1                
                # 현재 상태 및 가격, 현재 시간 등을 어딘가에 기록(기록메세지 : Sell 진입 손절)
                pyperclip.copy("Nasdaq Sell 진입 손절 \n\n" +
                '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
                '\n'+'현재상태 : '+str(states)+
                '\n' +'현재가격 : '+t600['Close'][-1])
                pyautogui.click( x=2050, y=346)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.hotkey('enter')  
                                    
            elif buy_cutcon==True:   
                # 매도 상태 및 가격, 현재 시간 등을 어딘가에 기록(상태메세지 : 반대매도신호 발생 올청산)
                states=0 
                loss_stack=0 # Loss stack 초기화
                pyautogui.click(x=3407, y=165, duration=0.02) # 청산버튼 클릭             
                pyperclip.copy("Nasdaq 반대 매수신호 발생. Sell Position 익절 \n\n" +
                '현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))+
                '\n'+'현재상태 : '+str(states)+
                '\n' +'현재가격 : '+t600['Close'][-1]+
                '\n'+'내용 : 익절청산')
                pyautogui.click( x=2050, y=346)
                pyautogui.hotkey('ctrl', 'v')
                pyautogui.hotkey('enter')                          

    print("현재 진입상태 :", states)
    print("CCI :", cci600[-1]) 
    print("현재 진입 가격 :", p_cur)  
    print("-------------------------------")
    print("위로중심돌파 확인 :", (midline<t600["High"].astype(float))[-1])
    print("CCI매도조건 확인 :", any((cci600>=100)[-3:]==True))
    print("20틱 매도 진입조건 :", (pd.DataFrame([-5<=(lowerline20.rolling(window=40).max()[i]-upperline20[i])<=10 for i in range(len(t20["High"]))]).set_index(t20["High"].index)[0])[-2])  
    print("CCI 20틱 매도조건 :", (cci20.astype(float)[-20:]>=100)[-2])
    print("-------------------------------")
    print("아래로중심돌파 확인 :", (midline>t600["Low"].astype(float))[-1])
    print("CCI매수조건 확인 :", any((cci600<=-100)[-3:]==True))        
    print("20틱 매수 진입조건 :", (pd.DataFrame([-10<=(upperline20.rolling(window=40).min()[i]-lowerline20[i])<=5 for i in range(len(t20["Low"]))]).set_index(t20["Low"].index)[0])[-2]) 
    print("CCI 20틱 매수조건 :", ((cci20.astype(float)[-20:]<=-100)==True)[-2]) 
    print("-------------------------------")
    print("현재 추세상태 :", trend_states)    
    print("Loss Stack :", loss_stack)
    print(t120["Close"].iloc[-1])
    print(t600["Close"].iloc[-1])
    print('현재시간 : '+str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


