from selenium import webdriver
from selenium.webdriver.support.select import Select
from ics import Calendar, Event
from selenium.common.exceptions import NoSuchElementException
from datetime import date, datetime
from twitter_get import importer
import sys
import arrow


def main():

    if len(sys.argv) != 5:
        print("Invalid amount of arguments")
        quit()

    if sys.argv[4] != 'True' and sys.argv[4] != 'False':
        print("Must be True or False")
        quit()

    # Change the below line for location of Chrome webdriver
    exec_path = r"ENTER LOCATION OF WEBDRIVER HERE"
    timezone = sys.argv[1]
    type = sys.argv[2].lower()
    timeStart = sys.argv[3]
    nij = sys.argv[4] == 'True'

    summaryDict = {}
    dateSaveDict = {}

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--use-fake-ui-for-media-stream")
    driver = webdriver.Chrome(options=options, executable_path=exec_path)
    driver2 = webdriver.Chrome(options=options, executable_path=exec_path)

    # https://sites.google.com/chromium.org/driver/downloads?authuser=0
    driver.get("https://schedule.hololive.tv/lives/"+type)

    driver.maximize_window()
    driver2.maximize_window()

    if(nij is True):
        driver3 = webdriver.Chrome(options=options, executable_path=exec_path)
        driver3.get("https://niji-mado.web.app/home")
        driver3.maximize_window()

        neDict = {'english': ['show kr streamers', 'show id streamers', 'show jp streamers', 'show upcoming lives'],
                  'indonesia': ['show kr streamers', 'show en streamers', 'show jp streamers', 'show upcoming lives'],
                  'hololive': ['show kr streamers', 'show id streamers', 'show en streamers', 'show upcoming lives'],
                  'lives': ['show upcoming lives']}
        ne = []

        if str(type) in neDict.keys():
            ne = neDict.get(type)

        tz = driver3.find_elements_by_class_name(
            'mat-focus-indicator.mat-tooltip-trigger.topbar-button.mat-button.mat-button-base')
        for i in tz:
            if i.get_attribute('aria-label') in ne:
                try:
                    i.click()
                except:
                    print("oof")

    time = Select(driver.find_element_by_id("timezoneSelect"))

    try:
        time.select_by_visible_text(timezone)
    except NoSuchElementException:
        print("Timezone not found | Ex: America/Chicago")
        driver.close()
        quit()

    date = driver.find_elements_by_class_name('holodule.navbar-text')

    stream = driver.find_elements_by_class_name('thumbnail')

    add(date, stream, dateSaveDict, summaryDict, driver2)

    if(nij is True):
        streamN = driver3.find_elements_by_class_name('mat-tooltip-trigger.live-button')
        addN(streamN, dateSaveDict, summaryDict)
        driver3.close()

    schedule(dateSaveDict,summaryDict,timezone,sys.argv[2],timeStart)

    driver.close()

    driver2.close()

    if str(type) == 'english':
        importer(nij)

def add(dateE, stream, dateSaveDict, summaryDict, driver):

    dateDict = {}
    streamDict = {}
    dateList = []
    summaryList = []
    numDateList = []
    firstSep = 0
    info = ''
    yt = ''
    embed = ''

    index = 0

    today = datetime(datetime.now().year,datetime.now().month,datetime.now().day,datetime.now().hour,datetime.now().minute)

    for e in dateE:
        test = e.location
        numDateList.append(e.text[0:5])
        for t in test:
            if(t == 'y'):
                dateDict[e.text] = test[t]
                dateSaveDict[index] = e.text
                index += 1

    for e in stream:
        test = e.location
        for t in test:
            if (t == 'y'):
                embed = e.get_attribute('href').replace('watch?v=', 'embed/')
                if('embed/' in embed):
                    driver.get(embed)
                    yt = driver.find_element_by_class_name('ytp-title')

                    info = e.text + " " + yt.text + " " + e.get_attribute('href')
                    streamDict[info] = test[t]

    for e in dateDict:
        dateList.append(dateDict[e])

    index = 1

    for e in dateDict:
        if(index == len(dateList)):
            next = sys.maxsize
        else:
            next = dateList[index]
        for t in streamDict:
            if streamDict[t] > dateDict[e] and streamDict[t] < next:

                if (firstSep == 0):
                    summaryList.append('Hololive')
                    firstSep = 1
                else:
                    summaryList.append('')
                new_datetime = datetime(datetime.now().year,int(numDateList[index-1][0:2]),int(numDateList[index-1][3:5]),int(t[0:2]),int(t[3:5]))

                if(new_datetime < today):
                    t = t.replace(t[0:5], 'Live!')
                t = t.replace('【', ' [ ')
                t = t.replace('】', ' ] ')

                summaryList.append(t.replace('\n',' '))

            else:
                continue
        firstSep = 0
        summaryDict[index] = list(summaryList)
        summaryList.clear()
        index += 1

