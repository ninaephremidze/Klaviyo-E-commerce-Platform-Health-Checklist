# imports
import requests
import math
import time
import csv
import sys
import os

## CONFIG
private = sys.argv[2]
name = sys.argv[1]
filename = 'demo_checks_'+name+'.csv'
##########################

def get_metrics():

    global private

    initial_call = 'https://a.klaviyo.com/api/v1/metrics?api_key={private}&page=0&count=1'.format(private=private)

    response = requests.get(initial_call)

    content = response.json()

    total = content['total']

    pages = math.ceil(total/100)

    metric_dict = dict()

    for page in range(pages):

        call = 'https://a.klaviyo.com/api/v1/metrics?api_key={private}&page={page}&count=100'.format(private=private,page=page)

        response = requests.get(call)

        content = response.json()

        for metric in content['data']:

            metric_dict[metric['name']] = metric

    return metric_dict

def get_flows():

    global private

    initial_call = 'https://a.klaviyo.com/api/v1/flows?api_key={private}&count=1'.format(private=private)

    response = requests.get(initial_call)

    content = response.json()

    total = content['total']

    pages = math.ceil(total/100)

    flows_dict = dict()

    for page in range(pages):

        call = 'https://a.klaviyo.com/api/v1/flows?api_key={private}&count=100'.format(private=private)

        response = requests.get(call)

        content = response.json()

        for flow in content['data']:

            flows_dict[flow['id']] = flow

    return flows_dict

def get_campaigns():

    global private

    initial_campaign_call = 'https://a.klaviyo.com/api/v1/campaigns?api_key={private}&count={count}&page={page}'.format(private=private,count=1,page=0)

    response = requests.get(initial_campaign_call)

    content = response.json()

    total = content['total']

    pages = math.ceil(total/100)

    campaign_dict = dict()

    for page in range(pages):

        current_campaign_call = 'https://a.klaviyo.com/api/v1/campaigns?api_key={private}&count={count}&page={page}'.format(private=private,count=100,page=page)

        response = requests.get(current_campaign_call)

        content = response.json()

        for data_point in content['data']:

            campaign_dict[data_point['id']]=data_point

    return campaign_dict


def attributed_revenue_percentage():

    global private
    global metric_dict

    metric_id = metric_dict['Placed Order']['id']

    # calculate total revenue

    all_revenue_call = 'https://a.klaviyo.com/api/v1/metric/{metric_id}/export?api_key={private}&unit={unit}&measurement={measurement}'.format(metric_id=metric_id,private=private,unit='month',measurement='value')

    response = requests.get(all_revenue_call)

    content = response.json()

    total_revenue = 0

    for data_point in content['results'][0]['data']:

        total_revenue += data_point['values'][0]

    # calculate attributed revenue

    att_revenue_call = 'https://a.klaviyo.com/api/v1/metric/{metric_id}/export?api_key={private}&unit={unit}&measurement={measurement}&by={by}'.format(metric_id=metric_id,private=private,unit='month',measurement='value',by='$attributed_message')
    
    response = requests.get(att_revenue_call)

    content = response.json()

    att_revenue = 0

    for result in content['results']:

        for data_point in result['data']:

            att_revenue += data_point['values'][0]

    return att_revenue/total_revenue


def last_attributed_revenue_campaigns():

    global private
    global metric_dict
    global campaign_dict

    metric_id = metric_dict['Placed Order']['id']

    export_call = 'https://a.klaviyo.com/api/v1/metric/{metric_id}/export?api_key={private}&unit={unit}&measurement={measurement}&by={by}'.format(metric_id=metric_id,private=private,unit='day',measurement='value',by='$attributed_message')

    response = requests.get(export_call)

    content = response.json()

    last_time = None

    for result in content['results']:

        if result['segment'][-7:-1] in campaign_dict.keys():

            for data_point in result['data']:

                if data_point['values'][0]>0:

                    if last_time is None:

                        last_time = data_point['date']

                    else:

                        if last_time < data_point['date']:

                            last_time = data_point['date']

    return last_time

def last_attributed_revenue_flows():

    global private
    global metric_dict
    global campaign_dict

    metric_id = metric_dict['Placed Order']['id']

    export_call = 'https://a.klaviyo.com/api/v1/metric/{metric_id}/export?api_key={private}&unit={unit}&measurement={measurement}&by={by}'.format(metric_id=metric_id,private=private,unit='day',measurement='value',by='$attributed_message')

    response = requests.get(export_call)

    content = response.json()

    last_time = None

    for result in content['results']:

        if result['segment'][-7:-1] not in campaign_dict.keys():

            for data_point in result['data']:

                if data_point['values'][0]>0:

                    if last_time is None:

                        last_time = data_point['date']

                    else:

                        if last_time < data_point['date']:

                            last_time = data_point['date']

    return last_time


