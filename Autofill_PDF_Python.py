import pdfrw
import pandas as pd


ANNOT_KEY = '/Annots'
ANNOT_NAME_KEY = '/Name'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = 'Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'


def autofill_bulk_pdf(input_pdf_path, client_csv):
    client_df = pd.read_csv(client_csv)
    client_dict = client_df.to_dict('index')
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    for x, y in client_dict.items():
        individual_dict = y
        for page in template_pdf.pages:
            annotations = page[ANNOT_KEY]
            for annotation in annotations:
                if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                    if annotation[ANNOT_FIELD_KEY]:
                        key = annotation[ANNOT_FIELD_KEY][1:-1]
                        if key in individual_dict.keys():
                            annotation.update(
                                pdfrw.PdfDict(V='{}'.format(individual_dict[key])))
                                
                            annotation.update(pdfrw.PdfDict(AP=''))
                            
                        '''For some reason, the PdfReader will not pull up an Annot if it is
                        listed more than once in the PDF. This also applies to 'exclusive or' 
                        check boxes. This is why I had to apply name to a different key ('Owner Name')'''
                       
                        if key == 'Owner Name':
                            annotation.update(
                                pdfrw.PdfDict(V='{}'.format(individual_dict['Name'])))
                                
                            annotation.update(pdfrw.PdfDict(AP=''))
        template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        pdfrw.PdfWriter().write('{} Review.pdf'.format(individual_dict['Name']), template_pdf)

autofill_bulk_pdf("C:Automation_Projects\Review_Form.pdf", "C:Automation_Projects\Client_Review_List_FINAL.csv")



def autofill_individual_pdf(input_pdf_path, client_csv, name):
    client_df = pd.read_csv(client_csv)
    client_dict = client_df.to_dict('index')
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    client_df = pd.read_csv(client_csv)
    name_list = client_df['Name'].values.tolist()
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
                            pdfrw.PdfDict(V='{}'.format(individual_dict[key])))
                                
                        annotation.update(pdfrw.PdfDict(AP=''))
                    if key == 'Owner Name':
                        annotation.update(
                            pdfrw.PdfDict(V='{}'.format(individual_dict['Name'])))
                                
                        annotation.update(pdfrw.PdfDict(AP=''))
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
    pdfrw.PdfWriter().write('{} Review.pdf'.format(individual_dict['Name']), template_pdf)

autofill_individual_pdf("C:Automation_Projects\Review_Form.pdf", "C:Automation_Projects\Client_Review_List_FINAL.csv", "John Doe")

def update_multiple_pdf(input_pdf_path, client_csv, *args):
    client_df = pd.read_csv(client_csv)
    client_dict = client_df.to_dict('index')
    template_pdf = pdfrw.PdfReader(input_pdf_path)
    client_df = pd.read_csv(client_csv)
    name_list = client_df['Name'].values.tolist()
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
                                pdfrw.PdfDict(V='{}'.format(individual_dict[key])))
                                    
                            annotation.update(pdfrw.PdfDict(AP=''))
                        if key == 'Owner Name':
                            annotation.update(
                                pdfrw.PdfDict(V='{}'.format(individual_dict['Name'])))
                                    
                            annotation.update(pdfrw.PdfDict(AP=''))
        template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))
        pdfrw.PdfWriter().write('{} Review.pdf'.format(individual_dict['Name']), template_pdf)
update_multiple_pdf("C:Automation_Projects\Review_Form.pdf", "C:Automation_Projects\Client_Review_List_FINAL.csv", "John Doe")
    
