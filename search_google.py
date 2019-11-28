import google 
# import wikipedia


def search_google(text):
	try: 
	    from googlesearch import search 
	except ImportError:  
	    print("No module named 'google' found") 
	  
	# to search 
	query =(text)
	message = "This is what I found on google:"
	for j in search(query, tld="co.in", num=10, stop=1, pause=2): 
	    return j
		
# def search_wikipedia(text):
# 	summary = wikipedia.summary(text)
# 	return summary