import yagmail

MAIL_PASSWORD = "awexnzjbnouukogv"
MAIL_FROM = "chennaifreelancersclub@gmail.com"
host = 'smtp.gmail.com'
port = 465
async def mail_trigger(email_to, otp):
    with yagmail.SMTP(MAIL_FROM, MAIL_PASSWORD, host, port) as yag:
        yag.send([email_to], "CFC", """<html><body><h2>CFC Testing: {}</h2></body></html>""".format(otp))
