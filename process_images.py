from pytube import Playlist
pl = Playlist("https://www.youtube.com/playlist?list=PLwVftHdWAdHM8l1N2EXmteTbE_nj_l2ER")
urls = pl.parse_links()
print(urls)
pl.download_all()

