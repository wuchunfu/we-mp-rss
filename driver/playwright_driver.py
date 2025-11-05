import os
import platform
import subprocess
import sys
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("检测到playwright未安装，正在自动安装...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "playwright"])
    print("playwright安装完成，正在安装浏览器...")
    subprocess.check_call([sys.executable, "-m", "playwright", "install"])
    from playwright.sync_api import sync_playwright
import json

class PlaywrightController:
    def __init__(self):
        self.system = platform.system().lower()
        self.driver = None
        self.browser = None
        self.context = None
        self.page = None
        self.isClose = True

    def string_to_json(self, json_string):
        try:
            json_obj = json.loads(json_string)
            return json_obj
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
            return ""

    def parse_string_to_dict(self, kv_str: str):
        result = {}
        items = kv_str.strip().split(';')
        for item in items:
            try:
                key, value = item.strip().split('=')
                result[key.strip()] = value.strip()
            except Exception as e:
                pass
        return result

    def add_cookies(self, cookies):
        if self.context is None:
            raise Exception("浏览器未启动，请先调用 start_browser()")
        for cookie in cookies:
            self.context.add_cookies([cookie])

    def add_cookie(self, cookie):
        if self.context is None:
            raise Exception("浏览器未启动，请先调用 start_browser()")
        self.context.add_cookies([cookie])

    def randomize_browser_features(self, mobile_mode=False):
        import random
        if mobile_mode:
            user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
        else:
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 OPR/79.0.4143.72",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Vivaldi/4.3",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36 Brave/1.27.111"
            ]
            user_agent = random.choice(user_agents)
        
        self.context.set_extra_http_headers({"User-Agent": user_agent})
        print(f"浏览器特征设置完成: {'移动端' if mobile_mode else '桌面端'}")
    import os
    def start_browser(self, headless=True, mobile_mode=False, dis_image=False, browser_name="firefox"):
        try:
            if  bool(os.getenv("NOT_HEADLESS",False)):
                headless = False
            if self.driver is None:
                self.driver = sync_playwright().start()
            
            # 根据浏览器名称选择浏览器类型
            if browser_name.lower() == "firefox":
                browser_type = self.driver.firefox
            elif browser_name.lower() == "webkit":
                browser_type = self.driver.webkit
            else:
                browser_type = self.driver.chromium  # 默认使用chromium
            
            self.browser = browser_type.launch(headless=headless)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()

            if mobile_mode:
                self.page.set_viewport_size({"width": 375, "height": 812})

            if dis_image:
                self.context.route("**/*.{png,jpg,jpeg}", lambda route: route.abort())

            self.randomize_browser_features(mobile_mode=mobile_mode)
            self.isClose = False
            return self.page
        except Exception as e:
            print(f"浏览器启动失败: {str(e)}")
            self.cleanup()
            raise

    def __del__(self):
        self.Close()

    def open_url(self, url):
        try:
            self.page.goto(url)
        except Exception as e:
            raise Exception(f"打开URL失败: {str(e)}")

    def Close(self):
        self.cleanup()

    def cleanup(self):
        """清理所有资源"""
        try:
            if hasattr(self, 'page') and self.page:
                self.page.close()
            if hasattr(self, 'context') and self.context:
                self.context.close()
            if hasattr(self, 'browser') and self.browser:
                self.browser.close()
            if hasattr(self, 'playwright') and self.driver:
                self.driver.stop()
            self.isClose = True
        except Exception as e:
            print(f"资源清理失败: {str(e)}")

    def dict_to_json(self, data_dict):
        try:
            return json.dumps(data_dict, ensure_ascii=False, indent=2)
        except (TypeError, ValueError) as e:
            print(f"字典转JSON失败: {e}")
            return ""

# 示例用法
if __name__ == "__main__":
    controller = PlaywrightController()
    try:
        controller.start_browser()
        controller.open_url("https://mp.weixin.qq.com/")
    finally:
        # controller.Close()
        pass