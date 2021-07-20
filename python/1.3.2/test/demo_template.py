import re
import airspeed
import json

user_data_json = '''{
	"name": "apple",
	"unitPrice": "1",
	"packagingSpecifications": [200, 400, 700],
	"regexValidator": {
		"name": "[a-zA-Z]+",
		"supplier": "[a-zA-Z0-9]+"
	}
}
'''

layout_text = '''
#set ($numPrice = $util.to_number(${unitPrice}))
		{
			"start_x" : 0, "start_y" : 0, "end_x" : 295, "end_y" : 79,
			"origin_font_type" : 0,"font_type" : "Zfull-GB 20", "font_size" : 16,
			"content_type" : "CONTENT_TYPE_TEXT", "content_alignment" : "LEFT",
			"content_reverse" : "TRUE", "number_script" : "SUPER", "number_gap" : "CONSECUTIVE",
			"font_type_script" : "Zfull-GB 24","font_size_script" : 25,
			"content_title" : "spec", "content_value" : u"OFF",
#if ($numPrice > 100)
			"content_color" : 'BLACK'
#else
			"content_color" : 'RED'
#end
		},
#if ($unitPrice < 100)
	{
			"start_x" : 0, "start_y" : 80, "end_x" : 295, "end_y" : 127,
			"origin_font_type" : 0,"font_type" : "Zfull-GB 20", "font_size" : 16,
			"content_type" : "CONTENT_TYPE_TEXT", "content_alignment" : "LEFT",
			"content_reverse" : "FALSE", "number_script" : "SUPER", "number_gap" : "CONSECUTIVE",
			"font_type_script" : "Zfull-GB 24","font_size_script" : 25,
			"content_title" : "Price", "content_value" : u"OFF",
			"content_color" : 'RED'
		},
#end
'''

template_text = '''
the name is ${name}.

#if ($unitPrice >= 1000)
ZONE-1: unit price is more than 1000.
#else
ZONE-2: unit price is less than 1000.
#end

#set ($num = 1)
#foreach ($spec in $packagingSpecifications)
packaging specification $num - $spec
#set ($num = $num + 1)
#end
'''

class Util:
	def to_number(self, txt):
		return int(txt)


user_data = json.loads(user_data_json)
user_data["util"] = Util()
template = airspeed.Template(layout_text)
print template.merge(user_data)
