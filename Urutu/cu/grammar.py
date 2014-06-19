def keyword(words, kernel):
	if words[0] == "if":
		return _if(words, kernel)

def _if(words, kernel):
	string = "if( "
	for word in words[1:-1]:
		string = string + str(word)
	return string + " )"

