import json
import math
import os
from datetime import timedelta

import dateutil.parser
import pytz
from django.conf import settings
from django_cron import CronJobBase, Schedule

from mad_web.labstatus.models import UTCSBackend, UTCSService


class ArchiveLabsResponse(CronJobBase):
    RUN_EVERY_MINS = 5  # every 5 minutes
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'mad_web.labstatus.cron_tasks.ArchiveLabsResponse'

    @staticmethod
    def should_save(json):
        if not json['meta']['success']:
            return False
        return True

    @staticmethod
    def name_response_subdir(json):
        updated_at = dateutil.parser.parse(json['meta']['updated'])
        time_tuple = updated_at.timetuple()
        return str(time_tuple.tm_year) + "-" + str(time_tuple.tm_yday)

    @staticmethod
    def name_response_file(json):
        updated_at = dateutil.parser.parse(json['meta']['updated'])
        time_tuple = updated_at.timetuple()
        time_bin = math.floor((time_tuple.tm_min + time_tuple.tm_hour * 60) / 5)
        return str(time_bin) + ".json"

    @staticmethod
    def response_paths_for_datetime_window(start, end):
        local = pytz.timezone("America/Chicago")
        start = local.localize(start, is_dst=None)
        start = start.astimezone(pytz.utc)

        end = local.localize(end, is_dst=None)
        end = end.astimezone(pytz.utc)

        stride = timedelta(minutes=5)
        current_date = start
        paths = []
        while current_date < end:
            paths.append(ArchiveLabsResponse.response_path_for_datetime(current_date))
            current_date += stride
        return paths

    @staticmethod
    def response_path_for_datetime(date):
        time_tuple = date.timetuple()
        time_bin = math.floor((time_tuple.tm_min + time_tuple.tm_hour * 60) / 5)
        filename = str(time_bin) + ".json"
        folder_name = str(time_tuple.tm_year) + "-" + str(time_tuple.tm_yday)
        return os.path.join(settings.MEDIA_ROOT, folder_name, filename)

    def do(self):
        backend = UTCSBackend(settings.UTCS_API_KEY)
        response = backend.raw_request(UTCSService.Labs)
        data = json.loads(response.text)
        if not self.should_save(data):
            return
        response_sub_dir = self.name_response_subdir(data)
        filename = self.name_response_file(data)
        path = os.path.join(settings.MEDIA_ROOT, response_sub_dir)
        filepath = os.path.join(path, filename)
        if not os.path.exists(path):
            os.makedirs(path)
        with open(filepath, 'w') as file:
            file.write(response.text)
