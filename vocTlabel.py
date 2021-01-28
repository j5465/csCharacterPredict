import os
import xml.etree.ElementTree as ET
import datetime
import shutil

classes = ["fbih", 'fbi', 'th', 't']

now = datetime.datetime.now()
index = 1
new = []
train_val = []
dst_dir = "data/dst"
Annotations_dir = "cs-PascalVOC-export/Annotations"
jpgImages = 'cs-PascalVOC-export/JPEGImages'


def convert(size, box):
  dw = 1.0 / (size[0])
  dh = 1.0 / (size[1])
  x = (box[0] + box[1]) / 2.0 - 1
  y = (box[2] + box[3]) / 2.0 - 1
  w = box[1] - box[0]
  h = box[3] - box[2]
  x = x * dw
  w = w * dw
  y = y * dh
  h = h * dh
  return (x, y, w, h)


def convert_annotation(fpath):
  global index
  tree = ET.parse(open(fpath))
  root = tree.getroot()
  jpgname = root.find("filename").text
  jpgpath = os.path.join(dst_dir, jpgImages, jpgname)

  while "{}_{}_{}_{}".format(now.year, now.month, now.day, index) in train_val:
    index += 1
  newname = "{}_{}_{}_{}".format(now.year, now.month, now.day, index)
  # print(newname)

  size = root.find("size")
  w = int(size.find("width").text)
  h = int(size.find("height").text)
  hav = False

  for obj in root.iter("object"):
    hav = True
    difficult = obj.find("difficult").text
    cls = obj.find("name").text
    # if cls not in classes or int(difficult) == 1:
    # continue
    if cls == "c":
      cls_id = 1
    elif cls == 't':
      cls_id = 3
    else:
      cls_id = classes.index(cls)
    xmlbox = obj.find("bndbox")
    b = (
        float(xmlbox.find("xmin").text),
        float(xmlbox.find("xmax").text),
        float(xmlbox.find("ymin").text),
        float(xmlbox.find("ymax").text),
    )
    bb = convert((w, h), b)
    with open(os.path.join("data/csmodels/ct/", newname + ".txt"), "a+") as f:
      f.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + "\n")
  if hav:
    train_val.append(newname)
    shutil.copy(jpgpath, os.path.join("data/csmodels/ct/", newname + ".jpg"))
    new.append(os.getcwd() + "/data/csmodels/ct/" + newname + ".jpg" + "\n")


with open(os.path.join("data/csmodels/ct/train_val.txt"), "a+") as f:
  f.seek(0)
  train_val = f.read().split("\n")
  for i in range(len(train_val)):
    train_val[i] = train_val[i].split("/")[-1].split(".")[0]

# print("train_val list:", train_val)


xml_list = os.listdir(os.path.join(dst_dir, Annotations_dir))
for fn in xml_list:
  if fn.endswith(".xml") == False:
    continue
  print(fn)
  convert_annotation(os.path.join(dst_dir, Annotations_dir, fn))
trainP = 7

with open(os.path.join("data/csmodels/ct/train_val.txt"), "a+") as f:
  for line in new:
    f.write(line)

for i in range(len(new)):
  flag = "train" if i % 10 < trainP else "val"
  with open(os.path.join("data/csmodels/ct/{}.txt".format(flag)), "a+") as f:
    f.write(new[i])
