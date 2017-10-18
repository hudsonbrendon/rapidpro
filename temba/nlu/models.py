# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
import json


NLU_API_NAME = 'NLU_API_NAME'
NLU_API_KEY = 'NLU_API_KEY'

NLU_BOTHUB_TAG = 'BTH'
NLU_WIT_AI_TAG = 'WIT'

NLU_API_CHOICES = (
    (NLU_BOTHUB_TAG, 'BotHub'),
    (NLU_WIT_AI_TAG, 'Wit.AI'),)

NLU_API_WITHOUT_KEY = [NLU_WIT_AI_TAG]


class BaseConsumer(object):
    """
    Base consumer
    This is the base for any nlu api consumers.
    """
    def __init__(self, auth, nlu_type):
        self.auth = auth
        self.name = "%s Consumer" % dict(NLU_API_CHOICES).get(nlu_type)

    def __str__(self):
        return self.name

    def list_bots(self):
        pass

    def predict(self, msg, bot):
        pass

    def get_headers(self):
        return {
            'Authorization': 'Bearer %s' % self.auth
        }

    def _request(self, base_url, data=None, headers=None, method='GET'):
        try:
            if method == 'POST':
                return requests.post(base_url, data=data, headers=headers)
            else:
                return requests.get(base_url, params=data, headers=headers)
        except:
            pass


class BothubConsumer(BaseConsumer):
    """
    Bothub consumer
    This consumer will call Bothub api.
    """
    BASE_URL = 'http://api.bothub.it/'

    def predict(self, msg, bot):
        predict_url = self.BASE_URL + 'bots'
        data = {
            'uuid': bot,
            'msg': msg
        }
        response = self._request(predict_url, data=data, headers=self.get_headers())
        predict = json.loads(response.content)
        intent = predict.get('answer', None).get('intent', None)

        return intent.get('name', None), intent.get('confidence', None)

    def list_bots(self):
        list_bots_url = self.BASE_URL + 'auth'
        response = self._request(list_bots_url, headers=self.get_headers())
        tuple_bots = tuple(json.loads(response.content))
        list_bots = list()
        for bot in tuple_bots:
            list_bots.append((bot.get('uuid'), bot.get('slug')))

        return tuple(list_bots)


class WitConsumer(BaseConsumer):
    """
    Wit AI consumer
    This consumer will call Wit Ai api.
    """
    BASE_URL = 'https://api.wit.ai/'

    def predict(self, msg, bot):
        predict_url = self.BASE_URL + 'message'
        data = {
            'q': msg,
            'n': 1
        }
        response = self._request(predict_url, data=data, headers=self.get_headers())
        predict = json.loads(response.content)
        entities = predict.get('entities', None)
        if entities:
            intents = entities.get('intent', None)
            if intents:
                return intents[0].get('value'), intents[0].get('confidence')


class NluApiConsumer(object):
    """
    Nlu API consumer
    This consumer will check which api will be called.
    """
    @staticmethod
    def factory(nlu_type, auth):
        if nlu_type == NLU_BOTHUB_TAG:
            return BothubConsumer(auth, nlu_type)
        if nlu_type == NLU_WIT_AI_TAG:
            return WitConsumer(auth, nlu_type)