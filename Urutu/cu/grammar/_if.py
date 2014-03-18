
def __init__(words, kernel):
	string = "if( "
	for word in words[1:-1]:
		string = string + str(word)
	return string + " )"

