from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
import shutil

class SpeciesScaper:
   def __init__(self):
      pass

   def GetData(self, url_):
      self.url = url_

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


      self.donotcheck = [  "zwarte_rotgans",
                           "flamingo",
                           "koereiger",
                           "zwarte_ibis",
                           "aalscholver",
                           "grote_aalscholver",
                           "kuhls_%7C_scopoli's_pijlstormvogel",
                           "pontische_meeuw",
                           "vale_pijlstormvogel",
                           "witwangstern",
                           "poelruiter",
                           "kleinste_jager",
                           "kleine_mantelmeeuw",
                           "baltische_mantelmeeuw",
                           "zwarte_zeekoet",
                           "steppekiekendief",
                           "middelste_bonte_specht",
                           "roodstuitzwaluw",
                           "cetti's_zanger",
                           "bergfluiter_%7C_balkanbergfluiter",
                           "siberische_tjiftjaf",
                           "sperwergrasmus",
                           "taigaboomkruiper",
                           "roze_spreeuw",
                           "westelijke_rosse_waaierstaart",
                           "blauwborst",
                           "roodsterblauwborst",
                           "siberische_boompieper",
                           "roodkeelpieper",
                           "roodmus",
                           "dwerggors",
                           "waterrrietzanger",
                           "oosterse_%7C_steppe-_%7C_vorkstaartplevier",
                           "kleine_burgemeester",
                           "orpheusspotvogel",
                           "amerikaanse_%7C_aziatische_goudplevier",
                           "bijeneter",
                           "gestreepte_strandloper",
                           "westelijke_%7C_moltoni's_%7C_balkanbaardgrasmus",
                           "oostelijke_%7C_westelijke_blonde_tapuit",
                           "bergfluiter_%7C_balkanbergfluiter",
                           "bastaardarend_%7C_schreeuwarend",
                           "kolgans",
                           "groenlandse_kolgans",
                           "grote_%7C_kleine_geelpootruiter",
                           "grote_%7C_kleine_grijze_snip",
                           "lachstern",
                           "buizerd",
                           "smelleken",
                           "ijslands_smelleken",
                           "steppebuizerd",
                           "turkestaanse_%7C_daurische_klauwier",
                           "langstaartklauwier_ssp_erythronotus",
                           "noordelijke_klapekster",
                           "siberische_noordelijke_klapekster",
                           "balearische_roodkopklauwier",
                           "diksnavelnotenkraker",
                           "noordse_%7C_swinhoes_boszanger",
                           "siberische_braamsluiper",
                           "vale_braamsluiper",
                           "koperwiek",
                           "ijslandse_koperwiek",
                           "aziatische_%7C_stejnegers_roodborsttapuit",
                           "zwarte_roodstaart",
                           "oosterse_zwarte_roodstaart",
                           "frater",
                           "britse_frater",
                           "groenlandse_witstuitbarmsijs",
                           "sneeuwgors",
                           "ijslandse_sneeuwgors",
                           "cassiarjunco",
                           "meenatortel",
                           "grutto",
                           "ijslandse_grutto",
                           "dwerggans",
                           "oehoe",
                           "kleine_canadese_gans"
                           "graszanger",
                           "grote_kruisbek",
                           "waterrrietzanger",
                           "humes_braamsluiper",
                           "atlantische_proven%C3%A7aalse_grasmus",
                           "dunbekwulp"]

      self.GetSpecies()
      self.FindAllData()

      self.CloseWebDriver()

   def ReadData(self):
         self.ReadDataFrame = pd.read_csv("data.csv")
         print(self.ReadDataFrame.head())

   def PlotAllData(self, month_, period):
      self.month = month_- 1
      self.period = period

      n_frames = len(self.ReadDataFrame)

      self.path = str(month_).zfill(2) + "-" + str(period)

      if os.path.exists("./" + self.path):
         shutil.rmtree("./" + self.path)
      os.mkdir("./" + self.path)

      shutil.copyfile("./main.tex", "./" + self.path + "/"+self.path+".tex")

      # Create latex file
      self.latexfile = open(self.path + "/fig.tex", "a")

      for i in range(n_frames):
         self.PlotData(self.ReadDataFrame.iloc[i])

      self.latexfile.close()

      command = "(cd " + self.path + "; pdflatex "+ self.path +".tex)"
      os.system(command)

   def PlotData(self, plotdf):
      # Transform data
      d0 = plotdf.Data0
      d0 = d0[1:-1].split(", ")
      d0 = [int(x) for x in d0]

      d1 = plotdf.Data1
      d1 = d1[1:-1].split(", ")
      d1 = [int(x) for x in d1]

      d2 = plotdf.Data2
      d2 = d2[1:-1].split(", ")
      d2 = [int(x) for x in d2]

      # Plotting criterium
      xm1 = 0.0
      xm2 = 0.0

      if self.period == 1:
         if self.month == 0:
            total = d2[-1]+d0[0]+d1[0]
         else:
            total = d2[self.month-1]+d0[self.month]+d1[self.month]

         xm1 = self.month - 0.3
         xm2 = self.month - 0.1

      elif self.period == 2:
         total = d0[self.month]+d1[self.month]+d2[self.month]
         xm1 = self.month - 0.1
         xm2 = self.month + 0.1

      elif self.period == 3:
         if self.month == 11:
            total = d1[-1] + d2[-1] + d0[0]
         else:
            total = d1[self.month] + d2[self.month] + d0[self.month+1]

         xm1 = self.month + 0.1
         xm2 = self.month + 0.3

      if total < 3:
         return

      print(plotdf.Filename + " - " + str(total))

      # Find maximum and total
      maxi = max([max(d0), max(d1), max(d2)])
      tot  = sum([sum(d0), sum(d1), sum(d2)])

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

      # Plot
      plt.figure(figsize=(8,3))
      plt.bar(X_axis - 0.2, d0, 0.2, label = ' 1-10')
      plt.bar(X_axis + 0.0, d1, 0.2, label = '11-20')
      plt.bar(X_axis + 0.2, d2, 0.2, label = '21-31')
      plt.axvline(x=xm1, linewidth=1.0, color='#d62728')
      plt.axvline(x=xm2, linewidth=1.0, color='#d62728')
      plt.xticks(X_axis, x_axis)
      plt.yticks(Y_axis)
      plt.title(plotdf.Title)
      plt.legend()
      plt.savefig(self.path +"/" +  plotdf.Filename)
      plt.close()


      self.latexfile.write('\n')
      self.latexfile.write('\\begin{wrapfigure}{r}{\\textwidth}\n')
      self.latexfile.write('\\includegraphics[width=0.4\\linewidth]{'+plotdf.Filename+'}\n')
      self.latexfile.write('\\end{wrapfigure}\n')

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

      self.DataFrame = pd.DataFrame()

      for i in indexrange:
         if(self.collectedNames[i] in self.donotcheck):
            print("Not checking " + self.collectedNamesPretty[i])
            continue

         print("[" + str(i+1) + "/" + str(self.nSpecies)+ "] " + str(self.collectedNamesPretty[i]))
         self.FindData(i)

      self.DataFrame.to_csv("data.csv", sep=',', index=False, encoding='utf-8')

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


      tot  = sum([sum(y_axis0), sum(y_axis1), sum(y_axis2)])


      title = self.collectedNamesPretty[index] + " (" + str(tot) + ")"
      if(cdna):
         title = title + " - Geen CDNA sinds: " + cdna

      # File name
      file_name = ''.join(filter(str.isalnum,self.collectedNames[index]))
      file_name = str(index+1).zfill(3) + "-" + file_name


      # Add to pandas dataframe
      new_data = {'Name':self.collectedNamesPretty[index], 'Title':title, 'Filename':file_name, 'Data0':y_axis0, 'Data1':y_axis1, 'Data2':y_axis2}

      self.DataFrame = pd.concat([self.DataFrame, pd.DataFrame([new_data])], ignore_index=True)



###########################################
import argparse
parser = argparse.ArgumentParser(description="My parser")

parser.add_argument('--new-data', dest='give_new_data', action='store_true')
parser.set_defaults(give_new_data=False)
args = parser.parse_args()

link = "https://www.dutchavifauna.nl/list"

speciesscraper = SpeciesScaper()

if(args.give_new_data):
   speciesscraper.GetData(link)


speciesscraper.ReadData()
for month_in in range(1,13):
   for period_in in range(1,4):
      speciesscraper.PlotAllData(month_in, period_in)