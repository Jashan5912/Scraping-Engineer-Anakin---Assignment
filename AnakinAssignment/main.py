import json
from selenium import webdriver
from time import sleep

driver = webdriver.Chrome()
driver.get("https://food.grab.com/sg/en/restaurants")

driver.maximize_window()

def write_json(new_data, filename="restaurants.json"):
    with open(filename, "r+") as file:
        file_data = json.load(file)
        file_data["restaurants"].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent=4)

for i in range(15):
    data = driver.find_element("id", "__NEXT_DATA__").get_attribute("innerHTML")
    parsedData = json.loads(data)

    restaurantLists = parsedData["props"]["initialReduxState"]["pageRestaurantsV2"][
        "entities"
    ]["restaurantList"]

    for key in restaurantLists:
        restaurant = {}
        restaurant["title"] = restaurantLists[key]["name"]
        restaurant["latitude"] = restaurantLists[key]["latitude"]
        restaurant["longitude"] = restaurantLists[key]["longitude"]
        write_json(restaurant)

    load_more = driver.find_element(
        "xpath", '//*[@id="page-content"]/div[4]/div/div/div[4]/div/button'
    )
    load_more.click()
    sleep(10)


driver.quit()
