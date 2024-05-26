from flask import request, Flask, jsonify
from flask_restx import Api, Resource, fields, reqparse
from flask_cors import CORS

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC


class Youtube_Video_Collecter(object):
    def __init__(self) -> None:
        self.url = "https://www.youtube.com"
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
    
        # 브라우저 설정 최적화
        chrome_options.add_argument("--no-sandbox")  # 샌드박스 비활성화
        chrome_options.add_argument("--disable-gpu")  # GPU 사용 비활성화
        chrome_options.add_argument("--window-size=1280x1696")  # 창 크기 설정
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")  # 이미지 로드 비활성화

        # 사용자 에이전트 설정 (크롤링 탐지 회피)
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

        # Chrome 프로세스 최적화
        chrome_options.add_argument("single-process")  # 단일 프로세스 모드
        chrome_options.add_argument("--disable-dev-shm-usage")  # 공유 메모리 사용 비활성화
        chrome_options.add_argument("--disable-dev-tools")  # 개발자 도구 비활성화
        chrome_options.add_argument("--no-zygote")  # Zygote 비활성

        # 로깅 비활성화 및 자동화 탐지 회피
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("detach", True)

        
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        self.wait = WebDriverWait(self.driver, 5)

    def get_Profile(self,name:str)->dict:
        ouput_Profile = {
            "name" : None,
            "imag" : None,
            "fans" : None,
            "id" : None
        }
        url:str = self.url+'/results?search_query='+name

        self.driver.get(url=url)

        
        try:
            channel = self.wait.until(
                EC.visibility_of_element_located((By.XPATH, "//*[@id='contents']/ytd-channel-renderer"))
            )
        except:
            print("문제 1")
            return
        
        try:
            channel_name = channel.find_element(By.XPATH, "//*[@id='channel-title'] //*[@id='text']")
            ouput_Profile['name'] = channel_name.text

            channel_imag = channel.find_element(By.XPATH, "//*[@id='avatar-section'] //*[@id='avatar']/yt-img-shadow //*[@id='img']")
            ouput_Profile['imag'] = channel_imag.get_attribute("src")

            channel_fans = channel.find_element(By.XPATH, "//*[@id='info-section'] //*[@id='video-count']")
            ouput_Profile['fans'] = channel_fans.text

            channel_id = channel.find_element(By.XPATH, " //*[@id='info-section'] //*[@id='main-link']")
            ouput_Profile['id'] = channel_id.get_attribute('href')
        except:
            print(ouput_Profile)
            self.driver.close()
            return
        
        return ouput_Profile


    def close(self):
        self.driver.close()

    
        
        











app = Flask(__name__)

api = Api(app=app, title='youtube')

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True)

ns_search = api.namespace('youtube_api')

input_model = api.model('download', {
    "url" :  fields.String(required=True),
    "path" : fields.String(required=True) 
})

@ns_search.route('/search')
class youtube_search(Resource):
    @ns_search.expect(parser)
    def get(self):
        try:
            args = parser.parse_args()
            name = args['name']

        except:
            import traceback
            e = traceback.format_exc()
            

def main():
    dd = Youtube_Video_Collecter()
    ddd = dd.get_Profile("괴물쥐")
    dd.close()
    print(ddd)

if __name__ == "__main__":
    main()