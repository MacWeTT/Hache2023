from .models import VerifiedEmails
import pandas
import os
from hache.settings import BASE_DIR


def run():
    pathh = os.path.join(BASE_DIR, 'emails.csv')
    dfList = pandas.read_csv(pathh)['emails'].tolist()
    all_emails = [*set(dfList)]
    bulk_list = list()
    for i in range(len(all_emails)):
        bulk_list.append(
            VerifiedEmails(email=all_emails[i]))

    bulk_msj = VerifiedEmails.objects.bulk_create(bulk_list)
    print(bulk_msj)
