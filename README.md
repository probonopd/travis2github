# travis2github [![Build Status](https://travis-ci.org/probonopd/travis2github.svg)](https://travis-ci.org/probonopd/travis2github)

Upload travis builds to GitHub Releases.

## 1. Add "travis" release to your project

You need to do this manually. Note that this release will be deleted and re-created every time travis-ci builds and uploads your software, hence providing a mechanism for having always the latest build available.

## 2. Edit .travis.yml

In your `.travis.yml`, add:

```
sudo: true # Is there a way around this?
install:
- sudo apt-get update -qq
- sudo apt-get install python-requests -qq # Is there a way around this?
- git clone https://github.com/username/repository.git
script:
- cd ./repository
- # Whatever is needed to build your software 
- ls -lh ./yourbinary # Assuming this is the binary you want to upload to GitHub Releases
- wget https://raw.githubusercontent.com/probonopd/travis2github/master/travis2github.py
- wget https://raw.githubusercontent.com/probonopd/travis2github/master/magic.py
- python travis2github.py ./yourbinary
```
