from playwright.sync_api import sync_playwright
import requests

forest_url = 'https://know.nifos.go.kr'
folder_name = 'C:\\practice\\ForestSeed\\assets\\'

def download_image(url, filename):
    response = requests.get(url)
    if response.status_code == 200:
        with open(folder_name+filename, 'wb') as f:
            f.write(response.content)
            print("Success to image download")
    else:
        print("Failed to image download")

def page_click(liIdx):
    strPageSelector = f'//*[@id="formSeedpilbkm"]/div/div[3]/div[3]/ul/li[{liIdx}]/a'
    page.click(strPageSelector)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=["--start-maximized"])
    # Chrome 계열의 브라우저. 자동 업데이트 기능 빠짐.
    page = browser.new_page(no_viewport=True) # 창 최대화
    page.goto('https://know.nifos.go.kr/rsrchrsltprcuse/rsrchdtainqire/main.do#AC=/rsrchrsltprcuse/rsrchdtainqire/seedpilbkm/viewPage.do&VA=content&PA=G4Swpg7g+gdgtgXgM5jAEwA4gDYCMDWcAMiEgC5A')
    
    # list check
    page.wait_for_selector('//*[@id="formSeedpilbkm"]/div/div[3]')
    
    page.keyboard.press('End')
    page.wait_for_timeout(500)

    nowPage = int(page.query_selector('//*[@id="page"]').inner_text())
    totalPage = int(page.query_selector('//*[@id="totPage"]').inner_text())
    print(f"total Page : {totalPage}")

    for pageNum in range(1, totalPage+1):
        print(f"{pageNum}번 페이지")
        idx = (pageNum%10)+2
        if(idx == 2):
            idx += 10
        
        page.keyboard.press('End')
        page_click(idx)

        elements = page.query_selector_all('//*[@id="list_body"]/tr')
        for element in elements:
            str_src = element.query_selector('img').get_attribute('src')
            str_alt = element.query_selector('img').get_attribute('alt')
            download_image(forest_url+str_src, str_alt)

        if(idx == 12):
            idx += 1
            page_click(idx)

    browser.close()