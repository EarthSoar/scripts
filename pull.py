import os.path
import time

import html2text as html2text
import requests
from bs4 import BeautifulSoup
import re

front_page = "https://learn.lianglianglee.com"


def get_title_and_content(soup, base_url):
    article_content = soup.find("div", {"class": "book-content"})
    for img_tag in article_content.find_all("img", {"src": re.compile(r'^assets/.*')}):
        img_tag['src'] = base_url + "/" + img_tag['src']

    a_tag = article_content.find("a", href="https://www.aliyun.com/minisite/goods?userCode=lc4iupk4")
    if a_tag:
        a_tag.decompose()

    content = f"# {soup.title.text}\n\n{article_content}"

    # 使用 html2text 将 HTML 转换为 Markdown
    converter = html2text.HTML2Text()
    markdown_content = converter.handle(content)
    return soup.title.text, markdown_content


def get_all_books_titles():
    resp = requests.get(front_page)
    resp.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    a_tags = soup.find("div", {"class": "book-post"}).find_all("a")
    return a_tags


def get_html_soup(url) -> BeautifulSoup:
    time.sleep(30)
    resp = requests.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup


def main():
    books = get_html_soup(front_page).find("div", {"class": "book-post"}).find_all("a")
    for book in books:
        if book.text == '阿里云2C2G3M 99元/年，老用户也可以哦':
            continue
        book_dir_a = get_html_soup(front_page + book.get('href')).find("div", {"class": "book-post"}).find_all("a")
        for dir in book_dir_a:
            if dir.text == '阿里云2C2G3M 99元/年，老用户也可以哦':
                continue
            title, content = get_title_and_content(get_html_soup(front_page + dir.get('href')), front_page + book.get('href'))
            os.makedirs(os.path.join("books", book.text.strip()), exist_ok=True)
            file_path = os.path.join("books", book.text.strip(), title + ".md")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)
            print(f"Markdown文件已保存为 {title}")


if __name__ == '__main__':
    main()
