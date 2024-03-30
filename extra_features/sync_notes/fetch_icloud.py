from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import sys
import os
from subprocess import check_output as co


def click_at_percentage(
    *,
    clicks,
    click_mode='left',
    wait_between_clicks=1.0,
    click_colors,
    absolute=True,
    download_wait_time=30,
    load_time=3,
    url,
    debug=False,
):
    url_stripped = url.replace('https://', '')
    if not url_stripped.startswith('share.icloud.com'):
        raise ValueError('URL must be an iCloud URL')

    chrome_opts = Options()
    if not debug:
        chrome_opts.add_argument("--headless")
    # chrome_opts.add_argument("--headless")
    # chrome_opts.add_argument("window-size=100x100")
    try:
        driver = webdriver.Chrome(
            options=chrome_opts
        )  # Adjust this to match your browser
        driver.get(url)  # Replace with your target URL

        if debug:
            driver.set_window_size(450, 550)
        else:
            driver.set_window_size(500, 411)

        def place_dot_helper(color):
            driver.execute_script(
                f"var d=document.createElement('div');d.style.position='absolute';d.style.left='{target_x}px';d.style.top='{target_y}px';d.style.width='5px';d.style.height='5px';d.style.backgroundColor='{color}';document.body.appendChild(d);"
            )

        def place_dot(i):
            place_dot_helper(click_colors[i % len(click_colors)])

        time.sleep(load_time)
        # Get the dimensions of the browser window using JavaScript
        width = driver.execute_script("return window.innerWidth;")
        height = driver.execute_script("return window.innerHeight;")

        for i, v in enumerate(clicks):
            xx, yy = v
            # Calculate the target coordinates as percentages
            if not absolute:
                target_x = int(width * xx)
                target_y = int(height * yy)
            else:
                target_x = int(width * xx)
                target_y = int(height * yy)
                # target_x = xx * fudge_width
                # target_y = yy * fudge_height

            # Create an instance of ActionChains
            actions = ActionChains(driver)

            print(f'{width=},{height=},{target_x=},{target_y=}')
            # Move the cursor to the calculated coordinate based on percentage input
            # Selenium starts from the top-left corner (0, 0) by default
            if click_mode == 'left':
                actions.move_by_offset(target_x, target_y).click().perform()
            else:
                actions.move_by_offset(
                    target_x, target_y
                ).context_click().perform()

            place_dot(i)
            actions.move_by_offset(-target_x, -target_y).click().perform()
            place_dot(i)
            time.sleep(wait_between_clicks)

        # Optional: Reset mouse position, might be useful in some scenarios

        # driver.execute_script(
        #     "document.querySelectorAll('ui-button')[5].click()"
        # )

        time.sleep(download_wait_time)
        # Clean up: Close the browser window
        driver.quit()
    except Exception as e:
        print(e)
        time.sleep(download_wait_time)
        driver.quit()


def download_share_link(url):
    # Example usage: Right-click at 50% width and 50% height of the screen
    rel_clicks = [(0.85, 0.95), (0.5, 0.8)]
    clicks = [(0, 0), (1200, 600), (400, 400)]
    click_mode = 'left'
    colors = ['red', 'blue', 'green']
    wait_between_clicks = 1.0
    absolute = False
    clicks = clicks if absolute else rel_clicks
    download_wait_time = 3
    debug = True
    load_time = 3

    # Scale fudge factor to adjust the percentage coordinates
    #     my macbook air is 1440x920, and the rel_clicks defined above
    #     work for that screen size. Therefore, whatever your screen size
    #     is, we need to adjust the coordinates to match the screen size.
    # ref_screen_size = [1440, 736]

    downloads_folder = os.path.expanduser('~/Downloads')
    num_files_in_downloads_folder = len(os.listdir(downloads_folder))
    click_at_percentage(
        clicks=clicks,
        click_mode=click_mode,
        click_colors=colors,
        wait_between_clicks=wait_between_clicks,
        absolute=absolute,
        download_wait_time=download_wait_time,
        load_time=load_time,
        url=url,
        debug=debug,
    )
    post_files = len(os.listdir(downloads_folder))

    if post_files > num_files_in_downloads_folder:
        return True
    else:
        return False


if __name__ == "__main__":
    url = sys.argv[1]
    download_share_link(url)
