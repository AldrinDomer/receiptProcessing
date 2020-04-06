import os
import process
import subprocess
import receipt_separation
import time
import read_config

receipt_dir = (read_config.get_parameter_values()[9]).format(os.getenv('username'))
xml_dir = (read_config.get_parameter_values()[12]).format(os.getenv('username'))

os.chdir(receipt_dir)
processor = None

def applyOCR():
    file_counter = 1
    time.sleep(10)
    for jpg_file in os.listdir(receipt_dir):
        if jpg_file.endswith(".jpg") or jpg_file.endswith(".pdf"):
            output_path = os.path.join(xml_dir,'{}.xml'.format(file_counter))
            process.main(jpg_file, output_path )
        file_counter += 1

if __name__ == "__main__":
    print("Applying ABBYY OCR SDK...")
    applyOCR()
    print("")
