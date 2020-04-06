
import xlrd
import os 

#function definition for retrieving parameter 
#values in the config.xlsx file_path

def get_parameter_values():

	loc = r"C:\Users\{}\Desktop\ABBYY_OCR_SDK\UiPath\config.xlsx"
	wb = xlrd.open_workbook(loc.format(os.getenv("username")))
	sheet = wb.sheet_by_index(0)

	Country               =	sheet.cell_value(1,1)
	ImageSource           = sheet.cell_value(2,1)
	correctOrientation 	  = sheet.cell_value(3,1)
	correctSkew 		  = sheet.cell_value(4,1)
	ExtendedCharacterInfo = sheet.cell_value(5,1)
	fieldRegionExportMode = sheet.cell_value(6,1)

	ServerUrl 			  = sheet.cell_value(7,1)
	ApplicationId		  = sheet.cell_value(8,1)
	Password 			  = sheet.cell_value(9,1)

	#filePaths 
	separated_receipts    = sheet.cell_value(10,1)
	scanned_PDFs		  = sheet.cell_value(11,1)
	processed_files		  = sheet.cell_value(12,1)
	output_XML			  = sheet.cell_value(13,1)
	output_CSV			  = sheet.cell_value(14,1)
	converted_pdf         = sheet.cell_value(15,1)

	parameter_ls = [Country, ImageSource, correctOrientation, 
						correctSkew,ExtendedCharacterInfo, fieldRegionExportMode,
						ServerUrl, ApplicationId, Password, 
						separated_receipts,scanned_PDFs, processed_files, 
						output_XML, output_CSV,converted_pdf]

	return parameter_ls

if __name__ == "__main__":
	get_parameter_values()

