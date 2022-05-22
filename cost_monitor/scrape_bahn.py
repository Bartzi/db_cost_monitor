import re
import time
from tracemalloc import start

from playwright.sync_api import Playwright, sync_playwright, expect


TIME_RE = re.compile('(?P<time>\d\d:\d\d)')
TIME_PATTERN = "%H:%M"

def extract_times(results_container):
    connections = results_container.query_selector_all(".overviewConnection")

    last_start_time = time.strptime("00:00", TIME_PATTERN)

    for connection in connections:
        connection_times = connection.query_selector_all(".connectionTime")
        assert len(connection_times) == 1, "found more than one connection time, something is wrong?"
        connection_time = connection_times[0]
        start_time = TIME_RE.search(connection_time.query_selector(".timeDep").inner_text()).group('time')
        end_time = TIME_RE.search(connection_time.query_selector(".timeArr").inner_text()).group('time')

        found_start_time = time.strptime(start_time, TIME_PATTERN)
        if found_start_time > last_start_time:
            last_start_time = found_start_time

        print(start_time)
        print(end_time)

    return last_start_time

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()

    # Open new page
    page = context.new_page()

    # Go to https://www.bahn.de/
    page.goto("https://www.bahn.de/")

    # Click button:has-text("Cookie settings")
    page.locator("button:has-text(\"Cookie settings\")").click()

    # Click text=Allow selected cookies
    page.locator("text=Allow selected cookies").click()

    # Click input[name="S"]
    page.locator("input[name=\"S\"]").click()

    # Fill input[name="S"]
    page.locator("input[name=\"S\"]").fill("München Hbf")

    # Press Tab
    page.locator("input[name=\"S\"]").press("Tab")

    # Fill input[name="Z"]
    page.locator("input[name=\"Z\"]").fill("Berlin hbf")

    date_input = page.locator("input[name=\"date\"]")
    date_input.evaluate("(node) => node.removeAttribute('readonly')")
    date_input.fill("Do, 14.07.2022")

    # Click input[name="time"]
    page.locator("input[name=\"time\"]").click()

    # Fill input[name="time"]
    page.locator("input[name=\"time\"]").fill("13:00")

    # Click input:has-text("Suchen")
    # with page.expect_navigation(url="https://reiseauskunft.bahn.de/bin/query.exe/dn?revia=yes&existOptimizePrice-deactivated=1&country=DEU&dbkanal_007=L01_S01_D001_qf-bahn-svb-kl2_lz03&start=1&protocol=https%3A&S=M%C3%BCnchen+Hbf&REQ0JourneyStopsSID=&Z=Berlin+hbf&REQ0JourneyStopsZID=&date=Do%2C+14.07.2022&time=13%3A00&timesel=depart&returnDate=&returnTime=&returnTimesel=depart&optimize=0&auskunft_travelers_number=1&tariffTravellerType.1=E&tariffTravellerReductionClass.1=0&tariffClass=2&rtMode=DB-HYBRID&externRequest=yes&HWAI=JS%21js%3Dyes%21ajax%3Dyes%21&externRequest=yes&HWAI=JS%21js%3Dyes%21ajax%3Dyes%21#hfsseq1|mp.02695317.1652630071"):
    with page.expect_navigation():
        page.locator("input:has-text(\"Suchen\")").click()
    # expect(page).to_have_url("https://reiseauskunft.bahn.de/bin/query.exe/dn?revia=yes&existOptimizePrice-deactivated=1&country=DEU&dbkanal_007=L01_S01_D001_qf-bahn-svb-kl2_lz03&start=1&protocol=https%3A&S=M%C3%BCnchen+Hbf&REQ0JourneyStopsSID=&Z=Berlin+hbf&REQ0JourneyStopsZID=&date=Do%2C+14.07.2022&time=13%3A00&timesel=depart&returnDate=&returnTime=&returnTimesel=depart&optimize=0&auskunft_travelers_number=1&tariffTravellerType.1=E&tariffTravellerReductionClass.1=0&tariffClass=2&rtMode=DB-HYBRID&externRequest=yes&HWAI=JS%21js%3Dyes%21ajax%3Dyes%21&externRequest=yes&HWAI=JS%21js%3Dyes%21ajax%3Dyes%21")

    # ---------------------

    results = page.wait_for_selector("#resultsOverviewContainer")
    while True:
        last_start_time = extract_times(results)
        if last_start_time > time.strptime("18:00", TIME_PATTERN):
            break

        later_button = results.query_selector(".later")
        with page.expect_navigation():
            later_button.click()
        results = page.wait_for_selector("#resultsOverviewContainer")
        print("new round")

    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
