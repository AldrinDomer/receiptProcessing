#performs cleanup on the working folder, by moving the processed files 
# to a folder named with the timestamp

import glob, os
import shutil
import time
import read_config

timestamped_dir     = (read_config.get_parameter_values()[11]).format(os.getenv('username'),
                                                                      time.strftime("%Y%m%d-%H%M%S"))
converted_pdf       = (read_config.get_parameter_values()[14]).format(os.getenv('username'))
output_XML          = (read_config.get_parameter_values()[12]).format(os.getenv('username'))
scanned_PDFs        = (read_config.get_parameter_values()[10]).format(os.getenv('username'))
separated_receipts  = (read_config.get_parameter_values()[9]).format(os.getenv('username'))

#creates a folder in 
os.mkdir(timestamped_dir)


def cleanup():
    path_ls = [converted_pdf,output_XML,scanned_PDFs,separated_receipts]
        
    for path in path_ls:
        files = glob.glob(path)
        for file in files:
            shutil.move(file, timestamped_dir, copy_function = shutil.copytree)

        os.mkdir(path)

if __name__ == '__main__':
    cleanup()
