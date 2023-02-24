from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = "localhost"
serverPort = 8080


def parse_FormData(query):
    splitted = query.split('&')
    ret = {}
    for pair in splitted:
        kvp = pair.split('=')
        ret[kvp[0]] = kvp[1]
    return ret

users = [
    {
        "username": "admin",
        "password": "adminpass"
    },
    {
        "username": "Jkral626",
        "password": "Lucy070406" #encrypted: a=fasdfasf
    }
]

def get_AllUsers():
    ret = []
    for user in users:
        ret.append(user["username"])
    return ','.join(ret) #admin,Jkral626

def authentication(userObj):
    for user in users:
        if user["username"] == userObj["username"] and user["password"] == userObj["password"]:
            return True
    return False

def register_NewUser():
    ret = []
    for user in users:
        if user["newpassword"] == user["passwordretype"]:
            ret.append(user["newusername"], user["newpassword"])
    return ','.join(ret)



routes = {
    "static": {
        "/": open("index.html").read(),
        "/about": "Project Website Network & Security",
        "/greeting": "'Ello, 'ello, hola! Ciao and Bonjour!",
        "/login": open("login.html").read(),
        "/register": open("register.html").read(),
        
    },
    "api": { 
    "/api/getAllUsers": get_AllUsers()    
    }
}

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in routes["static"]:
            self.http_header(200, "text/html")
            self.wfile.write(bytes(routes["static"][self.path], "utf-8"))
        elif self.path.startswith("/api"): #http://localhost:8080/api/getallusers
            self.http_header(200, "application/json")
            self.wfile.write(bytes("{\"result\": \"OK\", \"content\": %s}" % routes["api"][self.path], "utf-8"))
        else:
            self.http_header(404, "text/html")
            self.write(bytes("Page not found!", "utf-8"))
        return
    
    def do_POST(self):
        print("Hit by a post request")
        self.http_header(200, "text/html")
        
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length) 
        userData = parse_FormData(post_data.decode("UTF-8"))
        if authentication(userData):
            self.wfile.write(bytes("Welcome, " + userData["username"], "UTD-8"))
        else:
            self.wfile.write(bytes("Username and password do not match.", "UTF-8"))
        self.wfile.write(bytes("<a href=\"/login\">login</a>", "UTF-8"))
        return
        self.wfile.write(bytes("<a href=\"/register\">register</a>", "UTF-8"))
    def http_header(self, statuscode, contenttype):
        self.send_response(statuscode)
        self.send_header("Content-type", contenttype)
        self.end_headers()
    


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt: #CTRL + C
        pass

    webServer.server_close()
    print("Server has stopped.")