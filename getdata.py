from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import matplotlib.pyplot as plt
import numpy as np

class SpeciesScaper:
   def __init__(self, url_):
      self.url = url_
      self.pathdriver = "/home/jelotz/prog/chromedriver/chromedriver"
      self.collectedLinks = []
      self.collectedNames = []
      self.collectedNamesPretty = []
      self.nSpiecies = 0;

      self.chrome_options = Options()
      self.chrome_options.add_argument("--disable-extensions")
      self.chrome_options.add_argument("--disable-gpu")
      self.chrome_options.add_argument("--no-sandbox") # linux only
      self.chrome_options.add_argument("--headless")

      self.CreateWebDriver()
      self.GetSpecies()
      
      self.FindAllData()


      self.CloseWebDriver()

   def CreateWebDriver(self):
      #self.browser = webdriver.Chrome(executable_path = self.pathdriver, options = self.chrome_options)
      self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

   def CloseWebDriver(self):
      self.browser.quit()

   def GetSpecies(self):
   	self.browser.get(self.url)
   	links = self.browser.find_elements(By.TAG_NAME, "a")

   	i = 0

   	for elem in links:
   		href = elem.get_attribute("href")
   		hrefstr = str(href)

   		find1 = hrefstr.find("species")
   		find2 = hrefstr.find("?")
 
   		if find1>0 and find2<1:
   			self.collectedLinks.append(href)
   			self.collectedNames.append(hrefstr.split("species/")[1])
   			self.collectedNamesPretty.append(elem.text)

   	self.nSpecies = len(self.collectedNames)

   def FindAllData(self):
   	indexrange = range(0, self.nSpecies, 1)
   	for i in indexrange:
   		if(i==61):
   			# Avoid bug in dutchavifauna.nl
   			continue
   		print("[" + str(i) + "/" + str(self.nSpecies)+ "] " + str(self.collectedNamesPretty[i]))
   		self.FindData(i)

   def FindData(self, index):
   	link = self.collectedLinks[index]
   	self.browser.get(link)

   	scripts = self.browser.find_elements(By.TAG_NAME, "script")

   	for script in scripts:
   		innerHTML = script.get_attribute("innerHTML")
   		if innerHTML.find("decades.addRows")>0:
   			datas = innerHTML

   	datas = datas.split("decades.addRows([\n")[1].split("\n])")[0].split(",\n")

   	y_axis0 = []
   	y_axis1 = []
   	y_axis2 = []

   	for data in datas:
   		data = data[1:-1].split(", ")[1:]

   		y_axis0.append(int(data[0]))
   		y_axis1.append(int(data[1]))
   		y_axis2.append(int(data[2]))

   	x_axis=[ "Jan", "Feb", "Maa", "Apr", "Mei", "Jun",
   	         "Jul", "Aug", "Sep", "Okt", "Nov", "Dec"]

   	maxi = max([max(y_axis0), max(y_axis1), max(y_axis2)])

   	if(maxi<5):
   		step = 1
   	elif(maxi<11):
   		step = 2
   	elif(maxi<20):
   		step = 4
   	elif(maxi<30):
   		step = 5
   	elif(maxi<60):
   		step = 10;
   	else:
   		step = 20

   	# Tiks
   	Y_axis = range(0, maxi+1, step)
   	X_axis = np.arange(len(x_axis))

  		# Plot
   	plt.figure(figsize=(8,3))
   	plt.bar(X_axis - 0.2, y_axis0, 0.2, label = ' 1-10')
   	plt.bar(X_axis + 0.0, y_axis1, 0.2, label = '11-20')
   	plt.bar(X_axis + 0.2, y_axis2, 0.2, label = '21-31')
   	plt.xticks(X_axis, x_axis)
   	plt.yticks(Y_axis)
   	plt.title(self.collectedNamesPretty[index])
   	plt.legend()
   	plt.savefig(self.collectedNames[index])
   	plt.close()
   	#plt.show()


###########################################
link = "https://www.dutchavifauna.nl/list"
speciesscraper = SpeciesScaper(link)