def last_attributed_revenue_sms():

    global private
    global metric_dict

    metric_id = metric_dict['Placed Order']['id']

    export_call = 'https://a.klaviyo.com/api/v1/metric/{metric_id}/export?api_key={private}&unit=day&measurement=value&where=[["$flow_channel","=","$sms_channel"]]'.format(metric_id=metric_id, private=private)

    response = requests.get(export_call)

    content = response.json()

    last_time = None

    for data_point in content['results'][0]['data']:

        if data_point['values'][0]>0:

            if last_time is None:

                last_time = data_point['date']

            else:

                if last_time < data_point['date']:

                    last_time = data_point['date']

    return last_time



def last_event(event_name):

    global private
    global metric_dict

    metric_id = metric_dict[event_name]['id']

    call = 'https://a.klaviyo.com/api/v1/metric/{metric_id}/timeline?api_key={private}&count=1'.format(metric_id=metric_id, private=private)

    response = requests.get(call)

    content = response.json()

    last_time = None

    if content['count'] ==1:

        last_time = content['data'][0]['datetime']

    return format_time(last_time)


def last_campaign_event(event_name):

    global private
    global metric_dict
    global campaign_dict

    metric_id = metric_dict[event_name]['id']

    call = 'https://a.klaviyo.com/api/v1/metric/{metric_id}/export?api_key={private}&unit=day&measurement=count&by=$message'.format(metric_id=metric_id, private=private)

    response = requests.get(call)

    content = response.json()

    last_time = None

    for result in content['results']:

        if result['segment'][-7:-1] in campaign_dict.keys():

            for data_point in result['data']:

                if data_point['values'][0]>0:

                    if last_time is None:

                        last_time = data_point['date']

                    else:

                        if last_time < data_point['date']:

                            last_time = data_point['date']

    return last_time



def count_live_flows():

    global flows_dict

    count = 0

    for flow in flows_dict.values():

        if flow['status'] == 'live':

            count += 1

    return count


def count_flow_events(days,metric_name):
    # note: API only goes back max of 30 days/month

    global private
    global metric_dict

    metric_id = metric_dict[metric_name]['id']
    
    call = 'https://a.klaviyo.com/api/v1/metric/{metric_id}/export?api_key={private}&unit=day&measurement=count&by=$flow'.format(metric_id=metric_id, private=private)

    response = requests.get(call)

    content = response.json()

    count = 0

    for result in content['results']:

        data = result['data']

        data.reverse()

        data = data[:days]

        for data_point in data:

            count += data_point['values'][0]

    return count


def count_campaign_events(days,metric_name):
    # note: API only goes back max of 30 days/month

    global private
    global metric_dict
    global campaign_dict

    metric_id = metric_dict[metric_name]['id']
    
    call = 'https://a.klaviyo.com/api/v1/metric/{metric_id}/export?api_key={private}&unit=day&measurement=count&by=$message'.format(metric_id=metric_id, private=private)

    response = requests.get(call)

    content = response.json()

    count = 0

    for result in content['results']:

        if result['segment'][-7:-1] in campaign_dict.keys():

            data = result['data']

            data.reverse()

            data = data[:days]

            for data_point in data:

                count += data_point['values'][0]

    return count

def count_live_flow_events(days, metric_name):

    global private
    global metric_dict
    global flows_dict

    metric_id = metric_dict[metric_name]['id']
    
    call = 'https://a.klaviyo.com/api/v1/metric/{metric_id}/export?api_key={private}&unit=day&measurement=count&by=$flow'.format(metric_id=metric_id, private=private)

    response = requests.get(call)

    content = response.json()

    count = 0

    live_flow_ids = [key for key in flows_dict.keys() if flows_dict[key]['status']=='live']

    for result in content['results']:

        if result['segment'][-7:-1] in live_flow_ids:

            data = result['data']

            data.reverse()

            data = data[:days]

            for data_point in data:

                count += data_point['values'][0]

        return count


def all_live_received(days):

    global private
    global metric_dict
    global flows_dict

    metric_name = 'Received Email'

    metric_id = metric_dict[metric_name]['id']
    
    call = 'https://a.klaviyo.com/api/v1/metric/{metric_id}/export?api_key={private}&unit=day&measurement=count&by=$flow'.format(metric_id=metric_id, private=private)

    response = requests.get(call)

    content = response.json()

    count = 0

    live_flow_ids = [key for key in flows_dict.keys() if flows_dict[key]['status']=='live']

    for result in content['results']:

        if result['segment'][-7:-1] in live_flow_ids:

            data = result['data']

            data.reverse()

            data = data[:days]

            for data_point in data:

                count += data_point['values'][0]

            if count == 0:

                return False

        return True

def campaign_open_rate(days):

    opens = count_campaign_events(days,'Opened Email')
    received = count_campaign_events(days,'Received Email')

    if received == 0:

        return None

    else:

        return opens/received

def campaign_click_rate(days):

    clicks = count_campaign_events(days,'Clicked Email')
    received = count_campaign_events(days,'Received Email')

    if received == 0:

        return None

    else:

        return clicks/received

def flows_open_rate(days):

    opens = count_flow_events(days,'Opened Email')
    received = count_flow_events(days,'Received Email')

    if received == 0:

        return None

    else:

        return opens/received

