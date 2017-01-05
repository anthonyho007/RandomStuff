require 'json'
require 'rest-client'
require 'active_shipping'

origin = ActiveShipping::Location.new(country: 'CA',
									 province: 'QC',
									 city: 'Montreal',
									 zip: 'H3G 2A8')


res = RestClient.get("https://shopicruit.myshopify.com/admin/orders.json?page=1&access_token=c32313df0d0ef512ca64d5b336a0d7c6")
json = JSON.parse(res.body)
total_price = 0.00
before_price = 0.00
for order in json["orders"]
	puts order["email"]
	puts order["shipping_address"]["zip"]
	destination = ActiveShipping::Location.new(country: order["shipping_address"]["country_code"],
											   city: order["shipping_address"]["city"],
											   state: order["shipping_address"]["province_code"],
											   zip: order["shipping_address"]["zip"])
	puts order["total_price"]
	item_weight = 0.00
	for item in order["line_items"]
		item_weight += item["grams"]
	end
	packages = [ActiveShipping::Package.new(item_weight, [2, 3, 4])]
	canadapost = ActiveShipping::CanadaPost.new( login: 'CPC_DEMO_XML')
	rates_shipping = canadapost.find_rates(origin, destination, packages)
	rates = rates_shipping.rates.sort_by(&:price).collect {|rate| [rate.service_name, rate.price]}
	puts rates[0][1]/100
	puts "\n"
	before_price += order["total_price"].to_f
	total_price += order["total_price"].to_f + rates[0][1]/100
end
puts before_price
puts "total price is #{total_price*1.15}" 