import schedule
import time
import subprocess
import platform

# Find python path automatically
PYTHON_CMD = "python3" if platform.system() != "Windows" else "python"

def run_scrapy():
    print("🚀 Scrapy working...")
    subprocess.run(["scrapy", "crawl", "amazon"])

# Run every hour
schedule.every().hour.at(":00").do(run_scrapy)

print("⏳ Scheduler started. Scrapy works every 1 hour.")

while True:
    schedule.run_pending()
    time.sleep(60) # check every minute