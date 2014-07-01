import requests
import api_key
# Events - Urlname meetup
# https://api.meetup.com/2/events?&sign=true&status=past&group_urlname=Appsterdam&page=200
# RSVP - event id
# https://api.meetup.com/2/rsvps?&sign=true&event_id=24723711&page=200


urlname = "Appsterdam"
page = "2"
status = "past"
rsvp_page = "100"

past_events = requests.get("https://api.meetup.com/2/events?&sign=true&status="+status+"&group_urlname="+urlname+"&page="+page+"&key="+api_key)


print past_events.status_code
#print past_events.json()['results'][0]['id']
events_id = list()

for events in past_events.json()['results']:
	events_id.append(events['id'].encode('utf-8'))

print events_id
members = dict()
events_dict = dict()

for event in events_id:
	rsvp_event = requests.get("https://api.meetup.com/2/rsvps?&sign=true&event_id="+event+"&page="+rsvp_page+"&key="+api_key)
	print rsvp_event.status_code

	for member in rsvp_event.json()['results']:
		
		name = member['member']['name'].encode('utf-8')
		member_id = member['member']['member_id']
		response = member['response'].encode('utf-8')
		#print response
		members[name] = [member_id, response, {"responses" : []}]

	for name in members:
		#answer_response = members[name][1]['responses']
		#print response
		#print members[name][1]

		if members[name][1] == 'yes':
			members[name][2]['responses'].append(members[name][1])

print members

#print members['Craig']
	#print members[name][2]
		#print members['Craig'][1]
#print members['Craig'] #2 yes