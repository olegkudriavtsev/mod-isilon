# mod-isilon
mod-isilon repo

Representation of Isilon module.

## Development notes
Before development add `venv`:
```
virtualenv -p python3.7 path/to/virtualenv
source path/to/virtualenv/bin/activate

pip3 install -r requirements.txt
```

## Run application
For running application can be used 2 approaches for the moment: 
    - run via IDE, e.g. PyCharm.
    - run from console like ```python main.py```


### Run from IDE
For running from IDE first you need to install all requirements in root folder.
```
pip3 install -r requirements.txt
```

## Optional arguments
To use verbose pass -v or --verbose argument
To use server reflection use -r or --enable_reflection argument, it may be helpful for tools like grpcui
Use -h argument to see help text
