from selenium import webdriver
from selenium.webdriver.support.select import Select
from ics import Calendar, Event
from selenium.common.exceptions import NoSuchElementException
import sys
import arrow


def main():

    if len(sys.argv) != 4:
        print("Invalid amount of arguments")
        quit()

    timezone = sys.argv[1]
    type = sys.argv[2].lower()
    timeStart = sys.argv[3]

    summaryDict = {}
    dateSaveDict = {}

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--use-fake-ui-for-media-stream")
    # Change the below lines for location of Chrome webdriver then uncomment
    # driver = webdriver.Chrome(options=options, executable_path=r"ENTER LOCATION OF WEBDRIVER HERE")
    # driver2 = webdriver.Chrome(options=options, executable_path=r"ENTER LOCATION OF WEBDRIVER HERE")
    # https://sites.google.com/chromium.org/driver/downloads?authuser=0
    driver.get("https://schedule.hololive.tv/lives/"+type)

    driver.maximize_window()
    driver2.maximize_window()


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

    schedule(dateSaveDict,summaryDict,timezone,sys.argv[2],timeStart)

    driver.close()

    driver2.close()


def add(date, stream, dateSaveDict, summaryDict, driver):

    dateDict = {}
    streamDict = {}
    dateList = []
    summaryList = []
    info = ''
    yt = ''
    embed = ''


    index = 0

    for e in date:
        test = e.location
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
                summaryList.append(t.replace('\n',' '))
            else:
                continue
        summaryDict[index] = list(summaryList)
        summaryList.clear()
        index += 1

def schedule(dateSaveDict,summaryDict, timezone,type,timeStart):

    i = 0

    while i < len(dateSaveDict):
        c = Calendar()
        e = Event()
        e.name = "Hololive " + type + " Schedule for " + str(dateSaveDict[i][0:5])
        e.begin = arrow.get('2021' + '-' + str(dateSaveDict[i][0:2]) + '-' + str(dateSaveDict[i][3:5]) + ' ' + timeStart + ":00").replace(tzinfo=timezone)

        e.description = str(summaryDict[i+1])

        c.events.add(e)

        print(c.events)

        with open('holo_' + type + "_" + str(dateSaveDict[i][0:2]) + '-' + str(dateSaveDict[i][3:5])  +'.ics', 'w' ,encoding='utf8') as f:
            f.writelines(c)
        i += 1


if __name__ == "__main__":
    main()

