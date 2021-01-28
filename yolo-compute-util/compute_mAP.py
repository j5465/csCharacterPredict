from voc_eval import voc_eval
import os

map_ = 0
# classnames填写训练模型时定义的类别名称
classnames = ["c", "t"]
for classname in classnames:
    ap = voc_eval(
        "../results/{}.txt",
        "../data/VOC/VOCdevkit/VOC2007/Annotations/{}.xml",
        "../data/VOC/2007_test.txt",
        classname,
        ".",
    )
    map_ += ap
    # print ('%-20s' % (classname + '_ap:')+'%s' % ap)
    print("%s" % (classname + "_ap:") + "%s" % ap)
# 删除临时的dump文件
if os.path.exists("annots.pkl"):
    os.remove("annots.pkl")
    print("cache file:annots.pkl has been removed!")
# 打印map
map = map_ / len(classnames)
# print ('%-20s' % 'map:' + '%s' % map)
print("map:%s" % map)
