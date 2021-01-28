import os
path = os.path.join(os.getcwd(), 'data/csmodels/archive')
fl = os.listdir(path)
train_val = []
for dn in fl:
  print("dn", dn)
  if os.path.isdir(path + '/' + dn):
    imgl = os.listdir(path + '/' + dn)
    for img in imgl:
      if img.endswith('.jpg'):
        if img.split('.')[0] + '.txt' in imgl:
          train_val.append(path + '/{}/{}\n'.format(dn, img))


ft = open('data/train.txt', 'w')
fv = open('data/val.txt', 'w')
for i in range(len(train_val)):
  if i % 10 < 8:
    ft.write(train_val[i])
  else:
    fv.write(train_val[i])