def addN(stream, dateSaveDict, summaryDict):
    #print(stream)

    futureStream = []
    futurerStream = []
    currentStream = []
    i = 0
    dateInitialI = 0
    firstSep = 0
    firstSepP = 0
    firstSeppP = 0


    today = date.today()


    while dateInitialI < len(dateSaveDict): # Hololive usually has schedules up earlier
        dateInitialI += 1
    new_datetime = datetime(date.today().year,int(dateSaveDict[dateInitialI-1][0:2]),int(dateSaveDict[dateInitialI-1][3:5]))
    new_datetime = datetime.date(new_datetime)

    tdelta = new_datetime - today
    tdelta = tdelta.days

    for e in stream:
        try:
            tets = e.find_element_by_class_name('live-avatar-published-at.ng-star-inserted')
            i = 0
            while i < len(dateSaveDict):
                if str(dateSaveDict[i][0:2]) + '/' + str(dateSaveDict[i][3:5]) in tets.text:
                    if firstSeppP == 0:
                        futurerStream.append('\nNijisanji')
                        firstSeppP = 1
                    else:
                        futurerStream.append('')
                    t = e.get_attribute('title')
                    t = t.replace('【', ' [ ')
                    t = t.replace('】', ' ] ')
                    futurerStream.append(tets.text[11:16] + ' ' + t + ' ' + e.get_attribute('href'))
                    summaryDict[i+1] += futurerStream
                    futurerStream.clear()
                    i = len(dateSaveDict)
                elif len(tets.text)<6: # Only time
                    if firstSepP == 0 :
                        futureStream.append('\nNijisanji')
                        firstSepP = 1
                    else:
                        futureStream.append('')
                    t = e.get_attribute('title')
                    t = t.replace('【', ' [ ')
                    t = t.replace('】', ' ] ')
                    futureStream.append(tets.text + ' ' + t + ' ' + e.get_attribute('href'))
                    i = len(dateSaveDict)
                i += 1
        except NoSuchElementException: # Already live streams
            if firstSepP == 0:
                currentStream.append('\nNijisanji')
                firstSepP = 1
            else:
                currentStream.append('')
            t = e.get_attribute('title')
            t = t.replace('【', ' [ ')
            t = t.replace('】', ' ] ')

            currentStream.append('Live!' + ' ' + t + ' ' + e.get_attribute('href'))
        summaryDict[len(summaryDict)-tdelta] += futureStream
        futureStream.clear()
        summaryDict[len(summaryDict)-tdelta] += currentStream
        currentStream.clear()
def schedule(dateSaveDict,summaryDict, timezone,type,timeStart):

    i = 0

    while i < len(dateSaveDict):
        c = Calendar()
        e = Event()
        e.name = "VTuber " + type + " Schedule for " + str(dateSaveDict[i][0:5])
        e.begin = arrow.get(str(datetime.now().year) + '-' + str(dateSaveDict[i][0:2]) + '-' + str(dateSaveDict[i][3:5]) + ' ' + timeStart + ":00").replace(tzinfo=timezone)

        summaryDict[i+1] = "\n".join(summaryDict[i+1])
        e.description = str(summaryDict[i+1])

        c.events.add(e)

        print(c.events)

        with open('vtub_' + type + "_" + str(dateSaveDict[i][0:2]) + '-' + str(dateSaveDict[i][3:5])  +'.ics', 'w' ,encoding='utf8') as f:
            f.writelines(c)
        i += 1


if __name__ == "__main__":
    main()

