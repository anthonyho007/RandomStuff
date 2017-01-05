#!/usr/local/bin/python
import sys
import os
import json, urllib
import easypost
import requests

easypost.api_key = '2iGCUaPFzVzxGigMyGx7Zg'
from_address = easypost.Address.create(
	verify=["delivery"],
	name = "Anthony",
	street1 = "118 2nd Street",
	city = "San Francisco",
	state = "CA",
	zip = "94105",
	country = "US",
	)

class fetchData:
	def __init__(self):
		result = urllib.urlopen("https://shopicruit.myshopify.com/admin/orders.json?page=1&access_token=c32313df0d0ef512ca64d5b336a0d7c6").read()
		jdata = json.loads(result)
		total_revenue = 0.00
		for order in jdata["orders"]:
			to_address = easypost.Address.create(
				verify=["delivery"],
				name = order['shipping_address']['first_name'],
				street1 = order['shipping_address']['address1'],
				city = order['shipping_address']['city'],
				state = order['shipping_address']['province_code'],
				zip = order['shipping_address']['zip'],
				country = order['shipping_address']['country_code'],
				)
			item_weight = 0.00
			for item in order['line_items']:
				item_weight += item['quantity'] * item['grams']	
			try:
				parcel = easypost.Parcel.create(
					length = 5,
					width = 5,
					height = 4.3,
					weight = item_weight
				)
			except easypost.Error as e:
				raise e
			#fake customer info 
			customs_item = easypost.CustomsItem.create(
				description = "EasyPost t-shirts",
				hs_tariff_number = 123456,
				origin_country = "US",
				quantity = 2,
				value = 96.27,
				weight = 21.1
				)
			customs_info = easypost.CustomsInfo.create(
				customs_certify = 1,
				customs_signer = "Hector Hammerfall",
				contents_type = "gift",
				contents_explanation = "",
				eel_pfc = "NOEEI 30.37(a)",
				non_delivery_option = "return",
				restriction_type = "none",
				restriction_comments = "",
				customs_items = [customs_item]
			)

			shipment = easypost.Shipment.create(
				to_address = to_address,
				from_address = from_address,
				parcel = parcel,
				customs_info = customs_info
			)
			shipping = 0.00
			if shipment.rates != [] :
				rate = shipment.rates[0]
				data = rate['rate']
				print data
				shipping = float(data)
			order_total = float(order['total_price']) + shipping
			total_revenue += order_total * 1.15
		print total_revenue

if __name__ == "__main__":
	fetchData()



