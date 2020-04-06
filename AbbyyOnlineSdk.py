import shutil
import xml.dom.minidom
import json
import xlrd
import os
import read_config

try:
	import requests
except ImportError:
	print("You need the requests library to be installed in order to use this sample.")
	print("Run 'pip install requests' to fix it.")

	exit()


class ProcessingSettings:
	#Language = "English,Japanese"
	#OutputFormat = "docx"
	Country               =	str(read_config.get_parameter_values()[0]).replace(" ","")
	ImageSource           = str(read_config.get_parameter_values()[1])
	correctOrientation 	  = str(read_config.get_parameter_values()[2])
	correctSkew 		  = str(read_config.get_parameter_values()[3])
	ExtendedCharacterInfo = str(read_config.get_parameter_values()[4])
	fieldRegionExportMode = str(read_config.get_parameter_values()[5])


class Task:
	Status = "Unknown"
	Id = None
	DownloadUrl = None

	def is_active(self):
		if self.Status == "InProgress" or self.Status == "Queued":
			return True
		else:
			return False


class AbbyyOnlineSdk:
	# Warning! This is for easier out-of-the box usage of the sample only. Change to https://
	#  for production use. Change to http://cloud-westus.ocrsdk.com if you created your 
	#  application in US location
	ServerUrl = str(read_config.get_parameter_values()[6])

	# To create an application and obtain a password,
	# register at https://cloud.ocrsdk.com/Account/Register
	# More info on getting your application id and password at
	# https://ocrsdk.com/documentation/faq/#faq3
	ApplicationId = str(read_config.get_parameter_values()[7])
	Password = str(read_config.get_parameter_values()[8])

	Proxies = {
	
		}

	def process_image(self, file_path, settings):

		url_params = {
			"country"						:	settings.Country,
			"ImageSource"					: 	settings.ImageSource,
			"correctOrientation"			:   settings.correctOrientation,
			"correctSkew"					:	settings.correctSkew,
			"xml:writeExtendedCharacterInfo":	settings.ExtendedCharacterInfo,
			"xml:fieldRegionExportMode"     :   settings.fieldRegionExportMode
		}

	
		request_url = self.get_request_url("v2/processReceipt")

		with open(file_path, 'rb') as image_file:
			image_data = image_file.read()

		#s = requests.Session()
		response = requests.post(request_url, data=image_data, params=url_params,
								 auth=(self.ApplicationId, self.Password), proxies=self.Proxies)

		# Any response other than HTTP 200 means error - in this case exception will be thrown
		response.raise_for_status()

		# parse response xml and extract task ID
		task = self.decode_response_JSON(response.text)
		return task

	def get_task_status(self, task):
		if task.Id.find('00000000-0') != -1:
			# GUID_NULL is being passed. This may be caused by a logical error in the calling code
			print("Null task id passed")
			return None

		url_params = {"taskId": task.Id}
		status_url = self.get_request_url("v2/getTaskStatus")

		#s = requests.Session()
		response = requests.get(status_url, params=url_params,
								auth=(self.ApplicationId, self.Password), proxies=self.Proxies)

		task = self.decode_response_JSON(response.text)
		return task

	def download_result(self, task, output_path):
		get_result_url = task.DownloadUrl
		if get_result_url is None:
			print("No download URL found")
			return

		file_response = requests.get(get_result_url, stream=True, proxies=self.Proxies)
		with open(output_path, 'wb') as output_file:
			shutil.copyfileobj(file_response.raw, output_file)

	#original function definition below (from the sample ABBYY code);
	#this is for parsing the HTTP request for the v1\processReceipt API
	def decode_response(self, xml_response):
		""" Decode xml response of the server. Return Task object """
		dom = xml.dom.minidom.parseString(xml_response)
		task_node = dom.getElementsByTagName("task")[0]

		task = Task()
		task.Id = task_node.getAttribute("id")
		task.Status = task_node.getAttribute("status")
		if task.Status == "Completed":
			task.DownloadUrl = task_node.getAttribute("resultUrl")
		return task

	#added function definition for parsing the HTTP request for v2/processReceipt API
	def decode_response_JSON (self, json_response):
		parsed_json = json.loads(json_response)
		print (parsed_json)
		task = Task()
		task.Id = parsed_json["taskId"]
		task.Status = parsed_json["status"]
		print("Task ID :" + str(task.Id),"Task status: " + str(task.Status))

		if task.Status == "Completed":
			task.DownloadUrl = parsed_json["resultUrls"][0]
			print("Task URL: " + str(task.DownloadUrl))
		return task


	def get_request_url(self, url):
		return self.ServerUrl.strip('/') + '/' + url.strip('/')
