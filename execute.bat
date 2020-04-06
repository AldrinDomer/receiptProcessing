@echo off 

echo -------------------------------------------------------
echo  Automated Receipt Processing with ABBYY Cloud OCR SDK 
echo -------------------------------------------------------

echo     1.Setting up automation environment...
::add poppler file path to system PATH for while the cmd session is open 
PATH %PATH%;%USERPROFILE%\Desktop\ABBYY_OCR_SDK\project_setup\poppler-0.68.0\ >logs.txt

::upgrade pip
py -m pip install --upgrade pip >> logs.txt

::install necessary Python libraries
pip install --user --requirement "%USERPROFILE%\Desktop\ABBYY_OCR_SDK\ABBYY_working_folders\python_files\requirements.txt" >>logs.txt

echo     2.Applying receipt separation...

"%USERPROFILE%\AppData\Local\Programs\Python\Python38\python.exe" "%USERPROFILE%\Desktop\ABBYY_OCR_SDK\ABBYY_working_folders\python_files\receipt_separation.py" >>logs.txt

echo     3.Uploading each file to ABBYY OCR SDK...
echo           (This may take a while)

"%USERPROFILE%\AppData\Local\Programs\Python\Python38\python.exe" "%USERPROFILE%\Desktop\ABBYY_OCR_SDK\ABBYY_working_folders\python_files\applyOCR.py" >>logs.txt

echo     4.Parsing output XML files and saving data to CSV...

"%USERPROFILE%\AppData\Local\Programs\Python\Python38\python.exe" "%USERPROFILE%\Desktop\ABBYY_OCR_SDK\ABBYY_working_folders\python_files\parseXML_sendToCSV.py" >>logs.txt


echo Process complete.
echo Performing cleanup for next run...

"%USERPROFILE%\AppData\Local\Programs\Python\Python38\python.exe" "%USERPROFILE%\Desktop\ABBYY_OCR_SDK\ABBYY_working_folders\python_files\cleanup.py" >>logs.txt

