    # detections = darknet.detect_image(
    #     netMain[1], metaMain[1], darknet_image[1], thresh=0.5)
    # res = savebody_head(detections, NewImageName, 1)

    # if res and not (NewImageName in imglist) and time.time() - last_save > 1:
    #   last_save = time.time()
    #   print("body add ", NewImageName)
    #   imglist.append(NewImageName)
    #   Image.frombytes("RGB", st.size, st.bgra, "raw", "BGRX").save(
    #       path + '/{}.jpg'.format(NewImageName), quality=100, subsampling=0)
    # image = cvDrawBoxes(detections, image)