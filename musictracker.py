import os
import openpyxl
from openpyxl.styles import Font
import sqlite3

filename = 'C:/Users/Tengwei/Desktop/Music/MusicStats.xlsx'
directory = 'C:/Users/Tengwei/Desktop/Music'


def get_music_score(songname):
    global filename
    wb = openpyxl.load_workbook(filename)

    for sheetname in wb.sheetnames:
        sheet = wb[sheetname]
        for row in range(3, sheet.max_row + 1):
            if sheet.cell(row=row, column=2).value == songname:
                print(sheet.cell(row=row, column=3).value)
                return sheet.cell(row=row, column=3).value

    wb.close()


def change_music_score(songname, score):
    global filename
    wb = openpyxl.load_workbook(filename)

    for sheetname in wb.sheetnames:
        sheet = wb[sheetname]
        for row in range(3, sheet.max_row + 1):
            if sheet.cell(row=row, column=2).value == songname:
                sheet.cell(row=row, column=3).value += score
                print("Added score")

    wb.save(filename)
    wb.close()


def update_music_list():
    # Adds the new songs added. If a whole new genre is added it creates a new sheet for the genre
    global filename
    global directory
    wb = openpyxl.load_workbook(filename)

    for sheetname in os.listdir(directory):
        if os.path.isdir(f'{directory}/{sheetname}'):
            try:
                sheet = wb[sheetname]
                average_score = get_average_score(sheetname)
            except:
                sheet = wb.create_sheet(sheetname)
                average_score = 20
            sheet.cell(row=2, column=2).value = "Song Title"
            sheet.cell(row=2, column=2).font = Font(bold=True)
            sheet.cell(row=2, column=3).value = "Tracking Score"
            sheet.cell(row=2, column=3).font = Font(bold=True)
            for i, file in enumerate(os.listdir(f'C:/Users/Tengwei/Desktop/Music/{sheetname}')):
                print(i, file)
                music_file_added = False
                for i in range(sheet.max_row):
                    if file == sheet.cell(row=i + 3, column=2).value:
                        music_file_added = True
                        break

                if not music_file_added:
                    for i in range(sheet.max_row + 1):
                        if sheet.cell(row=i + 3, column=2).value is None:
                            sheet.cell(row=i + 3, column=2).value = file
                            sheet.cell(row=i + 3, column=3).value = average_score
                            break

    wb.save(filename)
    wb.close()


def get_average_score(sheetname):
    global filename
    wb = openpyxl.load_workbook(filename)

    total_score = 0
    sheet = wb[sheetname]
    for row in range(3, sheet.max_row + 1):
        total_score += sheet.cell(row=row, column=3).value

    average_score = round(total_score / (sheet.max_row - 2), 3) if sheet.max_row > 2 else 20
    wb.close()
    return average_score


if __name__ == "__main__":
    update_music_list()
