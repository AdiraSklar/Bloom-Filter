from BitHash import BitHash
from BitVector import BitVector
from BitHash import ResetBitHash

                             #EQUATION NOTES:

#d= number of Hash Functions 

#N= total number of bits in the array 

#phi = Expected proportion of bits still zero after n inserted keys

#P= false postive rate (all queried bits turn out to be 1’s)
     #porportion of of bits set to 1 in the array

                              #EQUATIONS
#A:                          #P = (1−phi)

#B ( derived from A)         #phi= 1− P^(1/d)

#C                           #phi = (1-d/N)^n

#D ( derived from C)         #N= d/(1- phi^(1/n))

class BloomFilter(object):  
    
    #returns the number of bits N (slots needed) 
    def __bitsNeeded(self, numKeys, numHashes, maxFalsePositive):
        
        #get bitsNeeded ( a.k.a N) 
        
        #(EQUATION B) 
        #first  get phi= the porportion  of zeros after numKeys inserts 
        phi= (1- ((maxFalsePositive)**(1/numHashes)))
        
        #(EQUATION D)
        #next, now that you have phi, get N __bitsNeeded
        N= int(numHashes/(1-((phi)**(1/numKeys))))
    
        return N #return the number of buts needed

    
    def __init__(self, numKeys, numHashes, maxFalsePositive):
        
        self.__numKeys= numKeys
        self.__numHashes= numHashes
        self.__maxFalsePositive= maxFalsePositive
        self.__BitVector= BitVector(size= self.__bitsNeeded(numKeys, numHashes,\
                                                            maxFalsePositive))
        self.__setBits=0   #tracks the amount of bits set to 1 at a given time
   
   
    
    # insert the specified key into the Bloom Filter.
    def insert(self, key):
        #loop from i=1, hash it __numHashes amount of times 
        for i in range(1,self.__numHashes+1): 
            
            slot= BitHash(key,i) % len(self.__BitVector)     #hash the slots 
            
            #if that bit hasnt been set already:
            if self.__BitVector[slot]!=1: 
               
                self.__BitVector[slot]=1                    #set that bit 
               
                self.__setBits+=1                           #incriment setBits
   
                # Doesn't return anything, since an insert into 
                # a Bloom Filter always succeeds!   
   
   
    # find if the key is in bloom filter 
    # Returns True if key MAY have been inserted into the Bloom filter. 
    # Returns False if key definitely hasn't been inserted into the BF.
    #mod N
    def find(self, key):
        for i in range(1,self.__numHashes+1):  
            
            slot= BitHash(key,i) % len(self.__BitVector)   #hash the slots 
            
            if self.__BitVector[slot]!=1:                  #if any bit isnt set
                
                return False                               #immediatly 
                                                           #return false
                                                           
        return True           #otherwise return True,to mark a MAYBE found key 
       
       
       

    # Returns the PROJECTED current false positive rate based on the
    # ACTUAL current number of bits actually set in this Bloom Filter. 
    #calculating P from phi and d 
    def falsePositiveRate(self):
        #phi is now the current number remaining zeroes in porportion to the  
        #total num of bits in the bitVector
        
        total= len(self.__BitVector)
        
              #amount of zeros       #over total bits
        phi= (total - self.__setBits)/total 
        
        #now calculate P (current false pos rate based in current phi) 
        P= (1- phi)**self.__numHashes
       
        return P                #return projected false positive rate 
        
    #return the amount of bits cuurently set 
    def numBitsSet(self): 
        return self.__setBits    

       

def __main():
    numKeys = 100000
    numHashes = 4
    maxFalse = .05
    
    #make bloom filter with these parameters
    a= BloomFilter(numKeys, numHashes, maxFalse)
    
    #now insert the first 100,000 words of the word file into into it 
    file= open("wordlist.txt")
    for i in range(100000):
        key=file.readline()
        a.insert(key)
    file.close()
    
    #print(a.numBitsSet())
    
    #print projected  false positive rate 
    print("projected False Positive Rate: "+ str(a.falsePositiveRate()))
    


    #now check that all of these keys that were insterted can be 
    #found in the Bloom Filter 
    missingWords=0 #counts any words not found in the BF
    file= open("wordlist.txt")
    for i in range(100000):
        key=file.readline()
        if not a.find(key): 
            missingWords+=1
                        
    print("missing words: "+ str(missingWords))  #yup its zero! 
                                         #all the keys were inserted properly:)
   
    # Now read the next 100,000 words from the file, none of which 
    # have been inserted into the Bloom Filter, and count how many of the 
    # words can be (falsely) found in the Bloom Filter.( actual fasle positive) 
    falselyFound=0
    for i in range(100000):
        key=file.readline()
        if  a.find(key): 
            falselyFound+=1
    file.close()
    print("Falsely found keys: "+ str(falselyFound)) 
   
    
    #get real percentage of false positives 
    #amnt of falsePos/amount searched 
    actFalsePos= falselyFound/100000 
    print("Actual False Positive Rate: "+ str(actFalsePos))
    
    #yay its very close to projected False Pos!! both around 0.05%
    
    
            
    
if __name__ == '__main__':
    __main()       

