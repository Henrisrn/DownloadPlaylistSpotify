import pytube
  
# where to save 
SAVE_PATH = "C://Users//henri//Downloads//Musiquepython" 
  
# link of the video to be downloaded 
link="https://www.youtube.com/watch?v=xWOoBJUqlbI"
yt = pytube.YouTube(link)
stream = yt.streams.first()
stream.download()