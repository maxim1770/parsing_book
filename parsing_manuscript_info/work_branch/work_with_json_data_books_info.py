import json
import os
import re
import re_functions_for_collect_data_books_info as re_functions


def work_with_data_book_info(data_book_info: dict):
    new_data_book_info = {
        'date': '1531',
        'sheets_number': 350,
    }

    for key in new_data_book_info.keys():
        try:
            data_book_info[key] = new_data_book_info[key]
        except KeyError as key_err:
            pass

    return data_book_info


def write_data_book_json_book(version: str, data_book: dict, title_book_eng_for_link: str, cur_time: str):
    with open(f'data/data_books/books/{title_book_eng_for_link}/{cur_time}/{version}_data_book.json', "w",
              encoding="utf-8") as json_file:
        json.dump(data_book, json_file, indent=4, ensure_ascii=False)


def write_data_book_json_books(version: str, data_book: dict, cur_time: str, count_iteration: int):
    with open(f'data/data_books/all_books/{cur_time}/{version}_data_books.json', "a",
              encoding="utf-8") as json_file:
        if count_iteration != 0:
            json_file.write(',\n')
        json.dump(data_book, json_file, indent=4, ensure_ascii=False)


def read_data_books_json(version: str, cur_time: str):
    with open(f'data/data_books/all_books/{cur_time}/{version}_data_books.json',
              encoding="utf-8") as json_file:
        return json.load(json_file)


def read_data_book_json(version: str, title_book_eng_for_link: str, cur_time: str):
    with open(f'data/data_books/books/{title_book_eng_for_link}/{cur_time}/{version}_data_book.json',
              encoding="utf-8") as json_file:
        return json.load(json_file)


def edit_data_book_title(data_book_info: dict):
    try:
        title = data_book_info['title']
    except KeyError as key_err:
        print(f"[my_ERROR]: {key_err}")
        return {}
    else:
        edited_title = re_functions.edit_title(title)
        return {'title': edited_title}


def edit_data_book_date(data_book_info: dict):
    try:
        date = data_book_info['date']
    except KeyError as key_err:
        print(f"[my_ERROR]: {key_err}")
        return {}
    else:
        edited_date = re_functions.edit_date(date)
        return {'date': edited_date}


def edit_data_book_sheets_number(data_book_info: dict):
    try:
        sheets_number_str = data_book_info['sheets_number']
    except KeyError as key_err:
        print(f"[my_ERROR]: {key_err}")
        return {}
    else:
        sheets_number_int = re_functions.edit_sheets_number_to_int(sheets_number_str)
        return {'sheets_number': sheets_number_int}


def edit_data_book_owner(data_book_info: dict):
    try:
        owner = data_book_info['owner']
    except KeyError as key_err:
        print(f"[my_ERROR]: {key_err}")
        return {}
    else:
        edited_owner = re_functions.edit_owner(owner)
        return {'owner': edited_owner}


def edit_data_book_info(data_book_info):
    edited_data_book_info = {}

    edited_data_book_info.update(edit_data_book_title(data_book_info))
    edited_data_book_info.update(edit_data_book_date(data_book_info))
    edited_data_book_info.update(edit_data_book_sheets_number(data_book_info))
    edited_data_book_info.update(edit_data_book_owner(data_book_info))

    return edited_data_book_info


def manager_edit_data_book(data_book, cur_time):
    edited_data_book = {}
    edited_data_book['title_book_eng_for_link'] = data_book['title_book_eng_for_link']
    edited_data_book['info'] = edit_data_book_info(data_book['info'])

    write_data_book_json_book('edit', edited_data_book, data_book['title_book_eng_for_link'], cur_time)


def manager_edit_data_books(data_books, cur_time):
    with open(f'data/data_books/all_books/{cur_time}/edit_data_books.json', "w",
              encoding="utf-8") as json_file:
        json_file.write('[\n')
    # -----
    count_iteration = 0
    # -----
    for data_book in data_books[:2]:
        title_book_eng_for_link = data_book['title_book_eng_for_link']
        # ---
        print(f"INFO, Итерация: {count_iteration}, Название: {title_book_eng_for_link}")
        # ---

        manager_edit_data_book(data_book, cur_time)

        edited_data_book = read_data_book_json('edit', title_book_eng_for_link, cur_time)

        write_data_book_json_books('edit', edited_data_book, cur_time, count_iteration)

        # -----
        count_iteration += 1
        # -----
        # ---
        print(*["-" * 20] * 3, sep='\n')
        # ---

    with open(f'data/data_books/all_books/{cur_time}/edit_data_books.json', "a",
              encoding="utf-8") as json_file:
        json_file.write('\n]')


def manager_merge_json_files(title_book_eng_for_link, cur_time: str):
    data_book = read_data_book_json("collect", title_book_eng_for_link, cur_time)

    edited_data_book = read_data_book_json("edit", title_book_eng_for_link, cur_time)

    finished_data_book = {}

    finished_data_book.update(data_book)
    finished_data_book.update(edited_data_book)

    write_data_book_json_book('finished', finished_data_book, title_book_eng_for_link, cur_time)


def manager_merges_json_files(data_books, cur_time: str):
    with open(f'data/data_books/all_books/{cur_time}/finished_data_books.json', "w",
              encoding="utf-8") as json_file:
        json_file.write('[\n')
    # -----
    count_iteration = 0
    # -----
    for data_book in data_books[:2]:
        title_book_eng_for_link = data_book['title_book_eng_for_link']
        # ---
        print(f"INFO, Итерация: {count_iteration}, Название: {title_book_eng_for_link}")
        # ---

        manager_merge_json_files(title_book_eng_for_link, cur_time)

        finished_data_book = read_data_book_json('finished', title_book_eng_for_link, cur_time)

        write_data_book_json_books('finished', finished_data_book, cur_time, count_iteration)

        # -----
        count_iteration += 1
        # -----
        # ---
        print(*["-" * 20] * 3, sep='\n')
        # ---

    with open(f'data/data_books/all_books/{cur_time}/finished_data_books.json', "a",
              encoding="utf-8") as json_file:
        json_file.write('\n]')


def main():
    cur_time = '18_07_2022_11_26'
    data_books = read_data_books_json("collect", cur_time)
    manager_edit_data_books(data_books, cur_time)

    manager_merges_json_files(data_books, cur_time)


if __name__ == "__main__":
    main()
