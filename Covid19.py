import API as api
from tkinter import *
from tkinter import ttk, font, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib

matplotlib.use("TkAgg")

dataSelection = ["Confirmed", "Deaths", "Recovered", "Active",
                 "Daily Confirmed", "Daily Deaths", "Daily Recovered", "Daily Active"]  # Secilecek veri tipleri
currentProvinces = []  # Secilmis eyaletler.
previousProvinces = []
currentXData = []  # Tarih degerlerinin tutuldugu liste.
currentYData = []  # Istenilen veri tipine gore vaka sayilarinin tutuldugu liste.
currentCountryProvinces = []  # Secilen ulkenin eyaletleri mevcutsa tutuldugu liste.
currentCountry = ""  # Suan secilen ulke.
currentDataType = ""  # Suna secilen veri tipi.
previousCountry = ""  # Tabloyu ayni verilerle tekrar tekrar cizmemek icin suanki ulkeyle karsilastirmak icin.
previousDataType = ""  # Tabloyu ayni verilerle tekrar tekrar cizmemek icin suanki veri tipiyle karsilastirmak icin.
previousCountryProvinces = []  # Tabloyu ayni bolgelerle tekrar tekrar cizmemek icin suanki bolgelerle
# karsilastirmak icin.

chartData = []  # Ilk cikan tablonun verilerinin saklandigi liste.
chartCurrentItem = None  # Tablodan secilen ulke.


def chartCountryShow(a):  # Tabloda ustune tiklanan ulkenin verilerini alan fonksiyon.
    global chartCurrentItem
    if str(chart.focus()) != "":
        chartCurrentItem = chart.item(chart.focus())
        countryNameLabel.config(text=chartCurrentItem["text"].split(" ")[1:])
        totalConfirmedLabel.config(text=chartCurrentItem["values"][0])
        totalDeathsLabel.config(text=chartCurrentItem["values"][1])
        totalRecoveredLabel.config(text=chartCurrentItem["values"][2])
        newConfirmedLabel.config(text=chartCurrentItem["values"][3])
        newDeathsLabel.config(text=chartCurrentItem["values"][4])
        newRecoveredLabel.config(text=chartCurrentItem["values"][5])
        openSpecificCountryFrame()


def chartSort(a):  # Tablo verilerini siralayan fonsiyon.
    global chartData
    chart.selection_clear()
    if a == "#0":
        chartData = (sorted(chartData, key=lambda i: i['Country']))
    else:
        chartData = (sorted(chartData, key=lambda i: i[a], reverse=True))
    chart.delete(*chart.get_children())
    chartWrite(chartData)


def chartDataGetting():  # Tablodaki verileri ceken fonksiyon.
    global chartData
    chartData = api.summaryDataGetting()


def chartWrite(data):  # Tabloya elamanlari ekleyen fonksiyon.
    count = 0
    for i in data:
        chart.insert("", "end", "item" + str(count), text="#" + str(count) + " " + i["Country"], values=(
            i["TotalConfirmed"], i["TotalDeaths"],
            i["TotalRecovered"], i["NewConfirmed"],
            i["NewDeaths"], i["NewRecovered"]))
        count += 1


def chartPlotSave():  # Tablodan secilen ulkenin grafigini kaydeden fonksiyon.
    chartFigure.savefig(str(chartCurrentItem["text"].split(" ")[2:]) + "ChartPlot.png")
    print("Grafik kaydedildi.")


def graphPlotSave():  # Grafigi cizilen ulkenin grafigini kaydeden fonksiyon.
    figure.savefig(str(currentCountry) + "GraphPlot.png")
    print("Grafik kaydedildi.")


