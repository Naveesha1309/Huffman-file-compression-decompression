
path = input("Enter the Path of file needed to be compressed:")      #input from the user
h = Huffmancode(path)              #create object for class
compressed_file = h.compression()        #invoking compression func which returns compressed file
h.decompress(compressed_file)
