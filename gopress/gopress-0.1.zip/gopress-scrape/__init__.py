# GoPress help functions
#############
# Functions #
#############
# Wrapper
def GoPress(username,password,zoekstring, publicaties, van, tot,max=100,output = [], init=0,van_init={},browser="chrome"):
    import sys
    print("########################################################################")
    print("                              Zoekopdracht                              ")
    print("########################################################################")
    print("Zoekstring: " + zoekstring)
    print_string = "Publicaties: "
    for publicatie in publicaties:
        print_string += publicatie["naam"] + ", "
    print(print_string[:-2])

    # Zet publicaties in 1 string om in naam van gesavede file te gebruiken
    publicaties_string = ""
    for publicatie in publicaties:
        if publicatie["editie"] == "":
            publicaties_string+= publicatie["naam"]
        else:
            publicaties_string+= publicatie["naam"] + " " + publicatie["editie"]

    # Tijdsperiode
    print("Tijdsinterval: " + van["dag"] + " " + van["maand"] + " " + van["jaar"] +
            " tot " + tot["dag"] + " " + tot["maand"] + " " + tot["jaar"])

    # Save Output Data:
    if van_init == {}:
        van_init = van
    # output = list van resultaten die elk een dict zijn met keys "publicatie", "datum", "titel" en "tekst"
    import pickle
    if output == []:
        try:
            output = pickle.load(open("results/" +
                            van_init["jaar"] + van_init["maand"] + van_init["dag"] +
                            "-" +
                            tot["jaar"] + tot["maand"] + tot["dag"] +
                            "_" +
                            zoekstring +
                            "_" +
                            publicaties_string +
                            ".p", "rb"))
            print("Reeds opgehaalde artikels: " + str(len(output)))
        except FileNotFoundError:
            output = list()
            print("Geen reeds opgehaalde artikels....")

    print(" ")
    print("########################################################################")
    print("                 Start GoPress Webscraping Algoritme                    ")
    print("########################################################################")

    import time
    ############
    # Get Data #
    ############
    # Initialize driver
    if init == 0:
        print("Initialiseer Selenium webdriver via Google Chrome....")
        driverGoPress = initializeGoPress(username,password,browser)

    # Search GoPress
    try:
        search_data = searchGoPress(driverGoPress,zoekstring, publicaties, van, tot)
    except Exception as e:
        print("Geen Selenium webdriver beschikbaar....")
        print(type(e))
        print(e.args)
        sys.exit(0)

    # Check number of results
    aantal_resultaten = search_data["aantal_resultaten"]

    print("Op te halen artikels: " + str(aantal_resultaten))

    if aantal_resultaten <= max:
        print("Aantal iteraties: 1")
        # Scrape GoPress straightforward
        output = scrapeGoPress(search_data, username,password,zoekstring, publicaties,max, van, tot, output, van_init)
    else:
        try:
            driverGoPress.refresh()
        except TimeoutError:
            driverGoPress = initializeGoPress(username,password)
        # driverGoPress.close()
        # driverGoPress.quit()

        # Try in multiple times, otherwise too big
        iterations = round(aantal_resultaten/max)
        if iterations*max < aantal_resultaten:
            iterations += 1

        print("Aantal iteraties: "+ str(iterations))

        [van_list,tot_list] = splitDateInterval(van,tot,iterations)

        for i in range(len(van_list)):
            print(" ")
            print("Iteratie "+ str(i+1) + " van " + str(iterations) + ": van " + van_list[i]["dag"] + " " + van_list[i]["maand"] + " " + van_list[i]["jaar"] +
                                                                        " tot " + tot_list[i]["dag"] + " " + tot_list[i]["maand"] + " " + tot_list[i]["jaar"])

            try:
                driverGoPress.refresh()
            except:
                driverGoPress = initializeGoPress(username,password)

            # time.sleep(5)
            # driverGoPress = initializeGoPress(username,password)
            search_data = searchGoPress(driverGoPress,zoekstring, publicaties, van_list[i], tot_list[i])
            output = scrapeGoPress(search_data, username,password,zoekstring, publicaties,max, van, tot, output,van_init)

        driverGoPress.close()

    return output