def infoButtonGraph():  # Grafik bilgi mesajini gosteren fonksiyon.
    messagebox.showinfo(title="Tablo Bilgilendirme", message="-Sağ üstteki oktan tablo ekranına geri dönebilirsiniz.\n"
                                                             "-Bir ülke ve bir veri türü sectikten sonra [DRAW] tuşuna "
                                                             "bastığınızda ülkeninin bölgeleri yoksa direkt ilk 10 "
                                                             "günün verilerini görebilirsiniz.Varsa açılan PROVINCE "
                                                             "sekmesinden en fazla üç tane bölge seçtikten sonra DRAW "
                                                             "tuşuna basarak görebilirsiniz.\n-Alttaki çubuğun sağ ve "
                                                             "sol tarafındaki listelerden görmek istediğiniz tarih "
                                                             "aralığını başlagıç-bitiş şeklinde seçebilirsiniz(Bölge "
                                                             "verilerinde bölgelerın başlangıç ve bitiş tarihleri "
                                                             "uyuşmadığı icin bölge veri gösteriminde kaldırdım.). "
                                                             "\n-Alttaki çubuğu kullanarak belirlediğiniz tarih "
                                                             "aralığında göreceğiniz veri sayısını değiştirebilirsiniz")


def infoButtonChart():  # Tablo bilgi mesajini gosteren fonksiyon.
    messagebox.showinfo(title="Tablo Bilgilendirme", message="-Sağ üstteki oktan grafik ekranına gidebilirsiniz.\n"
                                                             "-Ülkelerin sıralamasını değiştirmek için yukarıdaki "
                                                             "veri tiplerinden birine tıklayabilir, "
                                                             "sadece spesifik bir ülkeyi görmek için o ülkenin üstüne "
                                                             "tıklayabilirsiniz.\n"
                                                             "Not: [Country] A-Z'ye şeklinde sıralar.")


def provinceLimiter(a):  # ProvinceListBox'tan secilen eleman sayisini 3'le sinirlayan fonksiyon.
    global provinceSelection
    if len(countryProvinceListBox.curselection()) > 3:
        for i in countryProvinceListBox.curselection():
            if i not in provinceSelection:
                countryProvinceListBox.selection_clear(i)
    provinceSelection = countryProvinceListBox.curselection()


def mouseMotion(event):  # Grafigin ustune geldigimizde fare kordinatlarini grafik kordinatlari olarak veren ve bu
    # kordinatlarda bilgi paneli olusturan fonksiyon.
    try:
        for inf in informationPanels:
            inf.place_forget()
        if len(currentProvinces) > 0:
            for i in range(len(currentProvinces)):
                informationPanels[i].config(
                    text="Date: " + str(currentXData[i][int(event.xdata)]) + " Case: " + str(
                        currentYData[i][int(event.xdata)]))
                if 0 < event.xdata < dateSlider.get() and len(currentProvinces) < 2:
                    xTransform = a.transData.transform((int(event.xdata), int(event.ydata)))[0]
                    yTransform = \
                        a.transData.transform(
                            (int(event.xdata), currentYData[i][int(event.xdata)]))[
                            1]
                    informationPanels[i].place(x=xTransform, y=500 - yTransform)
                if len(currentProvinces) > 1:
                    xTransform = 375
                    yTransform = 68 + (i) * 22
                    informationPanels[i].place(x=xTransform, y=yTransform)
        else:
            if 0 < event.xdata < dateSlider.get():
                xTransform = a.transData.transform((int(event.xdata), int(event.ydata)))[0]
                yTransform = \
                    a.transData.transform((int(event.xdata), currentYData[int(event.xdata) + dateStart.current()]))[1]
            informationPanels[0].config(
                text="Date: " + str(currentXData[int(event.xdata) + dateStart.current()]) + " Case: " + str(
                    currentYData[int(event.xdata) + dateStart.current()]))
            informationPanels[0].place(x=xTransform, y=500 - yTransform)
    except:
        pass


def fontSize(val):  # Gosterilen eleman sayisina gore font boyu donduren fonksiyon.
    tickCount = val - dateStart.current()
    if tickCount <= 50:
        return 10
    elif 50 < tickCount <= 58:
        return 9
    elif 58 < tickCount <= 65:
        return 7
    elif 65 < tickCount <= 90:
        return 6
    elif 90 < tickCount <= 120:
        return 5
    elif tickCount > 120:
        return 4


def labelMaker(
        province):  # Bolgesi olan ulkelerde etiketlerde bolge adi da ciksin diye yazdigim deneysel bir fonksiyon.
    return "(" + str(province) + ")"


def drawLineGraph(x, y, province):  # Gonderdigimiz X ve Y degerleri ile cizgisel grafik cizen fonksiyon.
    a.plot(x, y, marker=".", label=currentCountry + province + "-" + currentDataType)
    a.legend(loc=2, framealpha=0)
    canvas.draw()


