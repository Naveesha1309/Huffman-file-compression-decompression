from huffmancode import Huffmancode

#Package import

from flask import Flask, render_template, send_file, make_response, url_for, Response, redirect, request 
 
#initialise app        - by creating an instance
app = Flask(__name__)

#decorator for homepage 
@app.route('/' )
def home():
    return render_template('index.html')

#-------------------------------------DRIVER FUNCTION------------------------------------

@app.route('/compress/', methods = ['POST', 'GET'] )
def compress():
    if request.method == 'POST':
        path = request.form.get('uploadfile')        #WORK ON THIS
        finalpath="C:\\Users\\Dell\\Desktop\\huffman test\\sample.txt"
        h = Huffmancode(finalpath)
        compressed_file = h.compression()       
        h.decompress(compressed_file)
        return redirect(url_for('index'))
    else:
        return render_template("index.html")

@app.route('/compressed-file/')
def index():
    return render_template("index.html",content="File compressed succesfully")
    

if __name__ == '__main__':
    app.run(debug = True)



# path = input("Enter the Path of file needed to be compressed:")      #input from the user
# h = Huffmancode(path)              #create object for class
# compressed_file = h.compression()        #invoking compression func which returns compressed file
# h.decompress(compressed_file)


#compress button ka part hai:
# compressed_file = h.compression()       
# h.decompress(compressed_file)
