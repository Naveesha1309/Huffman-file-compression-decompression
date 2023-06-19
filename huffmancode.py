#In Python, any written function can be called by another function.


#using a pre-defined python function for creation of heap.
#[Heap data structure is mainly used to represent a priority queue. In Python, it is available using the “heapq” module.
# The property of this data structure in Python is that each time the smallest heap element is popped(min-heap)]
import heapq
import os


   
#class for creating Binary tree.
class BinaryTree:

    #node in BT
    def __init__(self,value,frequ):       
        self.value = value
        self.frequ = frequ
        self.left = None        #left sub-tree
        self.right = None       #right sub-tree
    
    
         
    #'less than' function, used in creation of min heap.  
    def __lt__(self, other):       #other is the arguement for the comparision
        return self.frequ < other.frequ
    
    
    
     #'equal to' function, used in creation of min heap.  
    def __eq__(self, other):     #other is the arguement for the comparision
        return self.frequ == other.frequ
        
    
    
    
class Huffmancode:
    
    #accessing file using init function.
    def __init__(self,path):
        self.path=path
        self.__heap = []   #creating an iterable(list) to push the values into the heap. Basically an iterable can be converted into a heap. Result can be displayed in list format.
        self.__code = {}   #creating a dictionary to store the code corresponding to the character. Key = character , value = code
        self.__reversecode = {}      #creating a dictionary to map the code to its corresponding character. Key = code , value = character
        

    #frequency dictionary table from the input text file.
    #iterate through each character
    def __frequencydict_from_text(self, text):    
    
        frequ_dict = {}           
        for char in text:                   
            if char not in frequ_dict:
                frequ_dict[char] = 0      
            
            frequ_dict[char]+= 1     
        return frequ_dict            
    

    
    #Implementing heap function
    #insertion of (alphabet,freq) pair as a node in heap iterable/list
    def __Build_heap(self,frequency_dict):
        for key in frequency_dict:
            frequency = frequency_dict[key]      
            binary_tree_node = BinaryTree(key,frequency)   
            heapq.heappush(self.__heap, binary_tree_node)     
    
    

    # Minimum of 2 nodes must be present in heap to merge as a new node(parent)
    def __Build_Binary_Tree(self):
        
        while len(self.__heap) > 1:
            binary_tree_node_1 = heapq.heappop(self.__heap)     
            binary_tree_node_2 = heapq.heappop(self.__heap)
            sum_of_freq = binary_tree_node_1.frequ + binary_tree_node_2.frequ      #sum of child node's freq is the parent node's freq.
            
            #push new node with empty character, and sum as frequency.
            newnode = BinaryTree(None,sum_of_freq)   
            newnode.left = binary_tree_node_1
            newnode.right = binary_tree_node_2
            heapq.heappush(self.__heap,newnode)
        return     

    
    #Encoding: Generating code of characters.
    def __Build_Tree_Code_Helper(self,root,curr_bits):
        if root is None:
            return
        if root.value is not None:       #root.value checks if node has character(if yes, leaf node reached)
            self.__code[root.value] = curr_bits       #storing code in dictionary
            self.__reversecode[curr_bits] = root.value
            return
        
        #apply recursion
        #move to left or right until we reach the character node
        self.__Build_Tree_Code_Helper(root.left,curr_bits+'0')        #using string to store the binary code
        self.__Build_Tree_Code_Helper(root.right,curr_bits+'1')
    
    
    
    
    
    def __Build_Tree_Code(self): 
        
        root = heapq.heappop(self.__heap)         #we require the start node, that is the root node of the heap. Since there is only 1 element present in the heap, it's popped out, to get the root in hand.
        self.__Build_Tree_Code_Helper(root,'')
    
    
    
    
    #iterating each character in text and assigning its encoded value from the __code dictionary in the 'encoded_text' string.
    def __Build_Encoded_Text(self,text):
        encoded_text = ''
        for char in text:             
            encoded_text += self.__code[char]
        return encoded_text  
    
    
    

    #Padding of encoded text function - returns string 
    def __Build_Padded_Text(self,encoded_text):
        padding_value = 8 - len(encoded_text) % 8         
        for i in range(padding_value):
            encoded_text += '0'           #append the 0s to the encoded value: padding_value times. 
        
        #to store the padded value in its binary 8 bit format 
        padded_info = "{0:08b}".format(padding_value)            #string formatting- 1st 0 is to select which arguement to format, 08b represents '8' bit 'binary' conversion of the arguement.   
        padded_text = padded_info + encoded_text     #string
        return padded_text   
    
    
    
    
    
    def __Build_Byte_Array(self,padded_text):
        array = []
        for i in range(0,len(padded_text),8):       #slice the padded text in 8-8 bits string.
            byte = padded_text[i:i+8]                #i to i+8 slicing
            array.append(int(byte,2))              #array to store the decimal value of the 8 bit binary, base 2
        return array
    
    
    
    
 #Compression path:
#Path->File->Freq Dict->Heap->Binary Tree->Construct Code->Encoded Text->Binary File as output.

    def compression(self):
        
        #steps:
        # 1. Access the file and extract its text.
        filename,file_extension = os.path.splitext(self.path)          #path. splitext() method is used to split the path name into a pair root and ext.
        output_path = filename + '.bin'         #compressed output file with same filename and '.bin' extension
        
        
        
        #file comprehension
        with open(self.path,'r+') as file, open(output_path,'wb') as output:            #'r+' is to read the file, 'wb' is to write in binary
            text = file.read()
            text = text.rstrip()     #remove extra spaces
        
        

            # 2. Construct a frequency dictionary for each letter in the text.
            frequency_dict=self.__frequencydict_from_text(text)



            # 3. Construct a min heap. (min ele is the root node)
            #Use of in-build heap(heapq)
            build_heap = self.__Build_heap(frequency_dict)       #passing the above frequency dictionary for building the heap.



            # 4. Construct a binary tree, its node as the sum of the 2 min leaf nodes taken from the min heap.
            #Each node in BT is a pair of key and its corresponding value(['a': 40]).For leaf nodes, it the character and its freq, whereas for other nodes, the key is just blank, and value is the sum of its child nodes(['': 60]).
            #The resulting node is pushed into the heap.
            self.__Build_Binary_Tree()



            # 5. Construct code from binary tree and store it in a dictionary.
            self.__Build_Tree_Code()




            # 6. Generate the encoded text(binary).
            encoded_text = self.__Build_Encoded_Text(text)



            #Padding of encoded text.
            padded_text = self.__Build_Padded_Text(encoded_text)


            # 8. Return the binary file.
            bytes_array = self.__Build_Byte_Array(padded_text)
            final_bytes = bytes(bytes_array)
            output.write(final_bytes)
            
        print('Compressed file successfully')
        return output_path    #final
    
    
    
    
    #consider code:   00000011|0100110101110111100101001110010|100   - starting 8 bits is the padded_info in base 10  , convert into decimal, those many padded bits are sliced from the ending bits.
    def __Remove_Padding(self,text):
        padded_info = text[:8]
        padding_value = int(padded_info,2)       #converting base 10 to base 2
        text = text[8:]                      #working on the remaining bits except the 1st 8 bits
        text = text[:-1*padding_value]          #removing padding from the end of code - negative slicing 
        return text

    
    
    
    
    def __Decoded_Text(self,text):
        current_bits = ''
        decoded_text = ''
        for char in text:
            current_bits += char       #add the traversing bits until a character with matching code is found. 
            if current_bits in self.__reversecode:
                decoded_text += self.__reversecode[current_bits]
                current_bits = ''      #once a character is found, again initialize curr_bits to empty string to check for other the next character.
    
        return decoded_text
    
    
    
    def decompress(self,input_path):
        filename,file_extension = os.path.splitext(input_path)
        output_path = filename +'_decompressed'+'.txt'       
        
        with open(input_path,'rb') as file, open(output_path,'w') as output:        #input_file is the binary file which is compressed, thus 'rb'
            bit_string = ''          #store the decompressed data
            byte = file.read(1)           #reading file byte wise
            while byte:                        #until file gets empty
                byte = ord(byte)          #ord method to convert the unicode into number
                bits = bin(byte)[2:].rjust(8,'0')            #bin method to convert the previously calculate decimal number to binary. This gives in format b'110 say, for 3... So slicing is done, from index 2 ([2:]), to get only the binary. It is then converted to 8 bit binary by using rjust method. 
                bit_string += bits            #decompressed binary file with padding
                byte = file.read(1)
    
            #remove padding
            text_after_removing_padding = self.__Remove_Padding(bit_string)
    
    
            #creating a reverse dictionary
            actual_text = self.__Decoded_Text(text_after_removing_padding)
            output.write(actual_text)
            
        return output_path    #Final
        
        
        

path = input("Enter the Path of file needed to be compressed:")      #input from the user
h = Huffmancode(path)              #create object for class
compressed_file = h.compression()        #invoking compression func which returns compressed file
h.decompress(compressed_file)


'''
Output bin file:

Binary data is often represented using non-printable characters, and when you try to view it as text, 
it may appear as a series of strange or unintelligible characters.

Files that contain data which isn’t human-readable, especially executable machine code, 
are often called binaries. It looks like gibberish when viewed in a text editor. 

'''