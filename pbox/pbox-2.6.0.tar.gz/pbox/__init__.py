#!/usr/bin/env python
#--------------------------------------------------------------------------------------------------------------
import textwrap
#--------------------------------------------------------------------------------------------------------------

__name__ = 'pbox'
__version__ = '2.6.0'
__author__ = 'Caveiramanca'
__email__ = 'caveiramanca@gmail.com'
__license__ = 'LGPL'
__url__ = 'https://bitbucket.org/caveiramanca/pbox/'

_packages = ['pbox']
_requires = []
_info = 'Pbox is a simple module that makes it easier to handle persistent data using pickle or json.'
_keywords = ['pickle', 'persistent data', 'cPickle', 'json']
_platforms = ['Posix', 'Windows'] 
_download_url = 'https://bitbucket.org/caveiramanca/pbox/src/master/dist/'

_more_info = textwrap.dedent('''
                    **Pbox** is a simple module that makes it easier to handle persistent data using **pickle** or **json**.
                    You don't need to worry about writing and reading external files as well as packing and unpacking 
                    your objects to and from dictionaries. **It's all done for you!**
                    
                    Source code and **documentation** can be found `here <https://bitbucket.org/caveiramanca/pbox>`_.
                    
                    
                    **Changelog**
                    
                    Version 2.6.0:

                    * Added option to use **json** instead of **pickle**.
                    * Methods **datafile** and **cached** were added to manually overwrite the **box** contents.
                    
                    Version 2.5.4:

                    * Expanding **documentation**.
                    * Minor **code** refactoring.
                    
                    Version 2.5.3:

                    * Minor **code** refactoring.

                    Version 2.5.2:

                    * Fixed issue that prevented to **dump** objects living inside **functions** or **classes**.

                    Version 2.5.1:

                    * Added **cache_datafile** property to save the **data-file** content into **cache**.
                        
                    ''').strip()
                    
