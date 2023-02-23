import os
import re


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


if __name__ == '__main__':
    files = os.listdir('books/')
    for file in files:
        book: str = open_file('books/%s' % file)
        chapters = re.split(r'\n\n\n\nChapter\s[0-9]\..*(\n\n)', book)
        chapter_names = re.findall(r'\n\n\n\nChapter\s[0-9]\..*', book)
        filename = 'ex1.txt'
        chapters = list(filter(lambda cad: cad != '\n\n', chapters))
        # remove the introduction
        chapters.pop(0)
        # print(chapters)
        print(len(chapter_names))
        print(len(chapters))
        count = 1
        for chapter in chapters:
            chapter_to_txt = chapter_names[count-1].replace('\n\n\n\n', '') + '\n' + chapter.replace('\n\n\n\n\n', '').replace('\n\n\n\n', '').replace('\n\n\n', ' ').replace('\n\n', ' ')
            if count < 10:
                filename = file.replace('.txt', '000%s.txt' % count)
            elif count < 100:
                filename = file.replace('.txt', '00%s.txt' % count)
            elif count < 1000:
                filename = file.replace('.txt', '0%s.txt' % count)
            save_file(chapter_to_txt, 'chapters/%s' % filename)
            count += 1