# Initiate GoPress website and login
def initializeGoPress(username,password,browser="chrome"):
    import time
    from selenium import webdriver
    # "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    if browser == "chrome":
        driver = webdriver.Chrome()
    elif browser == "firefox":
        driver = webdriver.Firefox()

    url = "http://www.gopress.be/info/nl"
    driver.get(url)

    # Login
    driver.find_element_by_id("edit-email").send_keys(username)
    driver.find_element_by_id("edit-password").send_keys(password)
    driver.find_element_by_id("edit-submit").click()
    time.sleep(5)

    return driver

# Search GoPress using driver
def searchGoPress(driverGoPress,zoekstring, publicaties, van, tot):
    import time
    from selenium.webdriver.common.by import By

    # Geef zoekopdracht in
    zoek = driverGoPress.find_element_by_id("comfort-field-q")
    zoek.clear()
    zoek.send_keys(zoekstring)

    # Enkel exacte zin match
    driverGoPress.find_element_by_id("operator-exact").click()

    # Van welke datum tot welke datum
    # Zie dat optieveld open staat (dit moet, anders werkt het niet)
    while driverGoPress.find_element_by_id("comfort-more-options").get_attribute("style") == "display: none;" or driverGoPress.find_element_by_id("comfort-more-options").get_attribute("style") == "":
        driverGoPress.find_element_by_class_name("title_comfort-more-options").click()
    # VAN
    el = driverGoPress.find_element_by_id('comfort-from')
    for option in el.find_elements_by_tag_name('option'):
        if option.text == van["dag"] or option.text == van["maand"] or option.text == van["jaar"]:
            option.click() # select() in earlier versions of webdriver

    # TOT
    el = driverGoPress.find_element_by_id('comfort-to')
    for option in el.find_elements_by_tag_name('option'):
        if option.text == tot["dag"] or option.text == tot["maand"] or option.text == tot["jaar"]:
            option.click() # select() in earlier versions of webdrive

    # Selecteer publicaties
    # First deselect all
    active = driverGoPress.find_element_by_id("sources-type")
    active.find_element_by_class_name("check").click()
    if active.find_element_by_class_name("active").text != "Lijst":
        # Click again to deselect everything
        active.find_element_by_class_name("check").click()

    # Now select publications
    for publicatie in publicaties:
        # Eerst correcte type
        types = driverGoPress.find_element_by_id("sources-type")
        if publicatie["type"] == "krant":
            types.find_element_by_id("sources-newspapers").click()
        elif publicatie["type"] == "magazine":
            types.find_element_by_id("sources-magazines").click()
        elif publicatie["type"] == "twitter":
            types.find_element_by_id("sources-twitter").click()

        # Dan naam, afhankelijk van editie
        css_selector_string = "div[data-value='" + publicatie["naam"] + "']"
        if publicatie["editie"] == "":
            driverGoPress.find_element(By.CSS_SELECTOR, css_selector_string).find_element_by_class_name("sources-logo").click()
        else:
            driverGoPress.find_element(By.CSS_SELECTOR, css_selector_string).find_element_by_class_name("sources-open-editions").click()
            while "display: none;" in driverGoPress.find_element(By.CSS_SELECTOR, css_selector_string).find_element_by_class_name("sources-arrow-editions").get_attribute("style"):
                continue

            sources_scroll = driverGoPress.find_element_by_id("sources-editions-group").find_elements_by_class_name("sources-scroll-editions")
            for i in range(len(sources_scroll)):
                if "display: block;" in sources_scroll[i].get_attribute("style"):
                    for j in range(len(publicatie["editie"])):
                        css_selector_string_editie = "div[data-value='" + publicatie["naam"] + "__" + publicatie["editie"][j] + "']"
                        driverGoPress.find_element(By.CSS_SELECTOR, css_selector_string_editie).find_element_by_class_name("sources-logo").click()
                    break

    # Zoek!
    driverGoPress.find_element_by_class_name("sources-search").click()

    # Check number of results
    while True:
        try:
             aantal_resultaten = int(driverGoPress.find_element_by_class_name("comfort-nb-results").text.split(" ")[0])
        except:
            continue
        break

    # Return
    search_data = {"driver": driverGoPress,
                    "zoekstring" : zoekstring,
                   "publicaties" : publicaties,
                   "van": van,
                   "tot": tot,
                   "aantal_resultaten":aantal_resultaten}
    return search_data

