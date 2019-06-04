import os


def path_to_list(path):
  folders = []
  while True:
    path, folder = os.path.split(path)
    if folder:
      folders.append(folder)
    else:
      if path:
        folders.append(path)
      break
  folders.reverse()
  return folders

def path_delimiter():
  Folders = ['a','b']
  x = os.path.join(*Folders)
  return x[1]