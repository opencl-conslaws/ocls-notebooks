import os
from base64 import b64encode
from IPython.display import HTML
import cv2
import matplotlib.pyplot as plt
import numpy

codec2ext = dict(flv='flv', libx264='mp4', libvpx='webm',
                libtheora='ogg')

def encode_video(fps, prefix):
    filespec = '/tmp/{0}_frame_%04d.png'.format(prefix)
    movie_program = 'avconv'  # or 'ffmpeg'
    for codec in codec2ext:
        ext = codec2ext[codec]
        cmd = '%(movie_program)s -r %(fps)d -i %(filespec)s -y '\
              '-vcodec %(codec)s /tmp/%(prefix)s_movie.%(ext)s' % vars()
        #print cmd
        os.system(cmd)

def create_video_html_tag(prefix):
    video_tag = '<video controls>'
    for codec in codec2ext:
        ext = codec2ext[codec]
        video = open("/tmp/%(prefix)s_movie.%(ext)s" % vars(), "rb").read()
        video_encoded = b64encode(video)
        video_tag += ('<source src="data:video/{1};base64,{0}" type="video/{1}">'
                         .format(video_encoded, ext))
    video_tag += 'No video support</video>'
    return video_tag

def notebook_show_video(tag):
    return HTML(data=tag)

def show_log(n=10):
    fname = "fw.log"     # File to check

    with open(fname, "r") as f:
        f.seek (0, 2)           # Seek @ EOF
        fsize = f.tell()        # Get Size
        f.seek (max (fsize-1024, 0), 0) # Set pos @ last n chars
        lines = f.readlines()       # Read to end

    lines = lines[-n:]    # Get last 10 lines
    for line in lines:
        #if "WARNING" is not in line:
        print line


def fig2data ( fig ):
    # draw the renderer
    fig.canvas.draw ( )

    buf = fig.canvas.tostring_rgb()

    img = numpy.fromstring(buf, numpy.uint8)
    im_size = fig.canvas.get_width_height()
    rgb = img.reshape(im_size[1], im_size[0], 3)
    return rgb
    #r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]

    # Get the RGBA buffer from the figure
    #w,h = fig.canvas.get_width_height()
    #buf = numpy.fromstring ( fig.canvas.tostring_argb(), dtype=numpy.uint8 )
    #buf.shape = ( w, h,4 )

    # canvas.tostring_argb give pixmap in ARGB mode. Roll the ALPHA channel to have it in RGBA mode
    #buf = numpy.roll ( buf, 3, axis = 2 )
    #return buf

# Video globals
codec2ext_cv = dict(X263='mp4', VP80='webm',
                    FLV1='flv', THEO='ogg')
out = [None]*len(codec2ext_cv)

def start_recording(name, fps=24, w=800, h=600):
    i = 0
    for codec in codec2ext_cv:
        ext = codec2ext_cv[codec]
        fourcc = cv2.cv.CV_FOURCC(*'%(codec)s' % vars())
        out[i] = cv2.VideoWriter('%(name)s.%(ext)s' % vars(),fourcc,fps,(w,h))
        if out[i].isOpened() is False:
            print "Unsupported video codec (%(codec)s) or format (%(ext)s)" % vars()
        i += 1

def stream_frame(frame):
    for i in range(len(out)):
        if out[i].isOpened():
            out[i].write(frame[:,:,::-1])

def stop_recording():
    for i in range(len(out)):
        out[i].release()

def show_video(name):
    video_tag = '<video controls>'
    for codec in codec2ext_cv:
        ext = codec2ext_cv[codec]
        try:
            video = open("%(name)s.%(ext)s" % vars(), "rb").read()
        except:
            continue
        video_encoded = b64encode(video)
        video_tag += ('<source src="data:video/{1};base64,{0}" type="video/{1}">'
                         .format(video_encoded, ext))
    video_tag += 'No video support</video>'
    return notebook_show_video(video_tag)
