import requests
from lxml import etree
from bs4 import BeautifulSoup
from openpyxl import Workbook
from random import sample
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='file for results')
    parser.add_argument('num', help='number of courses', type=int)
    args = parser.parse_args()
    return args.path, args.num


def fetch_courses_list():
    site_map_url = 'https://www.coursera.org/sitemap~www~courses.xml'
    site_map = requests.get(site_map_url)
    xml_tree = etree.fromstring(site_map.content)
    namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    courses = [loc.text for loc in xml_tree.xpath(
        '//ns:loc',
        namespaces=namespaces)]
    return courses


def fetch_html_tree(course_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/50.0.2661.102 Safari/537.36',
    }
    request = requests.get(course_url, headers=headers)
    request.raise_for_status()
    raw_html = request.content
    soup = BeautifulSoup(raw_html, 'lxml')
    return soup


def get_course_info(soup):
    course_info = {}
    course_info['title'] = soup.find(
        'h1',
         class_='title display-3-text').get_text()
    course_info['lang'] = soup.find('div', class_='rc-Language').get_text()
    course_info['course_length'] = len(soup.find_all('div', class_='week'))
    course_info['start_dt'] = soup.find('div', class_='startdate').get_text()

    score_element = soup.find('div', class_='ratings-text bt3-visible-xs')

    course_info['av_score'] = (score_element.get_text()
                               if score_element else 'No scores')
    return course_info


def make_courses_workbook(courses_info):
    work_book = Workbook()
    work_sheet = work_book.active
    header = [
        'Title',
        'Language',
        "User's score",
        'Course length',
        'Start date',
    ]

    work_sheet.append(header)
    for course in courses_info:
        work_sheet.append([
            course['title'],
            course['lang'],
            course['av_score'],
            course['course_length'],
            course['start_dt'],
        ])
    return work_book


def save_workbook_to_file(workbook, file_path):
    workbook.save(file_path)


if __name__ == '__main__':
    file_path, num_of_courses = parse_arguments()
    courses_urls = fetch_courses_list()
    courses_urls = sample(courses_urls, num_of_courses)

    print('Requesting coursera...')
    courses_info = []
    for course_url in courses_urls:
        try:
            print('parsing {}'.format(course_url))
            soup = fetch_html_tree(course_url)
            courses_info.append(get_course_info(soup))
        except requests.exceptions.HTTPError as err:
            print("Couldn't request information to {}. {}".format(
                course_url,
                err))
        except AttributeError:
            print("Couldn't parse web page {}".format(course_url))

    courses_workbook = make_courses_workbook(courses_info)
    save_workbook_to_file(courses_workbook, file_path)
    print('Information recorded to {}'.format(file_path))
