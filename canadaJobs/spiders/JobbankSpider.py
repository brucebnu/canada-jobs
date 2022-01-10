import scrapy
import logging
import os
from canadaJobs.items import CanadajobsItem

class JobbankspiderSpider(scrapy.Spider):
    name = 'JobbankSpider'
    allowed_domains = ['www.jobbank.gc.ca']
    start_urls = []

    with open("./canadaJobs/towns.txt") as f:
        cities = f.readlines()

    # 命令格式： scrapy canadaJobs city -a cityName=NB -a sort=D
    def __init__(self, cityName=None, sort=None, *args, **kwargs):
        print('os.getcwd()', os.getcwd())

        i=1
        for city in self.cities:
            # print(i, '< 城市名称 >： ' + city)
            self.start_urls.append('https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=%s&sort=D'%city)
            i = i+1

        super(eval(self.__class__.__name__), self).__init__(*args, **kwargs)


    def parse(self, response):
        # logging.warning("--------------///////////////////////// Start", response);
        print('|||||||||||||||||||||||||||||||||||||||||||================> start_urls', len(self.start_urls))
        self.log('|||||||||||||||||||||||||||||||||||||||||||================> A response from %s just arrived!' % response.url)
        selector = scrapy.Selector(response)

        pages_total = selector.css("span.found::text").extract_first()
        pages = int(pages_total.replace(",", "")) // 25
        self.log("================> Start Pages Total : %s " % pages_total);
        self.log("================> Start Pages : %s"  % pages);

        # 当前页面25条数据
        self._extract_list(selector.css("article"))
        # print('==========================', selector.css("article"))
        for i in range(1, pages + 2):
            # url = response.url + "&page=" + str(i)
            # Session Expired Your session has expired. Please reload the page to continue.
            url = 'https://www.jobbank.gc.ca/jobsearch/job_search_loader.xhtml'
            # print('-------- job_search_loader', url)
            yield scrapy.Request(url, callback=self.parse_ajax, dont_filter=True)

    def parse_ajax(self, response):
        return self._extract_list(response.css("article"))

    def _extract_list(self, article):
        job_info = CanadajobsItem()
        # print('==========================', article)
        # results = response.css("article")
        self.log("================> Extract list start");
        index = 0
        for res in article:
            job_info['title']       = res.css("span.noctitle::text").extract_first().replace('\t', '').replace('\n','')
            job_info['company']     = res.css("li.business::text").extract_first()
            job_info['href']        = "https://www.jobbank.gc.ca" + res.css("a::attr(href)").extract_first()
            job_info['date']        = res.css("li.date::text").extract_first().replace('\t', '').replace('\n','')
            job_info['location']    = res.css("li.location::text").extract()
            job_info['location']    = job_info['location'][-1].strip()
            job_info['salary']      = res.css("ul.list-unstyled > li.salary::text").extract()
            job_info['salary']      = job_info['salary'][-1].strip().replace('\t', '').replace('\n','')
            if not job_info['salary']:
                job_info['salary'] = "N/A"
            index = index + 1
            print("[================> List info ]", index, job_info)
            yield job_info
        return job_info
        self.log("================> Extract list end \r\n\r\n")