# Scrape GoPress using driver
def scrapeGoPress(search_data, username,password,zoekstring, publicaties,max, van, tot, output,van_init):
    from selenium.webdriver.support.expected_conditions import staleness_of
    import time
    import pickle
    import numpy as np
    from bs4 import BeautifulSoup

    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    # Get inputs
    driverGoPress = search_data["driver"]
    zoekstring = search_data["zoekstring"]
    aantal_resultaten = search_data["aantal_resultaten"]
    publicaties = search_data["publicaties"]
    van_iteratie = search_data["van"]
    tot_iteratie = search_data["tot"]

    # First scroll down until all results are displayed on page
    # Estimate the number of scrolls necessary (25 extra per scroll)
    scrolls = np.ceil(aantal_resultaten/25) + 1
    print("Scrolling (ET: " + str(int(scrolls)*10) + " s) ....")
    for i in range(int(scrolls)):
        driverGoPress.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)

    resultaten = driverGoPress.find_elements_by_class_name("comfort-flipboard-article")

    # Check of scroll is vastgelopen
    # Signalen: - veelvoud van 25 resultaten zichtbaar
    #           - aantal zichtbare resulaten komt niet in buurt van aangekondigde resultaten

    if len(resultaten)%25 == 0 and len(resultaten) < (scrolls - 3)*25:
        print("ERROR: Selenium Webdriver vastgelopen tijdens scrollen....")
        print("GoPress herstarten vanaf volgende datum: " + van_iteratie["dag"] + " " + van_iteratie["maand"] + " " + van_iteratie["jaar"])

        # restart webdriver
        driverGoPress.close()

        from gopress_functions import GoPress
        output = GoPress(username,password,zoekstring, publicaties, van_iteratie, tot,max,output,init=0,van_init=van_init)

        import sys
        sys.exit(0)

    # Start scraping...
    time.sleep(10)

    count = 0
    totaal_artikels = len(resultaten)
    reeds_opgehaalde_artikels = 0
    opgehaalde_artikels = 0
    error_artikels = 0
    for resultaat in resultaten:
        # Time scraping
        if count == 0:
            start_gen = time.time()

        # Append new result
        output.append(dict())
        output[-1]["link_id"] = ""

        start_link_id = time.clock()
        while output[-1]["link_id"] == "" or output[-1]["link_id"] == None:
            output[-1]["link_id"] = resultaat.get_attribute("id")
            stop_link_id = time.clock()
            if (stop_link_id-start_link_id) > 10:
                break

        # First check if result is already in database
        reeds_opgeslagen = 0
        for reeds_opgeslagen_resultaat in output[:-1]:
            if reeds_opgeslagen_resultaat["link_id"] == "":
                break
            if reeds_opgeslagen_resultaat["link_id"] == output[-1]["link_id"]:
                # Reeds opgeslagen, ga naar volgende element in for loop
                reeds_opgeslagen = 1
                reeds_opgehaalde_artikels += 1
                # Remove last element
                output.pop(-1)
                break

        if reeds_opgeslagen == 0:
            # Scrape cover_info
            if resultaat.find_element_by_tag_name("h4").text == "":
                time.sleep(5)
                output[-1]["titel"] = resultaat.find_element_by_class_name("condensed").text
                output[-1]["publicatie"] = resultaat.find_element_by_tag_name("h4").text.split("\n")[0].split(" - ")[0]
                output[-1]["datum"] = resultaat.find_element_by_tag_name("h4").text.split("\n")[0].split(" - ")[1]
            else:
                try:
                    output[-1]["titel"] = resultaat.find_element_by_class_name("condensed").text
                    output[-1]["publicatie"] = resultaat.find_element_by_tag_name("h4").text.split("\n")[0].split(" - ")[0]
                    output[-1]["datum"] = resultaat.find_element_by_tag_name("h4").text.split("\n")[0].split(" - ")[1]
                except:
                    output[-1]["titel"] = ""
                    output[-1]["publicatie"] = ""
                    output[-1]["datum"] = ""

            if len(resultaat.find_element_by_tag_name("h4").text.split("\n")) == 1:
                output[-1]["pagina"] = ""
            else:
                output[-1]["pagina"] = resultaat.find_element_by_tag_name("h4").text.split("\n")[1]

            # Go to result (met webdriverwait om error te vermijden (not clickable))
            resultaat = WebDriverWait(driverGoPress, 20).until(EC.element_to_be_clickable((By.ID, resultaat.get_attribute("id"))))

            try:
                resultaat.click()
            except:
                try:
                    # print("ERROR: Element not clickable issue. Moving element into view....")
                    driverGoPress.execute_script("window.scrollBy(0, -150);")
                    resultaat.click()
                except:
                    error_artikels += 1
                    print("ERROR: Element not clickable issue, article was NOT retrieved....")
                    # Remove last element
                    output.pop(-1)
                    continue

            # dummy DOM that only exists on new page, not on old
            # use implictly_wait
            start = time.clock()
            while True:
                # Break out of loop after 120 seconds
                stop = time.clock()
                if (stop - start) > 120:
                    # restart webdriver
                    driverGoPress.close()

                    # Remove last element
                    output.pop(-1)

                    # Rerun GoPress function
                    print("ERROR: Selenium webdriver vastgelopen....")
                    print("GoPress herstarten vanaf volgende datum: " + van_iteratie["dag"] + " " + van_iteratie["maand"] + " " + van_iteratie["jaar"])
                    from gopress_functions import GoPress
                    output = GoPress(username,password,zoekstring, publicaties, van_iteratie, tot,max,output,init=0,van_init=van_init)

                    import sys
                    sys.exit(0)
                # Break out of while if search page is no longer displayed
                if driverGoPress.find_element_by_id("comfort-search-page").get_attribute("style") == 'display: none;': break

            # Nu zijn we op resultaat pagina, scrape de rest
            # Tekst
            source = driverGoPress.find_element_by_id("columns-cointainer").get_attribute("innerHTML")
            soup = BeautifulSoup(source)

            output[-1]["tekst"] = ""
            for paragraaf in soup.find_all("p"):
                output[-1]["tekst"] += paragraaf.text + " "

            # Zet publicaties in 1 string om in naam van gesavede file te gebruiken
            # Zet publicaties in 1 string om in naam van gesavede file te gebruiken
            publicaties_string = ""
            for publicatie in publicaties:
                if publicatie["editie"] == "":
                    publicaties_string+= publicatie["naam"]
                else:
                    publicaties_string+= publicatie["naam"] + " " + publicatie["editie"]

            # Save dit resultaat via pickle
            pickle.dump(output, open("results/" +
                                van_init["jaar"] + van_init["maand"] + van_init["dag"] +
                                "-" +
                                tot["jaar"] + tot["maand"] + tot["dag"] +
                                "_" +
                                zoekstring +
                                "_" +
                                publicaties_string +
                                ".p", "wb"), protocol =2)
            opgehaalde_artikels += 1

            # Ga terug
            driverGoPress.find_element_by_class_name("comfort-back-search").click()

        # Time scraping
        if count == 0:
            stop_gen = time.time()
            print("Scraping (ET: " + str(round((stop_gen-start_gen)*(len(resultaten)-1))) + " s) ....")

        # Counter
        count += 1

    # driverGoPress.close()
    print('Reeds opgehaalde artikels  : '  + str(reeds_opgehaalde_artikels))
    print('Nu opgehaalde artikels     : '  + str(opgehaalde_artikels))
    print('ERROR                      : '  + str(error_artikels))
    print('Totaal aantal artikels     : '  + str(totaal_artikels))

    return output