def flows_click_rate(days):

    clicks = count_flow_events(days,'Clicked Email')
    received = count_flow_events(days,'Received Email')

    if received == 0:

        return None

    else:

        return clicks/received

def no_duplicate_metrics():

    global private
    global metric_dict

    call = 'https://a.klaviyo.com/api/v1/metrics?api_key={private}&page=0&count=1'.format(private=private)

    response = requests.get(call)

    content = response.json()

    total = content['total']

    return not (total != len(metric_dict.keys()))

def format_time(timestring):

    if timestring:

        if '00:00' in timestring:

            timestring = timestring[:10]

    return timestring


### get data ####
print('\n\nPREPARING {name}'.format(name=name))

metric_dict = get_metrics()
campaign_dict = get_campaigns()
flows_dict = get_flows()

print('... loading data ...')

### revenue checks
last_attributed_revenue_campaigns = format_time(last_attributed_revenue_campaigns())
last_attributed_revenue_flows = format_time(last_attributed_revenue_flows())
last_attributed_revenue_sms = format_time(last_attributed_revenue_sms())
attributed_revenue_percentage = attributed_revenue_percentage()

print('... building report ...')

# add revenue print statements here
flows_live_count = count_live_flows()
recipients_in_all_live_flows = all_live_received(1)
recipients_in_flows_last_day = count_live_flow_events(1,'Received Email')
recipients_in_flows_last_week = count_live_flow_events(7,'Received Email')
flows_open_rate_day = flows_open_rate(1)
flows_click_rate_day = flows_click_rate(1)
flows_open_rate_week = flows_open_rate(7)
flows_click_rate_week = flows_click_rate(7)


last_sent_campaign = format_time(last_campaign_event('Received Email'))
recipients_in_campaigns_last_day = count_campaign_events(1,'Received Email')
recipients_in_campaigns_last_week = count_campaign_events(7,'Received Email')
campaigns_open_rate_day = campaign_open_rate(1)
campaigns_click_rate_day = campaign_click_rate(1)
campaigns_open_rate_week = campaign_open_rate(7)
campaigns_click_rate_week = campaign_click_rate(7)


#### build report #########

labels = []
values = []
data = []



## FLOWS

labels = [
    '# LIVE FLOWS',
    'RECEIPIENTS IN ALL LIVE FLOWS',
    '# RECEIPIENTS IN FLOWS PAST DAY',
    '# RECEIPIENTS IN FLOWS PAST WEEK',
    'FLOWS OPEN RATE DAY',
    'FLOWS CLICK RATE DAY',
    'FLOWS OPEN RATE WEEK',
    'FLOWS CLICK RATE WEEK'
    ]

values = [
    flows_live_count,
    recipients_in_all_live_flows,
    recipients_in_flows_last_day,
    recipients_in_flows_last_week,
    flows_open_rate_day,
    flows_click_rate_day,
    flows_open_rate_week,
    flows_click_rate_week
    ]

for i in range(len(labels)):

    data += [[labels[i],str(values[i])]]


## CAMPAIGNS

labels = [
    'LAST SENT CAMPAIGN',
    '# RECEIPIENTS IN CAMPAIGNS PAST DAY',
    '# RECEIPIENTS IN CAMPAIGNS PAST WEEK',
    'CAMPAIGNS OPEN RATE DAY',
    'CAMPAIGNS CLICK RATE DAY',
    'CAMPAIGNS OPEN RATE WEEK',
    'CAMPAIGNS CLICK RATE WEEK'
    ]

values = [
    last_sent_campaign,
    recipients_in_campaigns_last_day,
    recipients_in_campaigns_last_week,
    campaigns_open_rate_day,
    campaigns_click_rate_day,
    campaigns_open_rate_week,
    campaigns_click_rate_week
    ]

for i in range(len(labels)):

    data += [[labels[i],str(values[i])]]

## REVENUE

labels = [
    'LAST DATE CAMPAIGNS HAD ATTRIBUTED REVENUE',
    'LAST DATE FLOWS HAD ATTRIBUTED REVENUE',
    'LAST DATE SMS HAD ATTRIBUTED REVENUE',
    'ATTRIBUTED REVENUE PERCENTAGE'
    ]

values = [
    last_attributed_revenue_campaigns,
    last_attributed_revenue_flows,
    last_attributed_revenue_sms,
    attributed_revenue_percentage
    ]

for i in range(len(labels)):

    data += [[labels[i],str(values[i])]]

# METRICS

labels = []
values = []

labels += [
    'NO DUPLICATE METRICS',
]

values += [
    no_duplicate_metrics(),
]

for metric in metric_dict.keys():

    # print(metric,':',last_event(metric))
    labels += [metric]
    values += [last_event(metric)]


for i in range(len(labels)):

    data += [[labels[i],str(values[i])]]


## write to file
with open(filename,'w') as csvfile:

    writer = csv.writer(csvfile)

    for row in data:

        writer.writerow(row)



print('Completed Report')

os.system('aws s3 cp {filename} s3://demo-checks/{filename}'.format(filename=filename))
