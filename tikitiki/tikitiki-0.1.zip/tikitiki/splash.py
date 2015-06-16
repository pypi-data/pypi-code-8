try: # 2.x
    import Tkinter as tk
    import ttk
    import Tix
except: # 3.x
    import tkinter as tk
    import tkinter.ttk as ttk
    import tkinter.tix as Tix
import time
import tikitiki

'''
A basic splash gif displayed for a set number of seconds prior to loading
'''
class SplashScreen( object ):
  def __init__( self, tkRoot, image_str, minSplashTime=0, hideMain=True, isFilename=True ):
    self._hideMain = hideMain
    self._root              = tkRoot
    self._isFilename = isFilename
    self._img_data = image_str
    # self._image             = Tix.PhotoImage( file=imageFilename )
    self._splash            = None
    if minSplashTime is 0:
      self._minSplashTime = 0
    else:
      self._minSplashTime     = time.time() + minSplashTime

  def __enter__( self ):
    # Remove the app window from the display
    
    if self._hideMain:
      
      self._root.withdraw( )
      
      # Calculate the geometry to center the splash image
      if self._isFilename:
        self._image             = Tix.PhotoImage( file=self._img_data )
      else:
        self._image = Tix.PhotoImage( data=self._img_data)

      scrnWt = self._root.winfo_screenwidth( )
      scrnHt = self._root.winfo_screenheight( )

      imgWt = self._image.width()
      imgHt = self._image.height()

      imgXPos = (scrnWt / 2) - (imgWt / 2)
      imgYPos = (scrnHt / 2) - (imgHt / 2)

      # Create the splash screen      
      self._splash = Tix.Toplevel()
      self._splash.overrideredirect(1)
      self._splash.geometry( '+%d+%d' % (imgXPos, imgYPos) )

      self._label = Tix.Label( self._splash, image=self._image, cursor='watch' )
      self._label.pack( )

      # Force Tk to draw the splash screen outside of mainloop()
      self._splash.update( )
      #self._splash.update_idletasks() <-- this is meant to be safer but it doesn't display the gif or hide the window scaffolding...

  def __exit__( self, exc_type, exc_value, traceback ):
      # Make sure the minimum splash time has elapsed
      timeNow = time.time()
      if self._minSplashTime is not 0 and self._hideMain:
        if timeNow < self._minSplashTime:
          time.sleep( self._minSplashTime - timeNow )
          # get the time between frames - delay 0.05 of a sec
          #time.sleep( 0.05 )
        
        # Destroy the splash window
        self._splash.destroy( )
        
        # Display the application window
        if self._hideMain:
          self._root.deiconify( )

'''
spinner is like splash except that it:
* is displayed during program execution not before
* is started explicitly
* includes a callback to check if it may exit from the animation of it's spinner ( so the background task should be in a separate process)
'''
class Spinner(object):
  
  NO_OF_FRAMES = 31
  GIF_FRAME_RATE = 0.05

  def __init__(self, tkRoot):
    self._root              = tkRoot
    self._img_data = tikitiki.working_encoded
    self._splash            = None

  def show(self, callback_obj, check_progress):

    self._image = Tix.PhotoImage( data=self._img_data, format='gif -index 0')
    self._cb = callback_obj

    wndWt = self._root.winfo_width( )
    wndHt = self._root.winfo_height( )
    
    imgWt = self._image.width()
    imgHt = self._image.height()
    
    left = self._root.winfo_rootx()
    top = self._root.winfo_rooty()

    imgXPos = left + (wndWt / 2) - (imgWt / 2)
    imgYPos = top + (wndHt / 2) - (imgHt / 2)

    self._check_every = check_progress/Spinner.GIF_FRAME_RATE

    self._splash = Tix.Toplevel()
    self._splash.overrideredirect(1)
    self._splash.geometry( '+%d+%d' % (imgXPos, imgYPos) )
    self._splash.update_idletasks()

    self._label = Tix.Label( self._splash, image=self._image, cursor='watch' )
    self._label.pack()

    self.animate(0, 0)

  def animate(self, frame, cp):
    # check callback object, implements CheckProcessor interface
    if cp > self._check_every:
      cp = 0
      if not self._cb.still_processing():
        self.hide()
        return
    else:
      cp+=1
    frame = frame+1 if frame < (Spinner.NO_OF_FRAMES-1) else 0
    p = Tix.PhotoImage(data=self._img_data, format='gif -index %d' % frame)
    self.image = p
    self._label.configure(image=p)
    self._splash.update_idletasks()
    self._splash.after(int(Spinner.GIF_FRAME_RATE*1000), lambda: self.animate(frame, cp))

  def hide(self):
    self._splash.destroy()

'''
supplies check_progress interface for gui classes wishing to use the Spinner animation
Naturally, the 'work' should be running in a separate process.
'''
class CheckProcessor(object):
  def still_processing(self):
    raise NotImplementedError('Method not implemented in subclass')

#--------------------------------------------
# Now putting up splash screens is simple

if __name__=='__main__':
  # Create the tkRoot window
  tkRoot = tk.Tk( )
  
  with SplashScreen( tkRoot, tikitiki.working_encoded, 3.0, True, False ):
    pass
  tkRoot.mainloop( )


