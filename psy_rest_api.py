
def read_url(url):
    # Read URL
    import urllib2
	if len(url)=0:
        url = 'https://developer.yahoo.com/'
    
    e_code = [] # error code
    try:
    	f_obj = urllib2.urlopen(url) #f_obj is a file-like object
    	data = f_obj.read()
    	# concise code of the 2 lines above: data = urllib2.urlopen(url).read()
    except urllib2.HTTPError, e:
    	print "HTTP error: %d" % e.code
    	e_code = [HTTP, e.code]
    except urllib2.URLError, e:
    	print "Network error: %s" % e.reason.args[1]
    	e_code = [Network, e.reason.args[1]]
    if e_code==[]:
	    return [0, data]
	else
	    return [1, e_code, e]

def post_url(url, app_id, context, query):
	import urllib2
	# validate inputs
    if len(url)==0:
	    url = 'http://search.yahooapis.com/ContentAnalysisService/V1/termExtraction'
    if len(appid)==0:
        appid = 'YahooDemo'
    if len(context)==0:
        context = '''
        Italian sculptors and painters of the renaissance favored
        the Virgin Mary for inspiration
        '''
    query = 'madonna'
    # set parameters
    params = urllib.urlencode({
    	'appid': appid,
    	'context': context,
    	'query': query
    })
    #  use POST reqeust to get data
    e_code = [] # error code
    try:
        data = urllib.urlopen(url, params).read()
	except urllib2.URLError, e:
	    e_code = e
    if e_code==[]:
	    return [0, data]
	else
	    return [1, e_code]

def auth_url(url, login_url, username, pw):
    import urllib2
    # Example input values:
    # url = 'https://api.del.icio.us/v1/posts/recent'
	# login_url = 'https://api.del.icio.us/'
    # username = 'Your del.icio.us username'
    # pw = 'Your del.icio.us password'
	
    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(
    	None, login_url , username, pw
    )
    auth_handler = urllib2.HTTPBasicAuthHandler(password_manager)
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)
    xml = urllib2.urlopen(url).read()	
		