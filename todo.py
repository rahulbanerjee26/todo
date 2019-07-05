import http.server
from urllib.parse import parse_qs

#store all the todos
todos = {}

#no. of todos
count = 0

#html code for the form
form = '''<!DOCTYPE html>
<title>Bookmark Server</title>
<form method="POST">
    <label>Todo:
        <input name=todo>
    </label>
    <br>
    <button type="submit">Save it!</button>
</form>
<p>Todo list:
<pre>
{}
</pre>
'''


class handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        #status code
        self.send_response(200)
        global count

        #response body
        if(count == 0):
            
            #headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            #content
            known = "".join("No Todos")
            self.wfile.write(form.format(known).encode())
        
        else:
            
            #headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            #content
            known = "\n".join("{}) {}".format(key, todos[key])
                              for key in sorted(todos.keys()))
            self.wfile.write(form.format(known).encode())

    
    def do_POST(self):
        length = int(self.headers.get('content-length',0))
        body = self.rfile.read(length).decode()
        params = parse_qs(body)

        if "todo" not in params:

            #status code 400 for blank textfield error
            self.send_response(400)

            #header
            self.send_header('Content-type','text/plain; charset=utf-8')
            self.end_headers()

            #response body
            self.wfile.write("Textfield was blank. Please enter a value".encode())
            return
        else:
            item = params["todo"][0]
            global count
            count += 1
            todos[count] = item
            
            #status code 303 to redirect
            self.send_response(303)

            #header to redirect
            self.send_header('Location','/')
            self.end_headers()


if __name__ == '__main__':
    addr = ('',8000)
    httpd = http.server.HTTPServer(addr,handler)
    httpd.serve_forever()
    