def customstringToDatetime(datestring):
    datelist = datestring.split("-")

    # Add leading 0 to single date (1-9)
    if len(datelist[0]) == 1:
        datelist[0] = "0" + datelist[0]

    month_conversion = [
        ["Januari", "Jan"],
        ["Februari", "Feb"],
        ["Maart", "Mar"],
        ["April", "Apr"],
        ["Mei", "May"],
        ["Juni", "Jun"],
        ["Juli", "Jul"],
        ["Augustus", "Aug"],
        ["September", "Sep"],
        ["Oktober", "Oct"],
        ["November", "Nov"],
        ["December", "Dec"],
    ]

    for month in month_conversion:
        if datelist[1] == month[0]:
            datelist[1] = month[1]

    datestring = ""
    for i in range(len(datelist)):
        datestring += datelist[i] + "-"

    import datetime
    datetime_object = datetime.datetime.strptime(datestring[:-1], "%d-%b-%Y")

    return datetime_object

def datetimeToCustomstring(datetime_object):
    import datetime
    datestring = datetime_object.strftime("%d-%b-%Y")

    datelist = datestring.split("-")

    # Remove leading 0
    if datelist[0][0] == "0":
        datelist[0] = datelist[0][-1]

    month_conversion = [
        ["Januari", "Jan"],
        ["Februari", "Feb"],
        ["Maart", "Mar"],
        ["April", "Apr"],
        ["Mei", "May"],
        ["Juni", "Jun"],
        ["Juli", "Jul"],
        ["Augustus", "Aug"],
        ["September", "Sep"],
        ["Oktober", "Oct"],
        ["November", "Nov"],
        ["December", "Dec"],
    ]

    for month in month_conversion:
        if datelist[1] == month[1]:
            datelist[1] = month[0]

    datestring = ""
    for i in range(len(datelist)):
        datestring += datelist[i] + "-"

    datestring = datestring[:-1]

    return datestring

