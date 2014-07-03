import requests
from api_key import api_key
# Events - Urlname meetup
# https://api.meetup.com/2/events?&sign=true&status=past&group_urlname=Appsterdam&page=200
# RSVP - event id
# https://api.meetup.com/2/rsvps?&sign=true&event_id=24723711&page=200

### CONFIG ###
urlname = "Appsterdam"
page = "200"
time = "-6m,-1d"
status = "past"
rsvp_page = "100"
percentage = 0.6
### /CONFIG/ ###

past_events = requests.get("https://api.meetup.com/2/events?&sign=true&status="+status+"&group_urlname="+urlname+"&time="+time+"&page="+page+"&key="+api_key)

events_id = list()

for events in past_events.json()['results']:
	events_id.append(events['id'].encode('utf-8'))

print events_id
number_events = len(events_id)

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
		#print members['Craig'][1]

		if members[name][1] == 'yes':
			members[name][2]['responses'].append(members[name][1])


'''
Number of events from past 6 months, time = -6m,-1w
Get event rsvps from all events.
Number of YES add for each member.
If N yes >= percentage number, over all meetups.
There is a chance that that person will attend another meetup from that group.
Easy :)'''

#something is not allright...

certainty = percentage * float(number_events)
for member in members:
	n = len(members[member][2]['responses'])

	if n >= certainty:
		print member + " likelyhood, more than = " + str(certainty) + " '%' meetups this person has gone to in the past " + time
		member_percentage = int(float(number_events)) / int(float(n))
		print member + " number events " + str(number_events) + " / number of yes " + str(n) + " ==> percentage = " + str(float(member_percentage))