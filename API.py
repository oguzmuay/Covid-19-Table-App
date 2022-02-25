import requests
province = ['ALA Aland Islands', 'American Samoa', 'Anguilla', 'Antarctica', 'Aruba', 'Bermuda', 'Bouvet Island',
            'British Indian Ocean Territory', 'British Virgin Islands', 'Cayman Islands',
            'Christmas Island', 'Cocos (Keeling) Islands', 'Cook Islands', 'Falkland Islands (Malvinas)',
            'Faroe Islands', 'French Guiana', 'French Polynesia', 'French Southern Territories',
            'Gibraltar', 'Greenland', 'Guadeloupe', 'Guam', 'Guernsey', 'Heard and Mcdonald Islands',
            'Hong Kong, SAR China', 'Isle of Man', 'Jersey', 'Kiribati', 'Korea (North)',
            'Macao, SAR China', 'Marshall Islands', 'Martinique', 'Mayotte', 'Micronesia, Federated States of',
            'Montserrat', 'Nauru', 'Netherlands Antilles', 'New Caledonia', 'Niue',
            'Norfolk Island', 'Northern Mariana Islands', 'Palau', 'Pitcairn', 'Puerto Rico', 'Réunion', 'Saint Helena',
            'Saint Pierre and Miquelon', 'Saint-Barthélemy', 'Saint-Martin (French part)',
            'Samoa', 'Solomon Islands', 'South Georgia and the South Sandwich Islands',
            'Svalbard and Jan Mayen Islands', 'Tokelau', 'Tonga', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu',
            'US Minor Outlying Islands', 'Vanuatu', 'Virgin Islands, US',
            'Wallis and Futuna Islands']  # Bolgelerin listesi
# Kullandigim api ULKELERI verirken ulkelerin bolgelerinide veriyordu ancak apida bolgeler bos bir liste dondurdugu
# icin ulkeleri donduren api kullanarak cektigim listeden <PROVINCE> listesini cikardim. Ulkeleride bir kere cekip
# listeye kaydedebilirdim ancak api kullanarak cekme fikri daha hos geldi belki yeni ulke eklerler...
def countryDataGettting():
    try:
        response = requests.get("https://api.covid19api.com/countries")
        jsonFile = response.json()
        countryDict = []
        for i in jsonFile:
            countryDict.append(i["Country"])
        return [x for x in sorted(countryDict) if x not in province]
    except:
        raise

# Baslangicta ulkeleri teker teker cekip bolgeleri cikarmak cok zaman aldigi icin bu fonksiyonla butun bolgeleri bir listeye aldim.
def countryProvinceGetting(countries):
    province = []
    for i in countries:
        defaultURL = "https://api.covid19api.com/dayone/country/"
        requestURL = defaultURL + countrySlugGetting(i)
        response = requests.get(requestURL)
        if response.json() == []:# Bolge verilerinin bos bir liste dondurdugunu farkettim.Ben de bos liste dondurenleri yukaridaki listeye kaydetmek icin bir kez aldim.
            province.append(i)
    print("BITTI")

# Verdigim ulke kodu ve veri tipiyle bir URL hazirlayip URL'nin gonderdigi vaka sayisilari verisini bir liste haline getirip donduren fonksiyon.
def covidCaseDataGetting(slug, status):
    defaultURL = "https://api.covid19api.com/dayone/country/"
    if status[0:5] == "daily":
        if status[6:len(status)] == "active":
            requestURL = defaultURL+str(slug)# Aktif verilerinde sikinti oldugu icin eger ki [ACTIVE] verisi istenirse farkli bir sekilde veriler aliniyor.
        else:
            requestURL = defaultURL + str(slug) + "/status/" + str(status[6:len(status)])
    else:
        if status == "active":
            requestURL = defaultURL + str(slug)
        else:
            requestURL = defaultURL + str(slug) + "/status/" + str(status)
    try:
        response = requests.get(requestURL)
        jsonFile = response.json()
        caseData = []
        if status == "active" or status[6:len(status)] == "active":
            for i in jsonFile:
                provinceData = {}
                if i["Province"] != "":
                    provinceData["Province"] = i["Province"]
                    provinceData["Cases"] = i["Active"]
                    caseData.append(provinceData)
                # API 'da bazi bolgeleri olan ulkelerin sadece bolge bilgilerini verirken bazilarinda ise hem bolge
                # hem de genel verilerini vermisler.Iclerinde genel verilerin oldugu ulkeler benim yazdigim sistemi
                # bozdugu icin boldugum cozum.
                elif i["Country"] != "United Kingdom" and i["Country"] != "Canada" \
                        and i["Country"] != "Denmark" and i["Country"] != "United States of America":
                    caseData.append(i["Active"])
        else:
            for i in jsonFile:
                provinceData = {}
                if i["Province"] != "":
                    provinceData["Province"] = i["Province"]
                    provinceData["Cases"] = i["Cases"]
                    caseData.append(provinceData)
                # API 'da bazi bolgeleri olan ulkelerin sadece bolge bilgilerini verirken bazilarinda ise hem bolge
                # hem de genel verilerini vermisler.Iclerinde genel verilerin oldugu ulkeler benim yazdigim sistemi
                # bozdugu icin buldugum cozum.
                elif i["Country"] != "United Kingdom" and i["Country"] != "Canada" and\
                        i["Country"] != "Denmark" and i["Country"] != "United States of America":
                    caseData.append(i["Cases"])
        print("Vaka Verileri Alindi.")
        return caseData
    except:
        print("Vaka Degerleri Alinamadi")