def drawBarGraph(x, y):  # Gonderdigimiz X ve Y degerleri ile bar grafiki cizen fonksiyon.
    a.bar(x, y, label=currentCountry + "-" + currentDataType)
    a.legend()
    canvas.draw()


def updateValue(val):  # Grafigin altinda scrollbari oynattigimizda gosterilen deger sayisinin guncellenmis haliyle
    # grafigi tekrar cizdiren fonkiyon.
    if len(currentCountry) != 0 and len(currentDataType) != 0:
        a.clear()
        a.tick_params(axis='x', labelsize=fontSize(int(val)), labelrotation=-90)
        if len(currentCountryProvinces) > 0:
            if len(currentProvinces) > 0:
                for i in range(len(currentProvinces)):
                    if str(graphType.get()) == "Line Graph":
                        drawLineGraph(currentXData[i][0:int(val)],
                                      currentYData[i][0:int(val)],
                                      labelMaker(currentProvinces[i]))
                    elif str(graphType.get()) == "Bar Graph":
                        drawBarGraph(currentXData[i][0:int(val)],
                                     currentYData[i][0:int(val)])
        else:
            if str(graphType.get()) == "Line Graph":
                drawLineGraph(currentXData[dateStart.current():int(val)],
                              currentYData[dateStart.current():int(val)], "")
            elif str(graphType.get()) == "Bar Graph":
                drawBarGraph(currentXData[dateStart.current():int(val)],
                             currentYData[dateStart.current():int(val)])


def canvasCleaner():  # [Clean] tusuna basinca canvasi temizleyen ve verileri temizleyen fonksiyon.
    a.clear()
    global currentXData
    global currentYData
    global currentCountry
    global currentDataType
    global currentCountryProvinces
    global currentProvinces
    global startDate
    global endDate
    currentCountry = ""
    currentDataType = ""
    currentXData = []
    currentYData = []
    currentCountryProvinces = []
    currentProvinces = []
    startDate = []
    dateStart.config(value=startDate)
    endDate = []
    dateEnd.config(value=endDate)
    dateSlider.config(from_=0, to=0)
    provinceLabel.place_forget()
    countryProvinceListBox.place_forget()
    countryProvinceScroll.place_forget()
    canvas.draw()


def updateSlider(a):  # Baslangic ve bitis verilerini degistirince alttaki scrollbarin baslangic ve bitis degerlerini
    # guncelleyen fonksiyon.
    dateSlider.config(from_=dateStart.current() + 1, to=len(startDate) + dateEnd.current() + 1)
    updateValue(dateSlider.get())


