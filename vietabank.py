import requests
import json
import time
from requests.cookies import RequestsCookieJar
import re
import urllib.parse
import html
# from anticaptchaofficial.recaptchav3proxyless import *
# solver = recaptchaV3Proxyless()

# solver.set_verbose(1)
# solver.set_key("f3a44e66302c61ffec07c80f4732baf3")
# solver.set_website_url("https://ebanking.vietabank.com.vn/")
# solver.set_page_action("home_page")
# solver.set_min_score(0.3)
# solver.set_soft_id(0)

api_key = "CAP-6C2884061D70C08F10D6257F2CA9518C"  # your api key of capsolver
site_url = "https://ebanking.vietabank.com.vn/"  # page url of your target site


def capsolver(site_key):
    payload = {
        "clientKey": api_key,
        "task": {
            "type": 'ReCaptchaV3TaskProxyLess',
            "websiteKey": site_key,
            "websiteURL": site_url,
            "minScore": 0.7
        }
    }
    res = requests.post("https://api.capsolver.com/createTask", json=payload)
    resp = res.json()
    task_id = resp.get("taskId")
    if not task_id:
        print("Failed to create task:", res.text)
        return
    print(f"Got taskId: {task_id} / Getting result...")

    while True:
        time.sleep(1)  # delay
        payload = {"clientKey": api_key, "taskId": task_id}
        res = requests.post("https://api.capsolver.com/getTaskResult", json=payload)
        resp = res.json()
        status = resp.get("status")
        if status == "ready":
            return resp.get("solution", {}).get('gRecaptchaResponse')
        if status == "failed" or resp.get("errorId"):
            print("Solve failed! response:", res.text)
            return
