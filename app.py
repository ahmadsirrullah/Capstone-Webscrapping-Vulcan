from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#membuat link untuk menarik 15 halaman
url_list = []
url = 'https://www.kalibrr.id/job-board/te/data/'
for hlm in range(1,16): 
    url_new = url+str(hlm)
    url_list.append(url_new)

temp = [] #initiating a list

for i in url_list:
    #insert the scrapping here
	url_get = requests.get(i)
	soup = BeautifulSoup(url_get.content,"html.parser")
    #find your right key here
	table = soup.find('div', attrs = {'class': "k-border-b k-border-t k-border-tertiary-ghost-color md:k-border md:k-overflow-hidden md:k-rounded-lg"})
	row = table.find_all('a', attrs={'itemprop':"name"})
	row_length = len(row)
	for i in range(0, row_length):
        #scrapping process
        #title pekerjaan
		title = table.find_all('a', attrs={'itemprop':"name"})[i].text
        #lokasi perusahaan
		lokasi = table.find_all('a', attrs={"class": "k-text-subdued k-block"})[i].text
		lokasi = lokasi.strip()
        #tanggal pekerjaan di post dan dealine submit permohonan
		postNdl = table.find_all('span', attrs={'class' : 'k-block k-mb-1'})[i].text
		postNdl = postNdl.strip()
        #perusahaan
		perusahaan = table.find_all('span', attrs={'class' : 'k-inline-flex k-items-center k-mb-1'})[i].text
		temp.append((title, lokasi, postNdl, perusahaan))
    
temp

#change into dataframe
df = pd.DataFrame(temp, columns = ('title','lokasi','post_and_deadline', 'perusahaan'))
df.head()

#insert data wrangling here
	#1 Menyamakan semua nama Jakarta Selatan, Indonesia
df.replace("South Jakarta, Indonesia","Jakarta Selatan, Indonesia", inplace = True)
df.replace("Kota Jakarta Selatan, Indonesia","Jakarta Selatan, Indonesia", inplace = True)
df.replace("South Jakarta City, Indonesia","Jakarta Selatan, Indonesia", inplace = True)
	#2 Menyamakan semua nama Jakarta Pusat, Indonesia
df.replace("Central Jakarta, Indonesia","Jakarta Pusat, Indonesia", inplace = True)
df.replace("Kota Jakarta Pusat, Indonesia","Jakarta Pusat, Indonesia", inplace = True)
df.replace("Central Jakarta City, Indonesia","Jakarta Pusat, Indonesia", inplace = True)
	#3 Menyamakan semua nama Jakarta Barat, Indonesia
df.replace("Kota Jakarta Barat, Indonesia","Jakarta Barat, Indonesia", inplace = True)
df.replace("West Jakarta, Indonesia","Jakarta Barat, Indonesia", inplace = True)
df.replace("West Jakarta City, Indonesia","Jakarta Barat, Indonesia", inplace = True)
	#4 Menyamakan semua nama Jakarta Timur, Indonesia
df.replace("Kota Jakarta Timur, Indonesia","Jakarta Timur, Indonesia", inplace = True)
df.replace("East Jakarta, Indonesia","Jakarta Timur, Indonesia", inplace = True)
df.replace("East Jakarta City, Indonesia","Jakarta Timur, Indonesia", inplace = True)
	#5 Menyamakan semua nama Jakarta Utara, Indonesia
df.replace("Kota Jakarta Utara, Indonesia","Jakarta Utara, Indonesia", inplace = True)
df.replace("North Jakarta, Indonesia","Jakarta Utara, Indonesia", inplace = True)
df.replace("North Jakarta City, Indonesia","Jakarta Utara, Indonesia", inplace = True)
	#6 Menyamakan semua nama Tangerang Selatan, Indonesia
df.replace("South Tangerang, Indonesia","Tangerang Selatan, Indonesia", inplace = True)
	#7 Menghilangkan tanda "," dan kata "Indonesia" pada kolom "lokasi"
df.replace({', Indonesia': ''}, regex = True, inplace = True)
	#8 Membuat tabel agregasi lokasi dengan jumlah pekerjaan yang tersedia
df_groupping = pd.crosstab(
    index = df['lokasi'],
    columns = 'Jumlah Lowongan'
).sort_values(by = 'Jumlah Lowongan')
#end of data wranggling 

@app.route("/")
def index(): 
	
	card_data = f'{df_groupping["Jumlah Lowongan"].sum()}' #be careful with the " and ' 

	# generate plot
	ax = df_groupping.plot(kind = 'barh', ylabel = '', figsize = (20,9)) 
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		card_data = card_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)