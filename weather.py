# 天气查询 - 和风天气
# https://www.heweather.com/documents/api/s6

import requests


class Weather(object):
    def __init__(self, location):
        self.key = 'ec7b767041bf46129a369623d6159113'
        self.location = location
        self.station = ''
        self.forecast_url = 'https://free-api.heweather.com/s6/weather/forecast?location={}&key={}'.format(self.location, self.key)
        self.aqi_url = 'https://free-api.heweather.com/s6/air?location={}&key={}'.format(self.location, self.key)

    def get_request(self, url):
        resp = requests.get(url)
        return (resp.status_code == 200 and [resp.json()] or [None])[0]

    def wechat(self):
        # parse location/station
        station_info = ['十五厂', '虹口', '徐汇上师大', '杨浦四漂', '青浦淀山湖', '静安监测站', '浦东川沙', '浦东新区监测站', '浦东张江', '普陀']
        if '+' in self.location:
            if self.location.split('+')[0] in station_info:
                self.station = self.location.split('+')[0]
                self.location = self.location.split('+')[1]
                self.station_index = station_info.index(self.station)
            elif self.location.split('+')[1] in station_info:
                self.station = self.location.split('+')[1]
                self.location = self.location.split('+')[0]
                self.station_index = station_info.index(self.station)
            else:
                self.location = self.location
        else:
            self.location = self.location
        
        result_aqi = dict(self.get_request(self.aqi_url))
        result_forecast = dict(self.get_request(self.forecast_url))
        result = ''

        # format forecast
        if result_forecast and result_forecast['HeWeather6'][0].get('status', 'ok') == 'ok':
            result += '         温度  湿度 气压\n'
            for i, element in enumerate(result_forecast['HeWeather6'][0]['daily_forecast']):
                result += '{0} {4}-{3} {5}% {6} {1}/{2}\n'.format(element['date'][5:].replace('-','.').replace('0','',1),
                                                                    element['cond_txt_d'], element['cond_txt_n'],
                                                   element['tmp_max'],element['tmp_min'], element['hum'], element['pres'])
        else:
            return '未知城市（天气），请重新输入。例如：上海天气'

        # format aqi_city
        if result_aqi and result_aqi['HeWeather6'][0].get('status', 'ok') == 'ok':
            air_now_city = result_aqi['HeWeather6'][0]['air_now_city']
            result += '\n城市: {6}\nAQI: {1}\n空气质量: {2}\n主要污染物: {3}\nPM10: {4}\nPM25: {5}\n发布时间: {0}\n\n'.format(
                air_now_city['pub_time'],air_now_city['aqi'],air_now_city['qlty'],air_now_city['main'],air_now_city['pm10'],
                                                            air_now_city['pm25'],self.location)
        else:
            return '未知城市（空气），请重新输入。例如：上海天气+普陀、上海天气'

        # format aqi_area
        if self.station:
            air_now_station = result_aqi['HeWeather6'][0]['air_now_station'][self.station_index]
            result += '监测站: {6}\nAQI: {1}\n空气质量: {2}\n主要污染物: {3}\nPM10: {4}\nPM25: {5}\n发布时间: {0}\n\n'.format(
                air_now_station['pub_time'], air_now_station['aqi'], air_now_station['qlty'], air_now_station['main'],
                air_now_station['pm10'],air_now_station['pm25'],air_now_station['air_sta'])

        # tips
        result += '空气质量监测站（上海）:\n十五厂/虹口/徐汇上师大/杨浦四漂/青浦淀山湖/静安监测站/浦东川沙/浦东新区监测站/浦东张江/普陀\n例如:上海天气+普陀'
        return result

    def wxpy(self):
        # parse location/station
        station_info = ['十五厂', '虹口', '徐汇上师大', '杨浦四漂', '青浦淀山湖', '静安监测站', '浦东川沙', '浦东新区监测站', '浦东张江', '普陀']
        if '+' in self.location:
            if self.location.split('+')[0] in station_info:
                self.station = self.location.split('+')[0]
                self.location = self.location.split('+')[1]
                self.station_index = station_info.index(self.station)
            elif self.location.split('+')[1] in station_info:
                self.station = self.location.split('+')[1]
                self.location = self.location.split('+')[0]
                self.station_index = station_info.index(self.station)
            else:
                self.location = self.location
        else:
            self.location = self.location

        result_aqi = dict(self.get_request(self.aqi_url))
        result_forecast = dict(self.get_request(self.forecast_url))
        result = ''

        # format forecast
        if result_forecast and result_forecast['HeWeather6'][0].get('status', 'ok') == 'ok':
            result += '日期  温度  湿度 气压\n'
            for i, element in enumerate(result_forecast['HeWeather6'][0]['daily_forecast']):
                result += '{0} {4}-{3} {5}% {6} {1}/{2}\n'.format(
                    element['date'][5:].replace('-', '.').replace('0', '', 1),
                    element['cond_txt_d'], element['cond_txt_n'],
                    element['tmp_max'], element['tmp_min'], element['hum'], element['pres'])
        else:
            return '未知城市（天气），请重新输入。例如：上海天气'

        # format aqi_city
        if result_aqi and result_aqi['HeWeather6'][0].get('status', 'ok') == 'ok':
            air_now_city = result_aqi['HeWeather6'][0]['air_now_city']
            result += '\n城市: {6}\nAQI: {1}\n空气质量: {2}\n主要污染物: {3}\nPM10: {4}\nPM25: {5}\n发布时间: {0}\n\n'.format(
                air_now_city['pub_time'], air_now_city['aqi'], air_now_city['qlty'], air_now_city['main'],
                air_now_city['pm10'],
                air_now_city['pm25'], self.location)
        else:
            return '未知城市（空气），请重新输入。例如：上海天气+普陀、上海天气'

        # format aqi_area
        if self.station:
            air_now_station = result_aqi['HeWeather6'][0]['air_now_station'][self.station_index]
            result += '监测站: {6}\nAQI: {1}\n空气质量: {2}\n主要污染物: {3}\nPM10: {4}\nPM25: {5}\n发布时间: {0}\n\n'.format(
                air_now_station['pub_time'], air_now_station['aqi'], air_now_station['qlty'], air_now_station['main'],
                air_now_station['pm10'], air_now_station['pm25'], air_now_station['air_sta'])

        return result


# print(Weather('上海').wechat())
