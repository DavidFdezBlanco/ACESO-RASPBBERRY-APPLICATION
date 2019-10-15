# ACESO-RASPBBERRY-APPLICATION

## Sur linux based systems 

Clone the file into a local repository with git clone ....

Then make the command sudo npm install --unsafe-perm=true --alw-rootls

Finally npm start

## Sur windows based systems 


## Organisation

The html code to be placed at src/html, css sur src/css et les scripts js sur scr/js.
Le main.py will be the first js class that will be executed. If you want to access the DevTools uncomment the line mainWindow.webContents.openDevTools() on the main.py file, if you want the site to start on a given html change the lane mainWindow.loadFile('src/html/index.html'). 

# Git use

Commits must have a format: [Coder Name] - date - What you have changed

To commit, you need to :
  1. git pull
  2. check .gitignore to see if you have excluded the libraries (not useful, they can be replicated with npm install...)
  3. git add file_to_commit
  4. git commit
  5. git push
