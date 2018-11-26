from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from payment.Checksum import generate_checksum_by_str, generate_checksum, verify_checksum
from payment.Checksum import verify_checksum_by_str


def pay(request):
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

    callbackUrl = 'check'


    paytmParams = {
        'MID': merchantMid,
        'ORDER_ID': orderId,
        'CHANNEL_ID':channelId,
        'CUST_ID':custId,
        'MOBILE_NO': mobileNo,
        'EMAIL':email,
        'TXN_AMOUNT':txnAmount,
        'WEBSITE':website,
        'INDUSTRY_TYPE_ID':industryTypeId,
        'CALLBACK_URL':callbackUrl,
    }

    paytmChecksum = generate_checksum(paytmParams, merchantKey)

    paytmParams['CHECKSUMHASH'] = paytmChecksum

    return render(request , 'payment/form1.html' ,paytmParams)







def check(request):


    merchantKey = 'aahU7q8OUT@6r&ON'

    paytmParams = request.POST
    if request.POST('CHECKSUMHASH'):
        paytmChecksum = request.POST('CHECKSUMHASH')
    else:
        paytmChecksum = ''


    isValidChecksum = verify_checksum(paytmParams, merchantKey, paytmChecksum)

    if (isValidChecksum):
        return render(request, 'payment/form2.html', paytmParams)
    else:
        return HttpResponse("checksum verify failed")


def status(request):
    return render(request, 'payment/status.html')