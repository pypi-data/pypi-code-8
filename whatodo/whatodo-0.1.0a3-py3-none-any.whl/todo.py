import re

class TODO(object):
	# create todo class
	"""
	docstring for TODO
	"""

	def __init__(self, comment, filename, line_number, keywords):
		#print("'" + comment + "'")

		# define variables
		self.filename = filename
		self.line_number = line_number
		self.tags = []

		comment_lines = comment.splitlines()

		# cut the keyword from the title
		self.title = comment_lines[0]
		found_keyword = False
		for keyword in keywords:
			index = self.title.find(keyword)
			if index != -1:
				found_keyword = True
				length_of_keyword = len(keyword)
				cut_off = index + length_of_keyword
				self.title = self.title[cut_off:]
				self.title = self.title.strip()
			
		if not found_keyword:
			raise Exception("No keyword in comment")

		# search through body if for tags 
		# and strip beginning spaces and unwanted characters
		if len(comment_lines) > 1 :
			
			for index,line in enumerate(comment_lines[1:], 1):
				line = line.lstrip()
				line = line.lstrip("*")
				line = line.lstrip("//")
				line = line.lstrip("`")
				line = line.lstrip()
				comment_lines[index] = line

			self.body = "\n".join(comment_lines[1:]).rstrip()

			# find and extract tags
			self.tags = re.findall(r'#\w*', self.body)
			#print(self.tags)

		else:
			self.body = ""


	def __repr__(self):

		# print set up
		ret = ""
		ret += "TODO\n"

		ret += "Title: " + str(self.title) + "\n"
		ret += "Body:  " + str(self.body) + "\n"
		ret += "File:  " + str(self.filename) + ":" + str(self.line_number) + "\n"

		if len(self.tags) > 0:
			ret += "Tags: "
		for tag in self.tags:
			ret += str(tag) + ", "

		return ret

	def __dict__(self):
		ret = {}
		ret["filename"] = self.filename
		ret["line_number"] = self.line_number
		ret["title"] = self.title
		ret["body"] = self.body
		ret["tags"] = self.tags

		return ret

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)



if __name__ == '__main__':
	comment = """		TODO This is a todo
		This is a body #HASHTAGGALORE 
		#TWITTERSUCKS 
	"""
	test = TODO(comment, "file.py", 9999, ["TODO"])

	print(test)


		