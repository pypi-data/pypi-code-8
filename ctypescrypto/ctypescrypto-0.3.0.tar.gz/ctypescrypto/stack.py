" wrapper around OpenSSL stack abstraction"

class Stack:
    def __init__(crytostruct,itemclass,ptr=None,items=[]):
        """
        Creates stack object.
        @param cryptostruct - name of libcrypto structure such as X509 EVP_PKEY
                        (there must exist ${cryptostruct}_free function)
        @param itemclass - python wrapper class around this structure 

        @param ptr - pointer to existing OpenSSL stack structure. If
                None, new, empty stack would be created
        @param items - list of itemclass objects. If specifed, and ptr
                is None, new stack would be populated with these itesm
                        
        """
        raise NotImplementedError

    def __len__(self):
        """
        Return number of elements in the stack
        """
        return libcrypto.sk_num(self.ptr)
    def __getitem__(self,idx):
        """
        Returns stack element by index
        @param idx - index of stack element
        """
        raise NotImplementedError
    def __putitem__(self,idx,value):
        """
        Replases the item with given index
        @param idx index to replace
        @param value itemclass object
        """
        raise NotImplementedError
    def __del__(self):
        """
        Frees memory used by stack
        """
        libcrypto.sk_pop_free(self.ptr,libcrypto[self.freefunc])
    def append(self,value):
        libcrypto.sk_push(self.ptr,itemclass.clone(value.ptr))  
