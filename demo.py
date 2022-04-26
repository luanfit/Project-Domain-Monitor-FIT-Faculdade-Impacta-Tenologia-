# -*- coding: utf-8 -*-

import pandas as pd
import json
import csv
from shutil import move
import time
import os
from os import path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dnpedia.dnpedia import DnPediaSearch


dp = DnPediaSearch()
json_imparsing = []

dominios = ['impacta']

def Send_Email():

    #email_smtp = '52.97.67.66'
    email_smtp = 'smtp.gmail.com'
    email_user = 'e-mail de envio'
    email_send = 'destinatios'
    subject = 'titulo do e-mail'

    print('preparing to sending email')

    msg = MIMEMultipart()
    msg.set_boundary('------------040907050602020300000601')
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    print('message creating')

    body = """\
    <!DOCTYPE html>
    <html lang="pt-br">
        <head>
            <meta charset="utf-8"/>
            <style>
                .safeway > p {
                font-family: arial;
                font-size: 32px;
                color: grey;
                }

                .safeway > p > span {
                    font-family: arial;
                    font-style: bold;
                    font-size: 48px;
                    color: orange;

                }

                </style>
        </head>
        <body>
            <p>
                Report - Dominios Recentemente Adicionados. Caso os anexos tragam um novo dominio, siga o procedimento abaixo.
            </p>
            <p>
            </p>
        <div>
            </div>
    </html>
    """
    msg.attach(MIMEText(body, 'html'))

    print('opening atachments')
    filename = []
    for dms in dominios:
        filename.append(str(dms+".csv"))

    for filename in filename:
        try:
            attachment = open(filename, 'rb')

            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())

            encoders.encode_base64(part)

            part.add_header('Content-Disposition', 'attachment; filename= '+filename)

            msg.attach(part)
            print('csv atacheved')
        except:
            continue

    text = msg.as_string()
    server = smtplib.SMTP(email_smtp, 587)
    server.set_debuglevel(0)
    server.starttls()
    server.ehlo(email_smtp)
    server.login(email_user, 'senha_api')

    print('im sending email now')

    server.sendmail(email_user, email_send, text)
    server.quit()


def Search_Domain():
    for dominio in dominios:
        json_imparsing = []
        json_imparsing.append(str(json.dumps(dp.search(dominio), indent=4)))
        f = open(str(dominio)+'.json', 'w')
        for item in json_imparsing:
            f.write(item)
        f.close()


def To_Csv():

        for dominio in dominios:
           with open((str(dominio)+'.json')) as json_file:
                data = json.load(json_file)

                # for reading nested data [0] represents
                # the index value of the list
                #print(data['rows'][0])

                # for printing the key-value pair of
                # nested dictionary for looop can be used
                dominiofilter = []
                print("\nPrinting nested dicitonary as a key-value pair\n")
                for i in data['rows']:
                    print('\n')
                    dominiofilter.append((i['name']+'.'+i['zoneid'],"Data:", i['thedate']))
                    print(dominiofilter)

        for dominio in dominios:
           try:
                dm = str(dominio)
                print (dominio)
                print (dm)
                print (type(dm))
                df = pd.read_json((str(dm)+'.json'))
                if path.exists(r'/'+str(dm)+'.csv') == False:
                    df.to_csv(str(dominio)+".csv", index = False, header = False)
                    print('foi', dominio)
                else:
                    os.remove('/'+str(dm)+'.csv')
                    df.to_csv(str(dominio)+".csv", index = False, header = False)
               ### Do Some Stuff
           except:
               continue


Search_Domain()
To_Csv()
Send_Email()
