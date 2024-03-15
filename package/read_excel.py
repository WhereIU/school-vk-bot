import requests
import openpyxl

url = 'https://docs.google.com/spreadsheets/d/1yuhlcb4CCFFL3P1tGAEImSyThBg9WSSQZbxEj4H6L_k/export?format=xlsx&id=1yuhlcb4CCFFL3P1tGAEImSyThBg9WSSQZbxEj4H6L_k'
r = requests.get(url)
open('schedule.xlsx', 'wb').write(r.content)
book = openpyxl.open("schedule.xlsx")
sheet = book.active

schedule_time = []
for row in range (6, 11):
    schedule_time.append(sheet[row][1].value.replace('\n', '-'))

groups_info = {}
for row in range(6, sheet.max_row - 1):
    if sheet[row][0].value != None:
        group = sheet[row][0].value
        groups_info[group] = [[],[],[],[],[]]
    for coll in range(2, 7):
        current_item = sheet[row][coll].value
        if current_item is not None:
            current_item = current_item.split('\n')
        groups_info[group][(coll - 2) % 5].append(current_item)
book.save('schedule.xlsx')
