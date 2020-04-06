
import os
import xml.etree.ElementTree as ET
import pandas as pd
from io import StringIO
import time
import read_config

xml_dir = (read_config.get_parameter_values()[12]).format(os.getenv('username'))
csv_dir = (read_config.get_parameter_values()[13]).format(os.getenv('username'))

os.chdir(xml_dir)

data_lst = []

def parse_and_save():
    for xml_file in os.listdir(xml_dir):
        if xml_file.endswith(".xml"):
            tree = ET.parse(xml_file)
            root = tree.getroot()

            namespace = {'xmlns': 'https://www.abbyy.com/ReceiptCaptureSDK_xml/ReceiptCapture-1.1.xsd'}

            for element in root.findall('xmlns:receipt', namespace):
                #print (element.tag, element.attrib)
                try:
                    vendor_name = element.find("xmlns:vendor/xmlns:name/xmlns:recognizedValue/xmlns:text", namespace).text
                    vendor_contact = element.find("xmlns:vendor/xmlns:phone/xmlns:normalizedValue", namespace).text
                    transaction_date = element.find("xmlns:date/xmlns:normalizedValue", namespace).text
                    transaction_time = element.find("xmlns:time/xmlns:normalizedValue", namespace).text
                    transaction_total = element.find("xmlns:total/xmlns:normalizedValue", namespace).text

                    field_summary = [xml_file, vendor_name, vendor_contact, transaction_date,
                                       transaction_time, transaction_total]

                    data_lst.append(field_summary)

                except AttributeError:
                    break

    columns = ['XML File', 'Vendor', 'Contact No.', 'Date', 'Time', 'Total']
    df = pd.DataFrame(data_lst)
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    print("Succesfully parsed XML.")
    #print(df)
    print(" ")
    print("XML files successfully parsed and saved as a CSV file")
    df.to_csv(os.path.join(csv_dir, "{}.csv".format(str(timestamp))), encoding='utf-8', header = columns, index = False)

if __name__ == '__main__':
    print("")
    print("Parsing XML files into CSV....")
    print("")
    parse_and_save()
    print("")
    print("Process complete.")
