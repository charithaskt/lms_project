from django.shortcuts import render

# Create your views here.


merchantMid = 'LDSSev95602499938192'

merchantKey = 'aahU7q8OUT@6r&ON'


orderId = 'order1'

channelId = 'WEB'

custId = 'cust123'

mobileNo = '7777777777'

email = 'username@emailprovider.com'
txnAmount = '100.12'
website = 'WEBSTAGING'

industryTypeId = 'Retail'

callbackUrl = 'https://merchant.com/callback/'

paytmParams = {
    'MID': merchantMid ,
    'ORDER_ID': orderId ,
    'CHANNEL_ID':channelId ,
    'CUST_ID':custId ,
    'MOBILE_NO' : mobileNo ,
    'EMAIL':email ,
    'TXN_AMOUNT':txnAmount ,
    'WEBSITE' :website ,
    'INDUSTRY_TYPE_ID' : industryTypeId,
    'CALLBACK_URL':callbackUrl,
}

paytmChecksum = CheckSumServiceHelper.getCheckSumServiceHelper().genrateCheckSum(merchantKey, paytmParams)
