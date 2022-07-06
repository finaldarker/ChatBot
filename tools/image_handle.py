from PIL import Image

def image_handle(head_file):
    save_name='head_temp.png'
    picture_filepath='../resources/BG/'
    im1 = Image.open(picture_filepath+'log.png')
    # 加载头像图片
    im2 = Image.open(head_file)
    #图片裁剪
    im2 = im2.crop((im2.size[1]//6,0, im2.size[1]+im2.size[1]//6, im2.size[1]))
    #图片压缩
    im2=im2.resize((98,98), Image.ANTIALIAS)
    # 将头像框照片与头像图片大小调整到一置
    im2 = im2.resize((im1.size))
    im2.paste(im1, (0, 0), im1)
    im2.save(picture_filepath+save_name)
    #im2.show()

