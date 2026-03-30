# coding=utf-8
'''
Created on Apr 23, 2018
Desc: Webp convertor
@author: Mashiro https://2heng.xin
'''
import os
import sys
import json
import hashlib
from PIL import Image

# 获取脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GALLARY_DIR = os.path.join(SCRIPT_DIR, 'gallary')
JPEG_DIR = os.path.join(SCRIPT_DIR, 'jpeg')
WEBP_DIR = os.path.join(SCRIPT_DIR, 'webp')

class Single(object):
  def __init__(self, file, manifest):
    self.file = file
    self.mani = manifest

  def hash(self):
    hasher = hashlib.md5()
    with open(os.path.join(GALLARY_DIR, self.file), 'rb') as afile:
      buf = afile.read()
      hasher.update(buf)
    self.hash = hasher.hexdigest()
    self.jpeg = os.path.join(JPEG_DIR, self.hash + '.jpeg')
    self.webp = os.path.join(WEBP_DIR, self.hash + '.webp')
    self.jpeg_th = os.path.join(JPEG_DIR, self.hash + '.th.jpeg')
    self.webp_th = os.path.join(WEBP_DIR, self.hash + '.th.webp')

  def optimize(self):
    im = Image.open(os.path.join(GALLARY_DIR, self.file)).convert('RGB')
    im.save(self.jpeg, 'JPEG')
    im.save(self.webp, 'WEBP')
    im.thumbnail((450, 300))
    im.save(self.jpeg_th, 'JPEG')
    im.save(self.webp_th, 'WEBP')

  def manifest(self):
    self.mani[self.hash] = {
      'source': self.file,
      'jpeg': [self.jpeg, self.jpeg_th],
      'webp': [self.webp, self.webp_th]
    }

  def main(self):
    self.hash()
    self.optimize()
    self.manifest()
    return self.mani

def gen_manifest_json():
  onlyfiles = [f for f in os.listdir(GALLARY_DIR) if os.path.isfile(os.path.join(GALLARY_DIR, f))]
  id = 1
  Manifest = {}
  for f in onlyfiles:
    try:
      worker = Single(f, Manifest)
      Manifest = worker.main()
      print(str(id) + '/' + str(len(onlyfiles)))
      id += 1
    except OSError:
      print("Falied to optimize the picture: " + f)
  with open(os.path.join(SCRIPT_DIR, 'manifest.json'), 'w+') as json_file:
    json.dump(Manifest, json_file)


def main():
  gen_manifest_json()


if __name__ == '__main__':
  main()
  key = input('`manifest.json` saved. Press any key to quit.')
  quit()
