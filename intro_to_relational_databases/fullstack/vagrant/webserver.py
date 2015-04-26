from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from setup_database import Base, Restaurants, MenuItem
import cgi


#connect to db
engine = create_engine("postgresql://vagrant:glue@localhost/restaurant_db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                content = ''
                content += '<html><body><h1>Restaurant List</h1>'
                content += "<a href='restaurants/new'>Add a new restaurant</a><br>"
                rests = session.query(Restaurants).all()
                for rest in rests:
                    content += '<h2>%s</h2>' % (rest.name)
                    content += "<a href='restaurants/%s/edit'>Edit</a><br>" % (rest.id)
                    content += "<a href='restaurants/%s/delete'>Delete</a><br>" % (rest.id)
                    
                content += '</body></html>'
                
                self.wfile.write(content)
                return
            if self.path.endswith("/new"):
                self.send_response(200)
                self.end_headers()
       
                content = ''
                content += '<html><body>'
                content += '<h2>Register a new restaurant</h2>' 
                content += "<form method='POST' enctype='multipart/form-data' action='/new'><h2>What is the new restaurant's name?</h2><input name='rest_name' type='text'><input type='submit' value='Submit'></form>"

                self.wfile.write(content)
                return
            
            if self.path.endswith("/edit"):
                self.send_response(200)
                self.end_headers()

                id_num = self.path.split("/")[2]
                rest = session.query(Restaurants).filter_by(id=id_num).one()
                content = ''
                content += '<html><body>'
                content += '<h1>Name: %s</h2>' % (rest.name)
                content += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % rest.id
                content += "<input name='edit_name' type='text'>"
                content += "<input type='submit' value='Submit'></form>"
                content += "</body></html>"
                self.wfile.write(content)
                return
                
            if self.path.endswith("/delete"):
                
                self.send_response(200)
                self.end_headers()

                id_num = self.path.split("/")[2]
                rest = session.query(Restaurants).filter_by(id=id_num).one()
                content = ''
                content += '<html><body>'
                content += '<h1>Name: %s</h2>' % (rest.name)
                content += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % (rest.id)
                content += "<h2>Are you sure you want to delete it?</h2>"
                content += "<input type='submit' value='Yes!'></form>"
                content += "</body></html>"
                self.wfile.write(content)
                return
                
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    newcontent = fields.get('edit_name')[0]
                    id_num = self.path.split("/")[2]
                    rest = session.query(Restaurants).filter_by(id=id_num).one()
                    rest.name = newcontent
                    session.add(rest)
                    session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return
                
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    id_num = self.path.split("/")[2]
                    rest = session.query(Restaurants).filter_by(id=id_num).one()
                    session.delete(rest)
                    session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return
            
            if self.path.endswith("/new"):

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    newcontent = fields.get('rest_name')
                    session.add(Restaurants(name=newcontent[0]))
                    session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                
                return
                
        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

def main():
    try:
        hostname = ''
        port = 8080
        server = HTTPServer((hostname, port), webServerHandler)
        print "Web server running on port: %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C KeyboardInterrupt, closing server..."
        server.socket.close()

if __name__ == '__main__':
    main()
