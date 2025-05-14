import webbrowser as web
text=input("Enter your search query: ")
web.open("https://www.google.com/search?q=%s" % text)

