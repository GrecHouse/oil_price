"""
Sensor to indicate today's korean gas station oil price.
For more details about this platform, please refer to the documentation at
https://github.com/GrecHouse/oil_price

HA 주유소 유가 센서 : 주유소 기름값을 알려줍니다.
"""

import logging
import requests
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from datetime import datetime, timedelta
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME, CONF_TYPE)
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle


_LOGGER = logging.getLogger(__name__)

CONF_STATION_ID = 'station_id'
DEFAULT_NAME = 'Oil Price'
API_URL = 'https://raw.githubusercontent.com/GrecHouse/api/master/oil.json'
SUB_URL = 'https://place.map.kakao.com/main/v/{}?_={}'
OIL_TYPE = {
    '01': ['B034', '고급휘발유'],
    '02': ['B027', '휘발유'],
    '03': ['D047', '경유'],
    '04': ['K015', 'LPG'],
    '05': ['C004', '등유']
}

MIN_TIME_BETWEEN_API_UPDATES = timedelta(seconds=30)
MIN_TIME_BETWEEN_SENSOR_UPDATES = timedelta(seconds=3600)
SCAN_INTERVAL = timedelta(seconds=7200)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_TYPE, default='02'): cv.string,
    vol.Optional(CONF_STATION_ID): vol.All(cv.ensure_list, [cv.string]),
})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up a Oil Price Sensors."""
    name = config.get(CONF_NAME)
    type = config.get(CONF_TYPE)
    ids = config.get(CONF_STATION_ID)
    
    if ids is None:
        ids = ['avg']
    else:
        ids.insert(0, 'avg')
    
    sensors = []
    
    for station_id in ids:
        api = OilPriceAPI(station_id, OIL_TYPE[type])
        sensors += [OilPriceSensor(name, station_id, OIL_TYPE[type], api)]
        
    add_entities(sensors, True)

class OilPriceAPI:
    """OilPrice API."""

    def __init__(self, station_id, type):
        """Initialize the OilPrice API.."""
        self.station_id = station_id
        self.type = type
        self.result = {}

    @Throttle(MIN_TIME_BETWEEN_API_UPDATES)
    def update(self):
        """Update function for updating api information."""
        try:
            if self.station_id == 'avg':
                res = requests.get(API_URL, timeout=10)
                res.raise_for_status()
                response = res.json()
                for oil in response['OIL']:
                    if self.type[0] == oil['PRODCD']:
                        self.result['avg_date'] = oil['TRADE_DT']
                        self.result['avg_price'] = oil['PRICE']
                        self.result['avg_diff'] = oil['DIFF']
                        break
            else:
                tsp = int(datetime.now().timestamp() * 1000)
                req_url = SUB_URL.format(self.station_id, tsp)
                res = requests.get(req_url, timeout=10)
                res.raise_for_status()
                response = res.json()
                
                #{'isMapUser': False, 'isExist': False}
                if not response.get('isExist'):
                    _LOGGER.error('station_id is wrong.')
                    raise
                
                self.result['name'] = response['basicInfo']['placenamefull']
                
                info = response['oilPriceInfo']
                priceList = info['priceList']
                
                self.result['date'] = info['baseDate']
                
                if isinstance(priceList, list):
                    for price in priceList:
                        if self.type[1] == price['type']:
                            self.result['price'] = price['price']
                            break
                elif len(priceList) > 0:
                    if self.type[1] == priceList['type']:
                        self.result['price'] = priceList['price']

        except Exception as ex:
            _LOGGER.error('Failed to update OilPrice API status Error: %s', ex)
            raise


class OilPriceSensor(Entity):
    """Representation of a OilPrice Sensor."""

    def __init__(self, name, station_id, type_info, api):
        """Initialize the OilPrice sensor."""
        self._name = name
        self.oil_type = type_info[1]
        self.price = 0
        self.station_id = station_id
        self.base_date = '-'
        self.diff = '-'
        self.api = api

    @property
    def entity_id(self):
        """Return the entity ID."""
        return 'sensor.oil_price_{}'.format(self.station_id)

    @property
    def name(self):
        """Return the name of the sensor, if any."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return 'mdi:gas-station'

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return '원'

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.price

    @property
    def extra_state_attributes(self):
        """Attributes."""
        data = { 'oil_type': self.oil_type,
                 'base_date': self.base_date }
        if self.diff != '-':
            data['price_diff'] = self.diff
        return data

    @Throttle(MIN_TIME_BETWEEN_SENSOR_UPDATES)
    def update(self):
        """Get the latest state of the sensor."""
        if self.api is None:
            return

        self.api.update()

        result = self.api.result
        
        if 'price' in result:
            self._name = result.get('name')
            self.price = result.get('price').replace(",","").replace("원","")
            self.base_date = result.get('date')
        else:
            self._name = '전국평균'
            self.price = result.get('avg_price')
            self.base_date = result.get('avg_date')
            self.diff = result.get('avg_diff')
        
