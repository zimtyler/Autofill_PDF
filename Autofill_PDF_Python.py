import pdfrw
import pandas as pd
import os
import glob
from google.cloud import bigquery
from google.cloud.bigquery import magics

ANNOT_KEY = '/Annots'
ANNOT_NAME_KEY = '/Name'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = 'Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

creds = getCredentials(name, json_path)
user = bigquery.Client.from_service_account_json(creds)

def getClientDF(query_string, user):
    queryData = user.query(query_string)
    df = queryData.to_dataframe()
    return df
    
def updateClientPDF(inCloud=True, input_path, output_path):
    template_pdf = pdfrw.PdfReader(input_pdf_path).Root.AcroForm.update(
            pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true'))
        )
    if inCloud:
        client_df = getClientDF()
    else
        client_csv = glob.glob(os.path.join(input_path, "client_csv.csv"))
        client_df = pd.read_csv(client_csv)
        # client_dict = client_df.to_dict("index")
        template_pdf = pdfrw.PdfReader(input_pdf_path).Root.AcroForm.update(
            pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true'))
        )
        name_list = client_df["name"].values.tolist()
        for name in args:
            i = name_list.index(name)
            individual_dict = client_dict[i]
            for page in template_pdf.pages:
                annotations = page[ANNOT_KEY]
                for annotation in annotations:
                    if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                        if annotation[ANNOT_FIELD_KEY]:
                            key = annotation[ANNOT_FIELD_KEY][1:-1]
                            if key in individual_dict.keys():
                                annotation.update(
                                    pdfrw.PdfDict(V="{}".format(individual_dict[key]))
                                )       
                                annotation.update(pdfrw.PdfDict(AP=""))
                            # PDF Template uses two separate name fields.
                            # FINRA Regs == Wary of updating template.
                            if key == "Owner Name":
                                annotation.update(
                                    pdfrw.PdfDict(V='{}'.format(individual_dict["Name"]))
                                )
                                annotation.update(pdfrw.PdfDict(AP=""))
            # template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
            pdfrw.PdfWriter().write("{} Review.pdf".format(individual_dict["Name"]), template_pdf)
    updateClientPDF("C:Automation_Projects")

def main():
    unqId = input("Please provide your unique access code: ")
    creds = getCredentials(unqId, json_path)
    user = bigquery.Client.from_service_account_json(creds)
    qStr = """
    select
        name, dob, phoneNum, address,
        max(case when rn = 1 then acctNum end) as Account_1,
        max(case when rn = 2 then acctNum end) as Account_2,
        max(case when rn = 3 then acctNum end) as Account_3,
        max(case when rn = 4 then acctNum end) as Account_4)
        from (
            select
            name,
            dob,
            phoneNum
            acctNum,
            row_number() over (partition by name order by acctNum) as rn
            from client_info) ci
    group by name
    order By name;
"""
    inCloud = input("Query? yes or no: ")
    inCloudBool = inClound.lower()[0] == "y"
    
    input_path = input("Provide path to directory containing template and/or csvs: ")
    output_path = input{"Provide desired output directory: ")
    updateClientPDF(inCloud=inCloudBool, input_path, output_path)
    
if __name__ == '__main__':
    main()
        