_readme = textwrap.dedent(
                    ''' 
                    PBOX
                    -----------------------------------------------------------------------------------------------------------

                    Pbox is a simple module that makes it easier to handle persistent data using **pickle** or **json**.
                    You don't need to worry about writing and reading external files as well as packing and unpacking your 
                    objects to and from dictionaries. **It's all done for you**!

                    **To use the module do as following:**

                    -----------------------------------------------------------------------------------------------------------    

                    **importing Module:**

                    You can import the module in any way. The only new object reference added to your program scope will
                    be the module **pbox** or the class **CreateBox**.
                    ``` python
                            # Import the entire module ...
                            import pbox
                            # or just the class CreateBox.
                            from pbox import CreateBox
                            from pbox import * 
                    ```
                    -----------------------------------------------------------------------------------------------------------

                    **Creating Box Instance:**

                    You can either create a box with the defaut setup...
                    ``` python
                            import pbox
                            box = pbox.CreateBox()  # Default data-file = 'datafile.box'
                                                    # Default data-folder = './dat'
                                                    # Default encoding Protocol = pickle.HIGHEST_PROTOCOL or 2
                                                    # Default library type = 'pickle'
                    ```
                    or you can create a box with a specific setup:
                    ``` python
                            box = CreateBox(file = 'DATA.DAT', folder = '../MY_DATA_FOLDER/DATA', protocol = 0, type = 'json')
                                                    # Note that when you use 'json' instead of 'pickle', the protocol 
                                                    # attribute is actually ignored.
                    ```
                    -----------------------------------------------------------------------------------------------------------

                    **Managing Persistent Data:**
       
                    To **dump** objects just add them as **strings**, for instance:
                    ``` python
                            box = pbox.CreateBox()   
        
                            script = 'PBOX'
                            box.dump('script')
                    ```
                    You can **dump** various objects at once:
                    ``` python
                            name = 'CAVEIRAMANCA'
                            numbers = [2, 4, 6, 8, 10]
    
                            box.dump('script', 'name', 'numbers')
                    ```
                    To **pick** your objects from file, just call them as **strings** again.
                    You can only **pick** one object at a time, thou.
                    ``` python
                            name = box.pick('name')
                            numbers = box.pick('numbers')
                    ```
                    Objects can be of any kind but keep in mind if you **dump** a **function** or a **class**,
                    those objects will only be accessible during the same **Python** session.
                    I do not recommend doing that since in my tests it lead to pretty strange pickling behaviours.

                    if you experience somethig very weird, **try deleting the data-file**.
                    But avoid dumping **functions** or **classes** and you will be good to go.
                    
                    And by the way, if you are using **json** instead of **pickle**, you should never dump those types
                    of objects anyways. Also **json** protocol doesn't support **tuples**, all **tuples** are converted to 
                    **lists** when picked. Keep that in mind.
        
                    To remove objects from the **data-file** do as following...
                    ``` python
                            box.remove('script')
                            box.remove('name', 'numbers')
                    ```
                    and finally to **list** all objects saved in the **data-file**:
                    ``` python
                            box.list()
                    ```
                    -----------------------------------------------------------------------------------------------------------

                    **Using The Cache:**

                    If you need to add many objects at once or you have any object you might need to **pick** very often,
                    it's probably faster to use the **cache** instead of keep accessing the **data-file** all the time.

                    To add objects to the **cache** just do as following:
                    ``` python
                            box.cache('script', 'name', 'numbers')
                    ```
                    And to **pick** objects from **cache** type:
                    ``` python
                            box.pick('script', cache = True)
                    ```
                    **Listing** all objects in **cache** is also very straight forward:
                    ``` python
                            box.list(cache = True)
                    ```
                    So a good workflow if you need to add many objects from different parts of your code
                    is to create and use the same **box** since the **cache** of a **box** is saved in it's **instance**.
                    And then do as following:
                    ``` python
                            box.cache('object_01')
                            box.cache('object_02')
                            box.cache('object_03')
                            box.cache('object_04')
                
                            box.consolidate
                    ```
                    Being that once you **consolidate**, you push everything that is in the **cache** to the **data-file**.

                    And if you need to **pick** many objects at a time, it's probably a good idea to push them to **cache**
                    so you can avoing accessing the **data-file** all the time. That's how you do it:
                    ``` python
                            box.cache_datafile
        
                            obj1 = box.pick('object_01', cache = True)
                            obj2 = box.pick('object_02', cache = True)
                            obj3 = box.pick('object_03', cache = True)
                            obj4 = box.pick('object_04', cache = True)
                    ```
                    Note that you can't remove specific objects from the **cache** but you can sure **flush** it.
                    ``` python
                            box.flush
                    ```
                    This will empty the **cache**.
                    
                    -----------------------------------------------------------------------------------------------------------
                    
                    **A Few Other Handy Features:**
                    
                    You can **iterate** and count the number of objects in the **box**. Objects will be passed as **dictionaries**.
                    ``` python
                            box = pbox.CreateBox()
                            
                            for items in box:       # Outputs: {'object_01': 'value_object_01'}
                                print(items)        #          {'object_02': 'value_object_02'}
                                                    #          {'object_03': 'value_object_03'}
                                                    #          {'object_04': 'value_object_04'}
                            
                            len(box)                # Outputs: 4        
                    ```
                    **Iteration** and **len()** will take in consideration only the items in the **box** and 
                    not in the **cache**.
                    
                    You can also directly access the **data-file** and **cache** **dictionaries** to test their contents or
                    manipulate them directly. Just do as following:
                    ``` python
                            new_box = {'new_objectA': 'value_objectA', 'new_objectB': 'value_objectB'}
                            box.datafile = new_box
                            
                            if box.datafile:
                                print(box.datafile)
                            
                            new_cache = {'new_objectA': 'value_objectA', 'new_objectB': 'value_objectB'}
                            box.cached = new_cache
                                                                 
                            if box.cached:
                                print(box.cached)
                    ```
                    -----------------------------------------------------------------------------------------------------------

                    Keep in mind that objects in the **cache** or **data-file** need to **be unique**.
                    Adding an object with the same name of one that's already there will cause the value
                    of the object to be **updated**.

                    That's it folks, I hope you find this module useful. **Enjoy!**
                    
                        Caveiramanca - 2015
                    -----------------------------------------------------------------------------------------------------------

                    **Changelog**
                    
                    Version 2.6.0:

                    * Added option to use **json** instead of **pickle**.
                    * Methods **datafile** and **cached** were added to manually overwrite the **box** contents.
                    
                    Version 2.5.4:

                    * Expanding **documentation**.
                    * Minor **code** refactoring.
                    
                    Version 2.5.3:

                    * Minor **code** refactoring.

                    Version 2.5.2:

                    * Fixed issue that prevented to **dump** objects living inside **functions** or **classes**.

                    Version 2.5.1:

                    * Added **cache_datafile** property to save the **data-file** content into **cache**.

                    -----------------------------------------------------------------------------------------------------------
                    ''').strip()
                    
_classifiers = textwrap.dedent('''
                    Development Status :: 5 - Production/Stable
                    Intended Audience :: Developers
                    Operating System :: OS Independent
                    Natural Language :: English
                    Programming Language :: Python :: 2
                    Programming Language :: Python :: 3
                    Topic :: Software Development
                    Topic :: Software Development :: Libraries :: pygame
                    Topic :: Software Development :: Libraries :: Python Modules
                    Topic :: Games/Entertainment
                    ''').strip().splitlines()

_manifest = textwrap.dedent('''
                include README.md
                include README.txt
                include MANIFEST.in
                include LICENSE.txt
                recursive-include
                ''').strip()
                
_setup_cfg = textwrap.dedent('''
                [metadata]
                description-file = README.md
                ''').strip()

# --------------------------------------------------------------------------------------------------------------
__doc__ = _readme.replace('**', '').replace('``` python', '').replace('```', '')
#--------------------------------------------------------------------------------------------------------------
from .pbox import *
__all__ = ['CreateBox']
#--------------------------------------------------------------------------------------------------------------
#  END
#--------------------------------------------------------------------------------------------------------------