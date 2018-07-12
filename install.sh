
echo Install brew
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
echo End Installation brew
brew upgrade

echo Install Python3.6
brew install python3
python3 -m pip install --upgrade pip

echo Install pygame and other required packages
python3 -m pip install -U pygame --user
python3 -m pip install openpyxl
python3 -m pip install numpy
python3 -m pip install moviepy