def updateData():  # X ve Y verilerini istenilen veri tipinde alan ve duzenleyen fonksiyon.
    if len(countryListBox.curselection()) > 0 and len(dataSelectionListBox.curselection()) > 0:
        global startDate
        global endDate
        global currentXData
        global currentYData
        global currentCountry
        global currentDataType
        global currentProvinces
        global previousProvinces
        global previousCountry
        global previousDataType
        global currentCountryProvinces
        global previousCountryProvinces
        if currentCountry == "" and currentDataType == "":
            currentDataType = str(dataSelectionListBox.get(dataSelectionListBox.curselection()))
            currentCountry = str(countryListBox.get(countryListBox.curselection()))
        else:
            if currentDataType != str(dataSelectionListBox.get(dataSelectionListBox.curselection())):
                currentDataType = str(dataSelectionListBox.get(dataSelectionListBox.curselection()))
            if currentCountry != str(countryListBox.get(countryListBox.curselection())):
                currentCountryProvinces = []
                currentCountry = str(countryListBox.get(countryListBox.curselection()))
            elif len(currentCountryProvinces) > 0:
                currentProvinces = []
                for i in countryProvinceListBox.curselection():
                    currentProvinces.append(currentCountryProvinces[i])
        if str(currentDataType) != str(previousDataType) or str(currentCountry) != str(
                previousCountry) or currentProvinces != previousProvinces:
            currentYData = (
                api.covidCaseDataGetting(api.countrySlugGetting(currentCountry), currentDataType.lower())).copy()
            currentXData = (
                api.covidDateDataGetting(api.countrySlugGetting(currentCountry), currentDataType.lower())).copy()
            if (currentDataType.lower()[0:5] == "daily"):
                graphType.place(x=900, y=60, width=100)
                try:
                    if "Province" in currentYData[0]:
                        currentData = []
                        currentData.append({"Province": currentYData[0]["Province"],
                                            "Cases": currentYData[0]["Cases"]})
                        for i in range(0, len(currentYData) - 1):
                            provinceData = {}
                            provinceData["Province"] = currentYData[i + 1]["Province"]
                            saver = 0
                            for j in range(i - 1, 0, -1):
                                saver = 0
                                if currentYData[j]["Province"] == provinceData["Province"]:
                                    provinceData["Cases"] = int(currentYData[i + 1]["Cases"]) - int(
                                        currentYData[j]["Cases"])
                                    saver = 1
                                    break
                            if saver != 1:
                                provinceData["Cases"] = int(currentYData[i + 1]["Cases"])
                            currentData.append(provinceData)
                        currentYData = currentData.copy()
                except:
                    currentData = [0]
                    currentData[0] = currentYData[0]
                    for i in range(1, len(currentYData)):
                        currentData.append(int(currentYData[i]) - int(currentYData[i - 1]))
                    currentYData = currentData.copy()
        try:
            if "Province" in currentYData[0]:
                if not currentCountryProvinces:
                    countryProvinceListBox.delete(0, END)
                    currentCountryProvinces = []
                    for i in currentXData:
                        currentCountryProvinces.append(i["Province"])
                    currentCountryProvinces = list(dict.fromkeys(currentCountryProvinces))
                    countryProvinceListBox.insert(END, *currentCountryProvinces)
                currentProvinces = []
                for i in countryProvinceListBox.curselection():
                    currentProvinces.append(currentCountryProvinces[i])
        except:
            currentCountryProvinces = []
            currentProvinces = []
        if len(currentCountryProvinces) == 0:
            startDate = currentXData[0:(len(currentXData) // 2)]
            endDate = currentXData[(len(currentXData) // 2):len(currentXData)]
            dateStart.place(x=90, y=520, width=100)
            dateStart.config(value=startDate)
            dateStart.current(0)
            dateEnd.place(x=810, y=520, width=100)
            dateEnd.config(value=endDate)
            dateEnd.current(0)
        else:
            endLabel.place_forget()
            startLabel.place_forget()
            dateStart.place_forget()
            dateEnd.place_forget()


def openChartFrame():  # Tablo frame'ini acan ve diger iki frame'i kapatan fonksiyon.
    canvasFrame.pack_forget()
    treeViewFrame.pack()
    spesificCountryFrame.pack_forget()


def openGraphFrame():  # Grafik frame'ini acan ve diger frame'i kapatan fonksiyon.
    treeViewFrame.pack_forget()
    canvasFrame.pack()


def openSpecificCountryFrame():  # Istenilen ulkenin verilerinin gosterildigi frame'i acan ve diger frame'i kapatan
    # fonksiyon.
    global ax
    treeViewFrame.pack_forget()
    spesificCountryFrame.pack()
    labels = ["Total Confirmed", "Total Deaths", "Total Recovered", "New Confirmed", "New Deaths", "New Recovered"]
    explodes = [.1, .1, .1, .1, .1, .1]
    ax.pie(chartCurrentItem["values"], autopct="%.0f %%", pctdistance=.7, explode=explodes)
    ax.legend(labels)


def Draw():  # [Draw] tusuna basinca veri guncellenmesini saglayan ve grafigin ilk halini cizen fonksiyon.
    if len(countryListBox.curselection()) > 0 and len(dataSelectionListBox.curselection()) > 0:
        global previousCountry
        global previousDataType
        global currentCountry
        global currentDataType
        global currentCountryProvinces
        global previousCountryProvinces
        global currentProvinces
        global previousProvinces
        global currentXData
        global currentYData
        previousCountry = currentCountry
        previousDataType = currentDataType
        previousCountryProvinces = currentCountryProvinces
        previousProvinces = currentProvinces
        a.clear()
        updateData()
        if len(currentCountryProvinces) > 0:
            countryProvinceListBox.place(x=1000, y=490, height=110)
            countryProvinceScroll.place(x=1121.5, y=490, height=110)
            provinceLabel.place(x=1030, y=470)
            if len(currentProvinces) > 0:
                xData = []
                yData = []
                for i in range(len(currentProvinces)):
                    xData.append([])
                    yData.append([])
                    for j in currentXData:
                        if j["Province"] == currentProvinces[i]:
                            xData[i].append(j["Date"])
                    for k in currentYData:
                        if k["Province"] == currentProvinces[i]:
                            yData[i].append(k["Cases"])
                    if str(graphType.get()) == "Line Graph":
                        drawLineGraph(xData[i][0:10], yData[i][0:10], labelMaker(currentProvinces[i]))
                    elif str(graphType.get()) == "Bar Graph":
                        drawBarGraph(xData[i][0:10], yData[i][0:10])
                currentXData = xData.copy()
                currentYData = yData.copy()
                dateSlider.config(from_=1, to=len(currentXData[0]))
        else:
            countryProvinceListBox.place_forget()
            countryProvinceScroll.place_forget()
            provinceLabel.place_forget()
            if str(graphType.get()) == "Line Graph":
                drawLineGraph(currentXData[0:10], currentYData[0:10], "")
            elif str(graphType.get()) == "Bar Graph":
                drawBarGraph(currentXData[0:10], currentYData[0:10])
            dateSlider.config(from_=dateStart.current() + 1, to=len(startDate) + dateEnd.current() + 1)


mainWindow = Tk()
mainWindow.geometry("1140x600")
mainWindow.title("Covid-19")
mainWindow.resizable(0, 0)
mainWindow.iconbitmap("Covid.ico")
# Frame'ler.
canvasFrame = Frame(mainWindow, width=1300, height=700, bg="#FFFFFF")
treeViewFrame = Frame(mainWindow, width=1300, height=700, bg="#FFFFFF")
spesificCountryFrame = Frame(mainWindow, width=1300, height=700, bg="#FFFFFF")
# Tablo sayfasinda kullanilan widgetler.
backChartButton = Button(spesificCountryFrame, text="<", command=openChartFrame)
backChartButton["font"] = font.Font(size=20)
backChartButton.place(x=5, y=5, width=50, height=30)

countryNameLabel = Label(spesificCountryFrame, font="Helvetica 40 bold", bg="#FFFFFF", fg="#848484")
countryNameLabel.place(x=250, y=20, width=700, height=100)
totalConfirmedLabel = Label(spesificCountryFrame, anchor="w", font="Helvetica 30 bold", bg="#FFFFFF", fg="#E88346")
totalConfirmedLabel.place(x=370, y=150, width=170, height=50)
totalDeathsLabel = Label(spesificCountryFrame, anchor="w", font="Helvetica 30 bold", bg="#FFFFFF", fg="#F06A6A")
totalDeathsLabel.place(x=370, y=220, width=170, height=50)
totalRecoveredLabel = Label(spesificCountryFrame, anchor="w", font="Helvetica 30 bold", bg="#FFFFFF", fg="#89D378")
totalRecoveredLabel.place(x=370, y=290, width=170, height=50)
newConfirmedLabel = Label(spesificCountryFrame, anchor="w", font="Helvetica 30 bold", bg="#FFFFFF", fg="#E88346")
newConfirmedLabel.place(x=370, y=360, width=170, height=50)
newDeathsLabel = Label(spesificCountryFrame, anchor="w", font="Helvetica 30 bold", bg="#FFFFFF", fg="#F06A6A")
newDeathsLabel.place(x=370, y=430, width=170, height=50)
newRecoveredLabel = Label(spesificCountryFrame, anchor="w", font="Helvetica 30 bold", bg="#FFFFFF", fg="#89D378")
newRecoveredLabel.place(x=370, y=500, width=170, height=50)

ConfirmedLabel = Label(spesificCountryFrame, text="Total Confirmed:",
                       font="Helvetica 30 bold", bg="#FFFFFF", fg="#848484")
ConfirmedLabel.place(x=20, y=150, width=350, height=50)
DeathsLabel = Label(spesificCountryFrame, text="Total Deaths:", font="Helvetica 30 bold", bg="#FFFFFF", fg="#848484")
DeathsLabel.place(x=20, y=220, width=350, height=50)
RecoveredLabel = Label(spesificCountryFrame, text="Total Recovered:",
                       font="Helvetica 30 bold", bg="#FFFFFF", fg="#848484")
RecoveredLabel.place(x=20, y=290, width=350, height=50)
nConfirmedLabel = Label(spesificCountryFrame, text="New Confirmed:",
                        font="Helvetica 30 bold", bg="#FFFFFF", fg="#848484")
nConfirmedLabel.place(x=20, y=360, width=350, height=50)
nDeathsLabel = Label(spesificCountryFrame, text="New Deaths:", font="Helvetica 30 bold", bg="#FFFFFF", fg="#848484")
nDeathsLabel.place(x=20, y=430, width=350, height=50)
nRecoveredLabel = Label(spesificCountryFrame, text="New Recovered:",
                        font="Helvetica 30 bold", bg="#FFFFFF", fg="#848484")
nRecoveredLabel.place(x=20, y=500, width=350, height=50)

openGraphButton = Button(treeViewFrame, text=">", command=openGraphFrame)
openGraphButton["font"] = font.Font(size=20)
openGraphButton.place(x=1085, y=5, width=50, height=30)

infoButtonChart = Button(treeViewFrame, bitmap="info", command=infoButtonChart)
infoButtonChart.place(x=1085, y=565, width=50, height=30)

chart = ttk.Treeview(treeViewFrame)
chart["columns"] = ("TotalConfirmed", "TotalDeaths", "TotalRecovered", "NewConfirmed", "NewDeaths", "NewRecovered")
chart.place(x=0, y=0, width=1080, height=600)
chart.column("#0", minwidth=0, width=170, stretch=NO)
chart.heading("#0", text="Country", command=lambda c="#0": chartSort(c))
chart.column("TotalConfirmed", minwidth=0, width=151, stretch=NO)
chart.heading("TotalConfirmed", text="Confirmed", command=lambda c="TotalConfirmed": chartSort(c))
chart.column("TotalDeaths", minwidth=0, width=151, stretch=NO)
chart.heading("TotalDeaths", text="Deaths", command=lambda c="TotalDeaths": chartSort(c))
chart.column("TotalRecovered", minwidth=0, width=151, stretch=NO)
chart.heading("TotalRecovered", text="Recovered", command=lambda c="TotalRecovered": chartSort(c))
chart.column("NewConfirmed", minwidth=0, width=151, stretch=NO)
chart.heading("NewConfirmed", text="New Confirmed", command=lambda c="NewConfirmed": chartSort(c))
chart.column("NewDeaths", minwidth=0, width=151, stretch=NO)
chart.heading("NewDeaths", text="New Deaths", command=lambda c="NewDeaths": chartSort(c))
chart.column("NewRecovered", minwidth=0, width=151, stretch=NO)
chart.heading("NewRecovered", text="New Recovered", command=lambda c="NewRecovered": chartSort(c))
chartScroll = Scrollbar(treeViewFrame, command=chart.yview)
chartScroll.place(x=1080, y=40, height=520)
chart.configure(yscrollcomman=chartScroll.set)
chart.bind("<ButtonRelease-1>", chartCountryShow)

chartFigure = Figure(figsize=(5, 5), dpi=100)
chartCanvas = FigureCanvasTkAgg(chartFigure, spesificCountryFrame)
chartCanvas.get_tk_widget().place(x=550, y=100)

ax = chartFigure.add_subplot(111)

chartPlotSaveButton = Button(spesificCountryFrame, text="Save", command=chartPlotSave)
chartPlotSaveButton.place(x=1000, y=550, width=100, height=30)
# Grafik sayfasinda kullanilan widgetler
figure = Figure(figsize=(5, 10), dpi=100)
a = figure.add_subplot(111)
a.set_title("Covid-19 Data Graph")
a.set_ylabel("Cases")
a.set_xlabel("Dates")

canvas = FigureCanvasTkAgg(figure, canvasFrame)
canvas.get_tk_widget().place(x=0, y=0, width=1000, height=500)
canvas.draw()

fcm = figure.canvas.mpl_connect('motion_notify_event', mouseMotion)

informationPanels = []
for i in range(3):
    informationPanels.append(Label(canvasFrame, text="Test", bg="#FFFFFF"))  # InformationPanel olarak duzeltilcek
    informationPanels[i].config(bg="#FFFFFF")

graphTypes = ["Line Graph", "Bar Graph"]
clickedGraphType = StringVar()
clickedGraphType.set(graphTypes[0])

graphType = ttk.Combobox(canvasFrame, value=graphTypes)
graphType.current(0)

dateSlider = Scale(canvasFrame, from_=0, to=0, orient="horizontal", command=updateValue, length=600, bg="#FFFFFF",
                   showvalue=0)
dateSlider.place(x=200, y=520)

startLabel = Label(canvasFrame, text="Start Date:", bg="#FFFFFF")
startLabel.place(x=90, y=500)
startDate = []
dateStart = ttk.Combobox(canvasFrame)
dateStart.place(x=90, y=520, width=100)
dateStart.bind('<<ComboboxSelected>>', updateSlider)
endLabel = Label(canvasFrame, text="End Date:", bg="#FFFFFF")
endLabel.place(x=810, y=500)
endDate = []
dateEnd = ttk.Combobox(canvasFrame)
dateEnd.place(x=810, y=520, width=100)
dateEnd.bind('<<ComboboxSelected>>', updateSlider)

countryLabel = Label(canvasFrame, text="Country Selection", bg="#FFFFFF")
countryLabel.place(x=1010, y=0)

countryListBox = Listbox(canvasFrame, exportselection=0)
countryListBox.place(x=1000, y=20, height=300)

countryListScroll = Scrollbar(canvasFrame, bg="#FFFFFF")
countryListBox.config(yscrollcommand=countryListScroll.set)
countryListScroll.config(command=countryListBox.yview)
countryListScroll.place(x=1121.5, y=20, height=300)

dataSelectionLabel = Label(canvasFrame, text="Data Selection", bg="#FFFFFF")
dataSelectionLabel.place(x=1010, y=320)

dataSelectionListBox = Listbox(canvasFrame, exportselection=0)
dataSelectionListBox.place(x=1000, y=340, height=100)
dataSelectionListScroll = Scrollbar(canvasFrame, bg="#FFFFFF")
dataSelectionListScroll.config(command=dataSelectionListBox.yview)
dataSelectionListScroll.place(x=1121.5, y=340, height=100)
dataSelectionListBox.config(yscrollcommand=dataSelectionListScroll.set)

provinceLabel = Label(canvasFrame, text="Provinces", bg="#FFFFFF")
countryProvinceListBox = Listbox(canvasFrame, exportselection=0, selectmode=MULTIPLE)
countryProvinceScroll = Scrollbar(canvasFrame, bg="#FFFFFF")
countryProvinceScroll.config(command=countryProvinceListBox.yview)
countryProvinceListBox.config(yscrollcommand=countryProvinceScroll.set)
countryProvinceListBox.bind("<<ListboxSelect>>", provinceLimiter)
provinceSelection = countryProvinceListBox.curselection()

drawButton = Button(canvasFrame, text="Draw", command=Draw)
drawButton.place(x=1000, y=440, width=50, height=30)
infoButtonCanvas = Button(canvasFrame, bitmap="info", command=infoButtonGraph)
infoButtonCanvas.place(x=1055, y=440, width=30, height=30)
canvasPlotSaveButton = Button(canvasFrame, text="Save", command=graphPlotSave)
canvasPlotSaveButton.place(x=900, y=480, width=100, height=30)
clearButton = Button(canvasFrame, text="Clear", command=canvasCleaner)
clearButton.place(x=1090, y=440, width=50, height=30)
backToChartButton = Button(canvasFrame, text="<", relief=FLAT, bg="#FFFFFF", activebackground="white",
                           command=openChartFrame)
backToChartButton["font"] = font.Font(size=20)
backToChartButton.place(x=5, y=5, width=50, height=30)
# ---------------------------------------------------------------------------
treeViewFrame.pack()

# for i in api.countryDataGettting():
countryListBox.insert(END, *api.countryDataGettting())
# for j in dataSelection:
dataSelectionListBox.insert(END, *dataSelection)

chartDataGetting()
chartWrite(chartData)

mainWindow.mainloop()
