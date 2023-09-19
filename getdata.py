from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import matplotlib.pyplot as plt
import numpy as np




class SpeciesScaper:
   def __init__(self, url_, month_, firsthalve_):
      self.url = url_
      self.month = month_- 1
      self.firsthalve = firsthalve_

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
      self.browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

   def CloseWebDriver(self):
      self.browser.quit()

   def GetSpecies(self):
      self.browser.get(self.url)
      links = self.browser.find_elements(By.TAG_NAME, "a")

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
         print("[" + str(i+1) + "/" + str(self.nSpecies)+ "] " + str(self.collectedNamesPretty[i]))
         self.FindData(i)

   def FindData(self, index):
      link = self.collectedLinks[index]
      self.browser.get(link)

      # Find date until considered by CDNA
      cdna = self.browser.find_elements(By.XPATH,
         "//p[@class='right'][@style='text-align: right; clear: right;']")

      if len(cdna)>0: # avoid bug in dutchavifauna
         cdna = cdna[0].text

         if (cdna.find("beoordeelsoort: nee") > 0):
            cdna = cdna.split("laatste jaar beoordeeld door CDNA: ")
            if len(cdna)>1:
               cdna = cdna[1]
            else:
               cdna = None
         else:
            cdna = None
      else:
         cdna = None

      # Find case data per ten days
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

      # Find maximum and total
      maxi = max([max(y_axis0), max(y_axis1), max(y_axis2)])
      tot  = sum([sum(y_axis0), sum(y_axis1), sum(y_axis2)])

      # Choose lenght of y tiks
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

      x_axis = [ "Jan", "Feb", "Maa", "Apr", "Mei", "Jun",
                 "Jul", "Aug", "Sep", "Okt", "Nov", "Dec"]
      # Tiks
      Y_axis = range(0, maxi+1, step)
      X_axis = np.arange(len(x_axis))

      title = self.collectedNamesPretty[index] + " (" + str(tot) + ")"
      if(cdna):
         title = title + " - Geen CDNA sinds: " + cdna

      # File name
      file_name = ''.join(filter(str.isalnum,self.collectedNames[index]))
      file_name = str(index+1).zfill(3) + "-" + file_name


      # Month markers
      xm1 = self.month
      xm2 = self.month
      if (firsthalve==True):
         xm1 = xm1 - 0.3
         xm2 = xm2 + 0.1
      else:

         xm1 = xm1 - 0.1
         xm2 = xm2 + 0.3

      # Plot
      plt.figure(figsize=(8,3))
      plt.bar(X_axis - 0.2, y_axis0, 0.2, label = ' 1-10')
      plt.bar(X_axis + 0.0, y_axis1, 0.2, label = '11-20')
      plt.bar(X_axis + 0.2, y_axis2, 0.2, label = '21-31')
      #plt.axvline(x=xm1, ymin = 0.0, ymax=0.1, color='#d62728')
      #plt.axvline(x=xm2, ymin = 0.0, ymax=0.1, color='#d62728')
      plt.axvline(x=xm1, linewidth=1.0, color='#d62728')
      plt.axvline(x=xm2, linewidth=1.0, color='#d62728')
      plt.xticks(X_axis, x_axis)
      plt.yticks(Y_axis)
      plt.title(title)
      plt.legend()
      plt.savefig(file_name)
      plt.close()


###########################################
link = "https://www.dutchavifauna.nl/list"
month = 10
firsthalve = True
speciesscraper = SpeciesScaper(link, month, firsthalve)