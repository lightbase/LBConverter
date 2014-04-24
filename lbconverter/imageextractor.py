import os

def extract_pdf_images(pdf_path, root):
    """ @param pdf_path: pdf path on file system 
        @param root: file system path used to save images
        Return list of file system paths (images)
    """

    pdf = file(pdf_path, "rb").read()

    images = [ ]
    startmark = "\xff\xd8"
    startfix = 0
    endmark = "\xff\xd9"
    endfix = 2
    i = 0

    njpg = 0
    while True:

        istream = pdf.find("stream", i)
        if istream < 0:
            break
        istart = pdf.find(startmark, istream, istream+20)
        if istart < 0:
            i = istream+20
            continue
        iend = pdf.find("endstream", istart)
        if iend < 0:
            break
            raise Exception("Didn't find end of stream!")
        iend = pdf.find(endmark, iend-20)
        if iend < 0:
            break
            raise Exception("Didn't find end of JPG!")

        istart += startfix
        iend += endfix
        #print "JPG %d from %d to %d" % (njpg, istart, iend)
        jpg = pdf[istart:iend]
        jpgfile_path = root + "/jpg%d.jpg" % njpg

        if not os.path.exists(root):
            os.makedirs(root)

        jpgfile = file(jpgfile_path, "wb")
        jpgfile.write(jpg)
        jpgfile.close()

        images.append(jpgfile_path)

        njpg += 1
        i = iend

    return images
