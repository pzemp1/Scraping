import pandas as pd
import urllib3
from selenium import webdriver
import time

if __name__ == "__main__":
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    driver.get("https://oddspedia.com/table-tennis/czech-republic/liga-pro#odds")
    driver.implicitly_wait(10)
    #loadMore = driver.find_element_by_xpath(xpath="/html/body/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div/main/div[2]/div/div[1]/div[5]/button")
    counter = 0
    TextData = []

    ''' 
    Use Try: and Except: for control flow.
    
    1. Collect All "match-list-item match-list-item-with-odds" class name objects and store in array X. 
    2. We iterate through class = "match-list-item match-list-item-with-odds" object in Array X.
    We do multiple checks. If it fails any of these checks then we ignore it. 
    First, object in X (let this be i).
        1. Check if object class = "match-status" exists in object i. 
           If it exists, i is a valid object. (Rejects Matches which have not been played so far)
        2. Next check if the two object class = "match-team-name", exist in object i, Copy Names.
           First is Home , Second is Away. (Both Need to be present if not, Reject Sample)
        3. Check if the two object class = "match-score-result__score" exists within i.
           First is Home, Second is Away. (Reject Sample, if it does not exist)
        4. Check if the two object class = "odd_value", exists in object i. Copy Odds. 
           First is Home, Second is Away. 
           
        We will have 2 Datasets.
        One that includes all matches but excludes odds. 
        One that only includes matches with odds. 
        
        Generate predictions from both datasets and combine them, to combat the "loss" of data?
    '''


   #"match-score-result__score"
    # Replace white spaces with .

    Class = ["match-list-item.match-list-item--with-odds", ".match-status",
                  ".match-team__name", ".match-score-result__score", ".odd__value"]

    Data = []
    DataOdds = []

    while True:
        try:
            prevButton = driver.find_element_by_xpath(xpath="/html/body/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div/main/div[2]/div/div[1]/div[2]/button[1]")
            if counter != 0:
                loadMore = prevButton.find_element_by_xpath(xpath="/html/body/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div/main/div[2]/div/div[1]/div[5]/button")
                loadMore.click()
                time.sleep(2)

            AllObjects = driver.find_elements_by_class_name(Class[0])
            #print(len(AllObjects))
            #print(AllObjects)
            count = 0
            for i in AllObjects:
                #print(i.text)
                count += 1
                Temp = []
                TempOdds = []
                try:
                    MatchStatus = i.find_element_by_css_selector(Class[1])
                    #MatchStatus = i.find_element_by_class_name(Class[1])
                    print(f"A - {count}")
                    #If this exists we won't continue.
                except:
                    #MatchStatus = i.find_element_by_css_selector(Class[1])
                    #print(MatchStatus)
                    print(f"B - {count}")
                    continue

                try:
                    Players = i.find_elements_by_css_selector(Class[2])
                    #Players = i.find_elements_by_class_name(Class[2])
                    print(Players)
                    print(f"C - {count}")
                    if len(Players) != 2:
                        print(f"D - {count}")
                        continue

                    Temp.append(Players[0].text)
                    Temp.append(Players[1].text)
                    TempOdds.append(Players[0].text)
                    TempOdds.append(Players[1].text)

                except:
                    print(f"E - {count}")
                    continue

                try:
                    #MatchScores = i.find_elements_by_css_selector(Class[3])
                    #MatchObj = i.find_element_by_class_name(".match-score.match-score-boxed")
                    MatchScores = i.find_elements_by_css_selector(Class[3])
                    #print(len(MatchScores))
                    #MatchScores = i.find_elements_by_class_name(Class[3]) #If this does not exist we continue
                    #print(MatchScores[-2].text)
                    #print(MatchScores[-1].text)
                    Temp.append(MatchScores[-2].text)
                    Temp.append(MatchScores[-1].text)
                    TempOdds.append(MatchScores[-2].text)
                    TempOdds.append(MatchScores[-1].text)
                    print(f"F - {count}")
                except:
                    print(f"F1 - {count}")
                    continue

                continueExecution = True
                try:
                    Odds = i.find_elements_by_css_selector(Class[4])
                    #Odds = i.find_elements_by_class_name(Class[4])
                    TempOdds.append(Odds[0].text)
                    TempOdds.append(Odds[1].text)
                    continueExecution = False
                    print(f"G - {count}")
                except:
                    print(f"H - {count}")
                    pass

                if not continueExecution:
                    DataOdds.append(TempOdds)

                Data.append(Temp)
                print(TempOdds)
                print(Temp)

            prevButton.click()
            time.sleep(2)
        except:
            break

        #nextButton = driver.find_element_by_xpath(xpath="/html/body/div[1]/div[2]/div/div[1]/div[2]/div[2]/div/div/main/div[2]/div/div[1]/div[2]/button[2]")

    driver.implicitly_wait(3)

    print(Data)
    print(DataOdds)

    # Converto PandasDataframe

    df1 = pd.DataFrame(Data)
    df2 = pd.DataFrame(DataOdds)

    df1 = df1[::-1].reset_index(drop=True)
    df2 = df2[::-1].reset_index(drop=True)

    df1.columns = ["Home", "Away", "Home Set", "Away Set"]
    df2.columns = ["Home", "Away", "Home Set", "Away Set", "Home Odds", "Away Odds"]

    df1.to_csv("MoscowLiga2022.csv")
    df2.to_csv("MoscowLiga2022WithOdds.csv")





    #How do I add Form??
    # FT
    # Home (Player 1)
    # Away (Player 2)
    # (Miscellaneous Scores)
    # Home (Sets won)
    # Away (Sets won)
    # Home (Odds)
    # Away (Odds)

    #Or

    # FT
    # Home (Player 1)
    # Away (Player 2)
    # (Miscellaneous Scores)
    # Home (Sets Won)
    # Away (Sets Won)
    # No Odds Available

    #Or

    # Time (00:00)
    # Home (Player 1)
    # Away (Player 2)
    # Home (Odds)
    # Away (Odds)



    #
    #We can add form by the following

    #Access Elements by:
    # ID - Guaranteed to be unique (1)
    # CLASS (3)
    # NAME (2)
    # TAG  (4)
    driver.quit()
