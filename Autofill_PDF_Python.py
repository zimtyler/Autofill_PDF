# Recently updated this old script. This was originally my first big python project. And while the older version was difficult to read, it saved me so much time.
# Thought it deserved a make over.

import pdfrw
import json
import pandas as pd
import os
import sys
import glob
from google.cloud import bigquery


def approveClient():
    with open("C:sample_dir/advisors.json", "r") as advisors:
        jdict = json.load(advisors)
    unqId = input("Please provide access code: ")
    try:
        creds = jdict[unqId]["credentials"]
        target_dir = jdict[unqId]["clientReviewPath"]
    except:
        print("access denied, invalid access code.")
        _2ndTry = input("try again? yes or no: ")
        if _2ndTry[0].lower() == "y":
            try:
                unqId_2 = input("Please enter access code: ")
                creds = jdict[unqId_2][credentials]
                target_dir = jdict[unqId_2]["clientReviewPath"]
            except:
                print("Invalid access code. Try again later.")
                sys.exit()
        else:
            sys.exit()
    return creds, target_dir
    
def getClientDF(query_string, user):
    queryData = user.query(query_string)
    df = queryData.to_dataframe()
    return df
    
def updateClientPDF(df, target_dir):

    ANNOT_KEY = '/Annots'
    ANNOT_NAME_KEY = '/Name'
    ANNOT_FIELD_KEY = '/T'
    ANNOT_VAL_KEY = '/V'
    ANNOT_RECT_KEY = 'Rect'
    SUBTYPE_KEY = '/Subtype'
    WIDGET_SUBTYPE_KEY = '/Widget'
    client_dict=df.set_index('name').to_dict()
    
    for name in client_dict.keys():
        individual_dict = client_dict[name]
        template_pdf = pdfrw.PdfReader("template_path/template.pdf").Root.AcroForm.update(
                        pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true'))
                    )
        
        for page in template_pdf.pages:
            annotations = page[ANNOT_KEY]
            
            for annotation in annotations:
                if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    if annotation[ANNOT_FIELD_KEY]:
                        annotKey = annotation[ANNOT_FIELD_KEY][1:-1]
                        if annotKey in individual_dict.keys():
                            annotation.update(
                                pdfrw.PdfDict(V="{}".format(individual_dict[annotKey]))
                            )       
                            annotation.update(pdfrw.PdfDict(AP=""))
                            
                        # PDF Template uses two separate name fields.
                        # FINRA Regs == Wary of updating template.
                        if annotKey == "Owner Name":
                            annotation.update(
                                pdfrw.PdfDict(V='{}'.format(individual_dict["name"]))
                            )
                            annotation.update(pdfrw.PdfDict(AP=""))
        name_ = individual_dict["Name"]
        output = os.path.join(target_dir, f"{name_}_Review.pdf")
        pdfrw.PdfWriter().write(output, template_pdf)


def main():
    qStr = """
        select
            Name, DateOfBirth, PhoneNum, Address,
            max(case when rn = 1 then AcctNum end) as Account_1,
            max(case when rn = 2 then AcctNum end) as Account_2,
            max(case when rn = 3 then AcctNum end) as Account_3,
            max(case when rn = 4 then AcctNum end) as Account_4)
        from (
            select
            Name,
            DateOfBirth,
            PhoneNum
            AcctNum,
            UpdatedThisQuarter,
            row_number() over (partition by Name order by AcctNum) as rn
            from client_info
        ) ci
        where UpdatedThisQuarter = 1
        group by Name;
    """
    creds, target_dir = approveClient()
    user = bigquery.Client.from_service_account_json(creds)
    df = getClientDF(qStr, user)
    updateClientPDF(df, target_dir)

    
if __name__ == '__main__':
    main()
