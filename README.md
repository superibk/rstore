# Rstore
A command line tool that communicates with the public Reddit API, stores information about posts, and on subsequent executions can tell which posts are new, which posts have dropped off, and which had vote changes.

## Development
- To avoid complex storage setup, I stored the top N (N is 75 here) post details in a file  (.old_store) 
- Since the only major storage are the post details, I felt there was no need for a database 
- Retrieving the data as json is straight forward from the file 
- Using json and python dictionary, the access time is fast and optimized

## Installation

- Unzipped the rstore.zip file
- Run the command './install.sh' from the root directory of the rstore folder .

  Alternatively, you can run the command ' pip install . ' from the root directory ([install pip if you don't already have it](https://github.com/pypa/pip)) .


  ![](rstore.gif)

- Run 'rstore' from your command line(terminal) interface

- To Uninstall run "pip uninstall rstore"
