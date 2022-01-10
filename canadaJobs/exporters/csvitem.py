# -*- coding: utf-8 -*-
from scrapy.utils.project import get_project_settings
from scrapy.exporters import CsvItemExporter

class JobCsvItemExporters(CsvItemExporter):

    def __init__(self, *args, **kwargs):
        settings    = get_project_settings()
        delimiter   = settings['CSV_DELIMITER']
        kwargs['delimiter'] = delimiter
        fields_to_export    = settings['FIELDS_TO_EXPORT']
        file_name = settings['FEED_URI']
        # print('----------- fields_to_export', fields_to_export)
        if fields_to_export :
            kwargs['fields_to_export'] = fields_to_export

        if not file_name:
            file_name = args['name']

        # print('---------------------------------- settings', file_name, settings)
        # print('---------------------------------- args', args)
        # print('---------------------------------- kwargs', kwargs)


        #  ERROR: Error caught on signal handler: <bound method FeedExporter.open_spider of <scrapy.extensions.feedexport.FeedExporter object at
        # 感觉是哪个Item输出的时候，没有遵循scrapy的feedexport相关的规则，我在settings里面禁用了feedexporter，就不显示了
        # EXTENSIONS = {'scrapy.extensions.feedexport.FeedExporter': None}
        # super(JobCsvItemExporters, self).__init__(*args, True, ';', None, **kwargs)
        super(JobCsvItemExporters, self).__init__(*args)


