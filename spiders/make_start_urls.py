from .info import Info
from urllib.parse import urlencode



def start_request():
    all_start_links = []
    all_city = Info.city_info
    all_job = Info.job_info
    base_url = 'https://m.zhaopin.com/searchjob/search'
    form_data = {
        'KeyWord': '',
        'JobType': '',
        'Industry': '210500',
        'pageIndex': '1',
        'isSchoolJob': '0',
        'Location': '',
        'SF_2_100_32': '2'
    }
    for province in all_city:
        for city in province:
            if type(city) != list:
                continue
            city_id = city[0][1]
            for job_type_1st in all_job:
                for job_type_2nd in job_type_1st:
                    if type(job_type_2nd) != list:
                        continue
                    job_type_2nd_id = job_type_2nd[0][1]
                    form_data['JobType'] = job_type_2nd_id
                    form_data['Location'] = city_id
                    start_url = base_url + '?' +urlencode(form_data)
                    all_start_links.append(start_url)
    return all_start_links