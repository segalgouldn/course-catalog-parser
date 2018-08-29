# Noah Segal-Gould, 28 August 2018

import requests
import json

from bs4 import BeautifulSoup
from timeit import default_timer as timer


def make_course_list(urls, has_new_distributions=True, division_between_dates_and_times=False):
    course_list = []
    for url in urls:
        season = url.split("/")[5]
        department = url.split("/")[6].replace(".html", "").replace(".htm", "")
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        unchunked_widths = [int(w.get("width", "0")) for w in soup.find_all("td")]
        widths = [x for x in [unchunked_widths[i:i + 7] for i in range(0, len(unchunked_widths), 7)] if 0 not in x]

        course_reg_numbers = []
        for i in range(len(widths)):
            course_reg_numbers = [int(crn.text.replace("\n", " ").split()[0]) for crn in
                                  soup.find_all("td", {"width": str(widths[i][0])}) if len(crn.text) >= 5]
            if len(course_reg_numbers) >= 1:
                break

        course_codes = []
        course_titles = []
        for i in range(len(widths)):
            try:
                course_numbers_and_titles = [[p.text for p in td.find_all("p")] for td in
                                             soup.find_all("td", {"width": str(widths[i][1])})]
                course_codes = [" ".join(
                    d[0].replace("\xa0", "").replace("\r\n", "").replace("\n", "").replace("\r", "").strip().split())
                                for d in course_numbers_and_titles]
                course_titles = [" ".join(
                    d[1].replace("\xa0", "").replace("\r\n", "").replace("\n", "").replace("\r", "").strip().split())
                                 for d in course_numbers_and_titles]
                if len(course_codes) >= 1 and len(course_list) >= 1:
                    break
            except IndexError:
                break

        professors = []
        for i in range(len(widths)):
            professors = [" ".join(
                prof.text.replace("\xa0", " ").replace("\n", " ").replace("\r", " ").replace("Lab:", "").replace("LAB:",
                                                                                                                 "").replace(
                    "Screening:", "").strip().split()) for prof in soup.find_all("td", {"width": str(widths[i][2])})]
            if len(professors) >= 1:
                break

        schedules = []
        if has_new_distributions and not division_between_dates_and_times:
            for i in range(len(widths)):
                schedules = [" ".join(
                    dt.text.replace("\xa0", " ").replace("\n", " ").replace("\r", " ").replace(" \u2013 ", "-").replace(
                        ".", " ").strip().split()) for dt in soup.find_all("td", {"width": str(widths[i][3])})]
                if len(schedules) >= 1:
                    break
        else:
            for i in range(len(widths)):
                try:
                    schedules_part_1 = [" ".join(
                        dt.text.replace("\xa0", " ").replace("\n", " ").replace("\r", " ").replace(" \u2013 ",
                                                                                                   "-").replace(".",
                                                                                                                " ").strip().split())
                                        for dt in soup.find_all("td", {"width": str(widths[i][3])})]
                    schedules_part_2 = [" ".join(
                        dt.text.replace("\xa0", " ").replace("\n", " ").replace("\r", " ").replace(" \u2013 ",
                                                                                                   "-").replace(".",
                                                                                                                " ").strip().split())
                                        for dt in soup.find_all("td", {"width": str(widths[i][4])})]
                    schedules = [schedules_part_1[j] + " " + schedules_part_2[j] for j in range(len(schedules_part_2))]
                    if len(schedules) >= 1:
                        break
                except IndexError:
                    break

        locations = []
        if has_new_distributions and not division_between_dates_and_times:
            for i in range(len(widths)):
                locations = [dt.text.replace("\xa0", " ").replace("\n", " ").replace("\r", "").strip() for dt in
                             soup.find_all("td", {"width": str(widths[i][4])})]
                if len(locations) >= 1:
                    break
        elif not has_new_distributions and not division_between_dates_and_times:
            for i in range(len(widths)):
                locations = [dt.text.replace("\xa0", " ").replace("\n", " ").replace("\r", "").strip() for dt in
                             soup.find_all("td", {"width": str(widths[i][4])})]
                if len(locations) >= 1:
                    break
        else:
            for i in range(len(widths)):
                locations = [dt.text.replace("\xa0", " ").replace("\n", " ").replace("\r", "").strip() for dt in
                             soup.find_all("td", {"width": str(widths[i][5])})]
                if len(locations) >= 1:
                    break

        old_distributions = []
        if has_new_distributions and not division_between_dates_and_times:
            for i in range(len(widths)):
                try:
                    old_distributions = [dt.text.replace("\xa0", "").replace("\n", " ").replace("\r", " ").strip() for
                                         dt in soup.find_all("td", {"width": str(widths[i][6])})]
                    if len(old_distributions) >= 1:
                        break
                except IndexError:
                    break
        elif not has_new_distributions and division_between_dates_and_times:
            for i in range(len(widths)):
                try:
                    old_distributions = [dt.text.replace("\xa0", "").replace("\n", " ").replace("\r", " ").strip() for
                                         dt in soup.find_all("td", {"width": str(widths[i][6])})]
                    if len(old_distributions) >= 1:
                        break
                except IndexError:
                    break
        elif not has_new_distributions and not division_between_dates_and_times:
            for i in range(len(widths)):
                try:
                    old_distributions = [dt.text.replace("\xa0", "").replace("\n", " ").replace("\r", " ").strip() for
                                         dt in soup.find_all("td", {"width": str(widths[i][5])})]
                    if len(old_distributions) >= 1:
                        break
                except IndexError:
                    break
        else:
            old_distributions = [""] * len(course_reg_numbers)

        new_distributions = []
        if has_new_distributions and not division_between_dates_and_times:
            for i in range(len(widths)):
                new_distributions = [dt.text.replace("\xa0", "").replace("\n", " ").replace("\r", " ").strip() for dt in
                                     soup.find_all("td", {"width": str(widths[i][5])})]
                if len(new_distributions) >= 1:
                    break
        else:
            new_distributions = [""] * len(course_reg_numbers)

        descriptions = [
            s.parent.find_next_sibling('p').text.replace(b"\xd0\xb0".decode("utf-8"), "").replace("\xa0", "").replace(
                "\r\n", " ").replace("\u201c", "\"").replace("\u201d", "\"") for s in soup.find_all("tr") if
            s.parent.find_next_sibling('p') is not None]

        urls = [url] * len(course_reg_numbers)
        seasons = [season] * len(course_reg_numbers)
        departments = [department] * len(course_reg_numbers)

        final_list = [{"course_registration_number": crn,
                       "course_code": c,
                       "professors": p,
                       "schedules": s,
                       "locations": l,
                       "new_distributions": n,
                       "old_distributions": o,
                       "url": u,
                       "season": se,
                       "department": d,
                       "description": de,
                       "course_title": ct} for crn, c, p, s, l, n, o, u, se, d, de, ct in zip(course_reg_numbers,
                                                                                              course_codes,
                                                                                              professors,
                                                                                              schedules,
                                                                                              locations,
                                                                                              new_distributions,
                                                                                              old_distributions,
                                                                                              urls,
                                                                                              seasons,
                                                                                              departments,
                                                                                              descriptions,
                                                                                              course_titles)]
        course_list.extend(final_list)
    return course_list


def process_input(filename, has_new_distributions=True, division_between_dates_and_times=False):
    start = timer()
    with open(filename) as fp:
        input_urls = fp.read().split()
        final_output = make_course_list(input_urls, has_new_distributions, division_between_dates_and_times)
        print(filename + " output number of courses: " + str(len(final_output)))
        with open(filename + "_output.json", "w") as fn:
            json.dump(final_output, fn, sort_keys=True, indent=4)
            end = timer()
            print("Time elapsed: " + str(round(end - start)) + " seconds")
        return final_output


def main():
    top_courses = process_input("urls_new_distributions.txt")
    middle_courses = process_input("urls_spring_2016.txt",
                                   has_new_distributions=False,
                                   division_between_dates_and_times=False)
    bottom_courses = process_input("urls_old_distributions.txt",
                                   has_new_distributions=False,
                                   division_between_dates_and_times=True)

    all_courses = top_courses + middle_courses + bottom_courses
    with open("bard_courses.json", "w") as fn:
        json.dump(all_courses, fn, sort_keys=True, indent=4)
    print("Total output number of courses: " + str(len(all_courses)))


main()
