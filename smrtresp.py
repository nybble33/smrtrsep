#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import xml.etree.ElementTree as ET

ACTION = 'action'
DOMAIN_URL = 'http://api.smartresponder.ru/'
SUBSCRIBERS_URL = 'subscribers.html'
DELIVERIES_URL ='deliveries.html'

def send_post(url, data):
    headers = {"User-Agent": "Mozilla/5.0 (X11; U; Linux i686; ru; \
                    rv:1.9.2.6) Gecko/20100628 Ubuntu/10.04 (lucid) \
                    Firefox/3.6.6",
                   "Accept": "text/html,application/xhtml+xml,application\
                   /xml;q=0.9,*/*;q=0.8"}
    params = urllib.urlencode(data)
    #print 'Reading - ' + url
    return urllib2.urlopen(urllib2.Request(url, params, headers)).read()

class SR_response ():
    def __init__(self, XML_str):
        self.root = ET.fromstring(XML_str)

    @property
    def success(self):
        if self.root.find('result').text == '1':
            return True
        else:
            return False

    @property
    def count(self):
        return self.root.find('list').attrib['count']

    @property
    def elements(self):
        _el = []
        for elem in self.root.iter('element'):
            _items = {}
            for item in list(elem):
                _items[item.tag] = item.text
            #print _items
            _el.append(_items)
        return _el


class Subscriber():
    def __init__(self, email, **kwargs):
        self.email = email
        self._attrs = kwargs
        self._attrs['email'] = email
        for key in kwargs:
            setattr(self, key, kwargs[key])

    #@property
    #def exist_active(self):
    def __str__(self):
        return self.email

    @property
    def __fields__(self):
        return [arg for arg in dir(self) if not arg.startswith('_') and not callable(getattr(self, arg))]


class SmartResponder():
    def __init__(self, id):
        self.id = id

    @property
    def deliveries(self):
        post_request = {'action': 'list'}
        response = SR_response(self._send_request(DELIVERIES_URL, post_request))
        #print self._send_request(DELIVERIES_URL, post_request)
        return response.elements

    def _send_request(self, url, post_data):
        post_data['api_key'] = self.id
        return send_post(DOMAIN_URL+url, post_data)


    def _subscriber_exist(self, subscriber):
        post_request = {
            ACTION: 'list',
            'search[email]': subscriber.email
        }
        #~print self._send_request(SUBSCRIBERS_URL, post_request)
        self.response = SR_response(self._send_request(SUBSCRIBERS_URL, post_request))
        if self.response.count == '0':
            return  False
        else:
            return True

    def subscriber_email_exist(self, email):
        _sub = Subscriber(email)
        return self._subscriber_exist(_sub)

    def add_subscriber(self, _subscriber, _delivery):
        post_request = _subscriber._attrs
        post_request['action']='create'
        if not self._subscriber_exist(_subscriber):
            post_request['delivery_id'] = _delivery
            #print self.response
            #post_request['action'] = 'link_with_delivery'
            #print SR_response(self._send_request(SUBSCRIBERS_URL, post_request))
        else:
            post_request['action'] = 'link_with_delivery'
        #print post_request
        self.response = SR_response(self._send_request(SUBSCRIBERS_URL, post_request))
        return self.response


def add_subscriber(smart_resp, subscriber):
    pass


def subscriber_exist(email):
    post_request = {
        'api_key': foo.id,
        ACTION: 'list',
        'search[email]': email
    }
    print send_post(DOMAIN_URL+SUBSCRIBERS_URL, post_request)



if __name__ == '__main__':
    foo = SmartResponder('TPGls02fuK5vA0cKvCv1XxLpGY09KrYd')
    #sub = Subscriber('admin@nybble.net', group_id='39412')
    #foo.add_subscriber(sub, '575148')
    sub = Subscriber('admin@nybble.net')
    if foo._subscriber_exist(sub):
        print 'Exist'
    else:
        print 'Not Exist'
        print foo.add_subscriber(sub, '575148')
    '''
    print foo.id
    post_data = {
        'api_key': foo.id,
        'action': 'list',
        'fields': 'id,info'
    }
    #bar = send_post('http://api.smartresponder.ru/deliveries.html', post_data)
    #print bar
    '''
    '''
    root = ET.fromstring(bar)
    for child in root:
        print child.tag, child.attrib
    '''
    '''
    #for elem in root.iter('element'):
    #    for item in list(elem):
    #        print item.tag + '=' + item.text
    #print foo.deliveries
    for _del in foo.deliveries:
        print _del['id'], ' - ', _del['info']
    #print foo
    _sub = foo._subscriber_exist(sub)
    print sub._attrs
    '''