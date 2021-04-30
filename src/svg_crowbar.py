from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--verbose")
chrome_options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": "<path_to_download_default_directory>",
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False,
    },
)


def enable_download(browser, download_dir):
    browser.command_executor._commands["send_command"] = (
        "POST",
        "/session/$sessionId/chromium/send_command",
    )
    params = {
        "cmd": "Page.setDownloadBehavior",
        "params": {"behavior": "allow", "downloadPath": download_dir},
    }
    browser.execute("send_command", params)


def download_svg(chart_id):
    driver.get(f"https://datawrapper.dwcdn.net/{chart_id}")
    driver.execute_script(
        "(function () { var e = document.createElement('script'); e.setAttribute('src', 'https://nytimes.github.io/svg-crowbar/svg-crowbar-2.js'); e.setAttribute('class', 'svg-crowbar'); document.body.appendChild(e); })();"
    )
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "button"))
    )
    buttons = driver.find_elements_by_tag_name("button")
    driver.execute_script(
        """
        var buttons = document.querySelectorAll('button');
        for (i=0;i<buttons.length;i++) {
            if (i === 0) {
                continue;
            } else {
                buttons[i].parentNode.remove()
            }
        };
    """
    )
    buttons[0].click()


if __name__ == "__main__":
    from util import load_config

    config = load_config()
    charts = config["charts"]

    driver = webdriver.Chrome(options=chrome_options)
    enable_download(
        driver,
        "img",
    )
    for chart_info in charts:
        if chart_info["type"] != "table":
            download_svg(chart_info["id"])