def splitDateInterval(van,tot,iterations):
    # Change van en tot continuously
    import datetime
    van_datetime = customstringToDatetime(van["dag"] + "-" + van["maand"] + "-" + van["jaar"])
    tot_datetime = customstringToDatetime(tot["dag"] + "-" + tot["maand"] + "-" + tot["jaar"])

    van_list = []
    tot_list = []
    interval_totaal = tot_datetime - van_datetime
    interval_iteration = round(interval_totaal.days/iterations)

    for iteration in range(iterations):
        if iteration == 0:
            van_list.append(van_datetime)
        else:
            van_list.append(tot_list[-1] + datetime.timedelta(days=1))

        tot_list.append(van_list[-1] + datetime.timedelta(days=interval_iteration))

        test = tot_datetime - tot_list[-1]
        if test.days <= 0:
            # Too far
            tot_list[-1] = tot_datetime
            break

    for i in range(len(van_list)):
        dummy = dict()
        dummy["dag"] = datetimeToCustomstring(van_list[i]).split("-")[0]
        dummy["maand"] = datetimeToCustomstring(van_list[i]).split("-")[1]
        dummy["jaar"] = datetimeToCustomstring(van_list[i]).split("-")[2]
        van_list[i] = dummy
    for i in range(len(tot_list)):
        dummy = dict()
        dummy["dag"] = datetimeToCustomstring(tot_list[i]).split("-")[0]
        dummy["maand"] = datetimeToCustomstring(tot_list[i]).split("-")[1]
        dummy["jaar"] = datetimeToCustomstring(tot_list[i]).split("-")[2]
        tot_list[i] = dummy

    return [van_list,tot_list]
