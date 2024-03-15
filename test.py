import schedule
import time
        
def job():
    print("Функция запущена!")
schedule.every(1).second.do(job)

schedule.run_pending()
time.sleep(1)