# Verdigim ulke kodu ve veri tipiyle bir URL hazirlayip URL'nin gonderdigi gunlerin verisini bir liste haline getirip donduren fonksiyon.
def covidDateDataGetting(slug, status):
    defaultURL = "https://api.covid19api.com/dayone/country/"
    if status[0:5] == "daily":
        if status[6:len(status)] == "active":
            requestURL = defaultURL + str(slug)# Aktif verilerinde sikinti oldugu icin eger ki [ACTIVE] verisi istenirse farkli bir sekilde veriler aliniyor.
        else:
            requestURL = defaultURL + str(slug) + "/status/" + str(status[6:len(status)])
    else:
        if status == "active":
            requestURL = defaultURL + str(slug)
        else:
            requestURL = defaultURL + str(slug) + "/status/" + str(status)
    try:
        response = requests.get(requestURL)
        jsonFile = response.json()
        dateData = []
        for i in jsonFile:
            provinceData = {}
            if i["Province"] != "":
                provinceData["Province"] = i["Province"]
                provinceData["Date"] = i["Date"][6:10]
                dateData.append(provinceData)
            # API 'da bazi bolgeleri olan ulkelerin sadece bolge bilgilerini verirken bazilarinda ise hem bolge
            # hem de genel verilerini vermisler.Iclerinde genel verilerin oldugu ulkeler benim yazdigim sistemi
            # bozdugu icin boldugum cozum.
            elif i["Country"] != "United Kingdom" and i["Country"] != "Canada" \
                    and i["Country"] != "Denmark" and i["Country"] != "United States of America":
                dateData.append(i["Date"][6:10])
        print("Tarih Verileri Alindi.")
        return dateData
    except:
        raise
        print("Tarih Degerleri alinamadi")

# Veri cekerken kullandigim URL'lerde kullanmak icin ulke slug'i donduren fonksiyon.
def countrySlugGetting(country):
    try:
        response = requests.get("https://api.covid19api.com/countries")
        jsonFile = response.json()
        for i in jsonFile:
            if (i["Country"] == country):
                print("Ulke Kod Verisi Alindi.")
                return i["Slug"]
    except:
        print("Ulke Kodu Alinamadi")

# Ana sayfadaki verilerin hepsini donduren fonksiyon.
def summaryDataGetting():
    try:
        data = []
        response = requests.get("https://api.covid19api.com/summary")
        jsonFile = response.json()
        dict = {}
        dict["Country"] = "Global"
        for i in jsonFile["Global"]:
            dict[i] = jsonFile["Global"][str(i)]
        data.append(dict)
        for i in jsonFile["Countries"]:
            dict = {}
            for j in i:
                if str(j) != "CountryCode" and str(j) != "Slug" and str(j) != "Date": #Sadece vaka verilerini eklemek icin filtreleme
                    dict[str(j)] = i[str(j)]
            data.append(dict)
        return data
    except:
        raise
        print("Genel Bilgi Alinamadi")

#summaryDataGetting()
#countryDataGettting()
#covidCaseDataGetting("united-kingdom", "confirmed")
#covidDateDataGetting("china", "confirmed")
#countryProvinceGetting(countryDataGettting())