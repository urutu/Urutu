import _if

def __init__(words, kernel):
	if words[0] == "if":
		return _if.__init__(words, kernel)