class VietaBank:
    def __init__(self, username, password, account_number):
        self.keyanticaptcha = "b8246038ce1540888c4314a6c043dcae"
        self.cookies = RequestsCookieJar()
        self.session = requests.Session()
        self.tokenNo = ''
        self.url_post = ''
        self.url_accountactivityprepare = ''
        self._ss = ''
        self.password = password
        self.username = username
        self.account_number = account_number
        self.is_login = False
    def check_title(self,html_content):
        pattern = r'<title>(.*?)</title>'
        match = re.search(pattern, html_content)
        return match.group(1) if match else None
    def check_error_message(self,html_content):
        pattern = r'<div id="ul.errors" class="errorblock" style="color:red; ">(.*?)</div>'
        match = re.search(pattern, html_content)
        return match.group(1) if match else None
    def extract_data_cId(self,html_content):
        pattern = r'<input id="data_cId" name="data_cId" type="hidden" value="(.*)"/>'
        match = re.search(pattern, html_content)
        return match.group(1) if match else None
    def extract_data_sitekey(self,html_content):
        pattern = r'<button id="btnfind" name="btnfind" data-sitekey="(.*)" type="button" data-action="submit"'
        match = re.search(pattern, html_content)
        return match.group(1) if match else None
    def extract_url_post(self,html_content,account_number):
        pattern = r'<a href="/(.*)">'+account_number+'</a>'
        match = re.search(pattern, html_content)
        return match.group(1) if match else None
    def extract_url_accountactivityprepare(self,html_content):
        pattern = r'<a href="(.*)"  class="btn btn-primary btn-sm">Lịch sử biến động số dư</a>'
        match = re.search(pattern, html_content)
        return match.group(1) if match else None
    def extract_transaction(self,html_content):
        pattern = r'var transHis = (.*)];'
        match = re.search(pattern, html_content)
        return match.group(1)+']' if match else '[]'
    def extract_account_name(self,html_content):
        pattern = r'<input id="flddestaccountname" name="rqBene\.beneficiaryDTO\[0\]\.paymentTemplateDTO\[0\]\.domesticImReqDataDTO\.destAccount\.accountDesc" class="form-control eng" title="T&ecirc;n chủ thẻ" data-toggle="tooltip" data-placement="top" readonly="readonly" type="text" value="(([A-Z]|\s)*)"/>'
        match = re.search(pattern, html_content)
        return match.group(1) if match else None
    def extract_account_number(self,html_content):
        pattern = r'<a href="/accountdetailsview\.html\?pid=\w+&fcid=asmp">(\d+)</a>\s*-\s*.*?<td.*?>([\d,.]+)</td>'

        matches = re.findall(pattern, html_content, re.DOTALL)

        extracted_data = []
        for match in matches:
            account_number = match[0]
            account_balance = float(match[1].replace(',', ''))
            account_info = {'account_number': account_number, 'balance': account_balance}
            extracted_data.append(account_info)

        if extracted_data:
            return (extracted_data)
        else:
            return None
    def login(self):
        url = "https://ebanking.vietabank.com.vn/"
        payload = {}
        headers = {}
        response = self.session.get(url, headers=headers, data=payload)

        url = "https://ebanking.vietabank.com.vn/"
        payload = 'ipify=0.0.0.0&disable-pwd-mgr-1=disable-pwd-mgr-1&disable-pwd-mgr-2=disable-pwd-mgr-2&disable-pwd-mgr-3=disable-pwd-mgr-3&askRename=&askRenameMsg=&actionFlg=&idChannelUser='+str(self.username)+'&password='+urllib.parse.quote(str(self.password))
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.100.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://ebanking.vietabank.com.vn',
        'Connection': 'keep-alive',
        'Referer': 'https://ebanking.vietabank.com.vn/',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
        }

        response = self.session.post(url, headers=headers, data=payload)
        self._ss = str(int(time.time() * 1000))
        title = self.check_title(response.text)
        if title == 'Tổng quan tài khoản':
            self.is_login = True
            return {
                'code': 200,
                'success': True,
                'message': 'Đăng nhập thành công',
                'data':{
                'tokenNo': self.tokenNo
                }
            }

        else:
            check_error_message = html.unescape(self.check_error_message(response.text))
            if check_error_message:
                if 'Tên đăng nhập hoặc mật khẩu không hợp lệ' in check_error_message:
                    return {'code':444,'success': False, 'message': (check_error_message)} 
                return {
                    'code':400,
                    'success': False,
                    'message': (check_error_message)
                }
            else:
                return {
                    'code':520,
                    'success': False,
                    'message': 'Unknow Errors!'
                }

    def get_accounts_list(self,account_number):
        payload = {}
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.100.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://ebanking.vietabank.com.vn/accountdetailsview.html',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache'
        }

        response = self.session.get("https://ebanking.vietabank.com.vn/accountsummary.html", headers=headers, data=payload)
        accounts = self.extract_account_number(response.text)
        self.url_post = self.extract_url_post(response.text,account_number)
        return accounts
    def get_account_details(self):
            url = "https://ebanking.vietabank.com.vn/"+self.url_post
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.100.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Origin': 'https://ebanking.vietabank.com.vn',
                'Connection': 'keep-alive',
                'Referer': 'https://ebanking.vietabank.com.vn/accountdetailsview.html',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache'
                }

            response = self.session.get(url, headers=headers)
            self.url_accountactivityprepare = self.extract_url_accountactivityprepare(response.text)
            
            return response.text
    def get_balance(self,account_number):
        if not self.is_login:
            login = self.login()
            if not login['success']:
                return login
        accounts_list = self.get_accounts_list(account_number)
        if accounts_list:
            for account in accounts_list:
                if account.get('account_number') == account_number:
                    if int(account.get('balance')) < 0:
                        return {'code':448,'success': False, 'message': 'Blocked account with negative balances!',
                                'data': {
                                    'account_number':account_number,
                                    'balance':int(account.get('balance'))
                                }
                                }
                    else:
                        return {'code':200,'success': True, 'message': 'Thành công',
                                'data':{
                                    'account_number':account_number,
                                    'balance':int(account.get('balance'))
                        }}
            return {'code':404,'success': False, 'message': 'account_number not found!'} 
        else: 
            return {'code':520 ,'success': False, 'message': 'Unknown Error!'} 

    def get_transactions(self,account_number,fromDate,toDate):
        if not self.is_login:
            login = self.login()
            if not login['success']:
                return login
        # self.get_account_details()
        # url = "https://ebanking.vietabank.com.vn/"+self.url_accountactivityprepare
        url = "https://ebanking.vietabank.com.vn/accountactivityprepare.html"
        payload = {}
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
        }
        response = self.session.get(url, headers=headers, data=payload)
        data_sitekey = self.extract_data_sitekey(response.text)
        # reCaptcha_response = reCaptchaV3('https://www.google.com/recaptcha/api2/anchor?ar=1&k='+data_sitekey+'&co=aHR0cHM6Ly9lYmFua2luZy52aWV0YWJhbmsuY29tLnZuOjQ0Mw..&hl=en&v=moV1mTgQ6S91nuTnmll4Y9yf&size=invisible&sa=submit')
        # solver.set_website_key(data_sitekey)
        # reCaptcha_response = solver.solve_and_return_solution()
        # print(response.text)
        if data_sitekey:
            reCaptcha_response = capsolver(data_sitekey)
            if not reCaptcha_response:
                return   {"success": False,"code": 406,"message": "Error bypass reCaptchaV3!"}
            data_cId = self.extract_data_cId(response.text)
            print(reCaptcha_response)
            payload = {
            'refid': '',
            'rqTrans.account.nbrAccount': str(account_number),
            'rqTrans.searchBy': '1',
            'rqTrans.searchTxnType': '0',
            'rqFromDate': fromDate,
            'rqToDate': toDate,
            'rqFromAmount': '',
            'rqToAmount': '',
            'rqTrans.toaccount.nbrAccount': '',
            'g-recaptcha-response': reCaptcha_response,
            'rqTrans.page.pageNo': '1',
            'rsTrans.totalPages': '0',
            'reporttype': '',
            'flgAction': 'find',
            'ipify':'',
            '_ls': '1',
            '_ss': '1',
            'data_cId': str(data_cId)
            }
            files=[

            ]
            headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Origin': 'https://ebanking.vietabank.com.vn',
            'Referer': url,
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
            'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
            }
            response = self.session.post(url, headers=headers, data=payload,files=files)
            # with open('output.html', 'w', encoding='utf-8') as html_file:
            #     html_file.write(response.text)            
            transactions =  json.loads(self.extract_transaction(response.text))
            return {'code':200,'success': True, 'message': 'Thành công',
                    'data':{
                        'transactions':transactions,
            }}
        else:
            data_cId = self.extract_data_cId(response.text)
            payload = {
            'refid': '',
            'rqTrans.account.nbrAccount': str(account_number),
            'rqTrans.searchBy': '1',
            'rqTrans.searchTxnType': '0',
            'rqFromDate': fromDate,
            'rqToDate': toDate,
            'rqFromAmount': '',
            'rqToAmount': '',
            'rqTrans.toaccount.nbrAccount': '',
            # 'g-recaptcha-response': reCaptcha_response,
            'rqTrans.page.pageNo': '1',
            'rsTrans.totalPages': '0',
            'reporttype': '',
            'flgAction': 'find',
            'ipify':'',
            '_ls': '1',
            '_ss': '1',
            'data_cId': str(data_cId)
            }
            files=[

            ]
            headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Origin': 'https://ebanking.vietabank.com.vn',
            'Referer': url,
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
            'sec-ch-ua': '"Microsoft Edge";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
            }
            response = self.session.post(url, headers=headers, data=payload,files=files)
            # with open('output.html', 'w', encoding='utf-8') as html_file:
            #     html_file.write(response.text)
            transactions =  json.loads(self.extract_transaction(response.text))
            return {'code':200,'success': True, 'message': 'Thành công',
                    'data':{
                        'transactions':transactions,
            }}
    def mapping_bank_code(self,bank_name):
        with open('banks.json','r', encoding='utf-8') as f:
            data = json.load(f)
        for bank in data['data']:
            if bank['shortName'].lower() == bank_name.lower():
                return {
                    'bin': bank['bin'],
                    'name': bank['name'],
                    'code': bank['code']
                    }
        return None
    def get_bank_name(self, ben_account_number, bank_name):
        if not self.is_login:
            login = self.login()
            if not login['success']:
                return login
        url = "https://ebanking.vietabank.com.vn/domesticimmetransfer.html"

        payload = {}
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'https://ebanking.vietabank.com.vn/fundtransfer.html',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
        'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
        }

        response =  self.session.get(url, headers=headers, data=payload)
        data_cId = self.extract_data_cId(response.text)
        bank_info = self.mapping_bank_code(bank_name)
        
        url = "https://ebanking.vietabank.com.vn/domesticimmetransfer.html"
    
        payload = {'rqBene.beneficiaryDTO[0].paymentTemplateDTO[0].idTemplate': '0',
        'sidata.si_type': 'TN',
        'sidata.next_exec_date': '',
        'sidata.executionFrequency': '1',
        'sidata.exec_days': '0',
        'sidata.exec_mths': '0',
        'sidata.exec_yrs': '0',
        'sidata.first_exec_date': '',
        'sidata.final_exec_date': '',
        'feeamt': '0.0',
        'vat': '0.0',
        'feeMin': '0.0',
        'feeMax': '0.0',
        'feePercent': '0.0',
        'cardInfo': '',
        'rqBene.beneficiaryDTO[0].paymentTemplateDTO[0].domesticImReqDataDTO.beneficiaryBankDetails[0].beneficiaryCodeType': 'ATA',
        'rqBene.beneficiaryDTO[0].paymentTemplateDTO[0].domesticImReqDataDTO.beneficiaryBankDetails[0].swiftCode': bank_info['bin'],
        'destbankname2': bank_info['name'] + ' ('+bank_info['code']+')',
        'rqBene.beneficiaryDTO[0].paymentTemplateDTO[0].domesticImReqDataDTO.destAccount.nbrAccount': ben_account_number,
        'rqBene.beneficiaryDTO[0].paymentTemplateDTO[0].domesticImReqDataDTO.destAccount.accountDesc': '',
        'destbankname': '',
        'transferamt': '',
        'rqBene.beneficiaryDTO[0].paymentTemplateDTO[0].domesticImReqDataDTO.narrative': '',
        '__templateName': '',
        'rqBene.beneficiaryDTO[0].paymentTemplateDTO[0].templateName': '',
        '__templatelevel': 'P',
        'rqBene.beneficiaryDTO[0].paymentTemplateDTO[0].typeTxn': '',
        'flgAction': 'getCardInfo',
        'ipify': '',
        '_ls': '1',
        '_ss': '1',
        'data_cId': str(data_cId)}
        files=[

        ]
        headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Origin': 'https://ebanking.vietabank.com.vn',
        'Referer': 'https://ebanking.vietabank.com.vn/domesticimmetransfer.html',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
        'sec-ch-ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"'
        }

        response = self.session.post(url, headers=headers, data=payload,files=files)
        account_name = self.extract_account_name(response.text)
        return account_name
        

    

username = "0328656240"
password = "Phau147@"
fromDate='10/05/2024'
toDate = '12/05/2024'
account_number = "00553597"

vietabank = VietaBank(username,password,account_number)

# username = "0362245196"
# password = "Nguyen157#"
# fromDate='29/02/2024'
# toDate = '30/03/2024'
# account_number = "00509294"

# session_raw = vietabank.login()
# print(session_raw)

# accounts_list = vietabank.get_accounts_list()
# print(accounts_list)

# balance = vietabank.get_balance(account_number)
# print(balance)

history = vietabank.get_transactions(account_number,fromDate,toDate)
print(history)

# bank_name = vietabank.get_bank_name("0621000456871", "Vietcombank")
# print(bank_name)