from common.abstract_threading import (
    atomic, Future, set_thread_pool, ThreadPool,
    turn_jitting_off)
import sys, time


def calculate(a, b, im_size, max_iter=255):
    #print "a:%s, b:%s, im_size:%s" % (a, b, im_size)
    ar, ai = a
    br, bi = b
    width, height = im_size
    imag_step = (bi - ai) / (height - 1)
    real_step = (br - ar) / (width - 1)
    #print "real/width:%s, imag/height:%s" % (real_step, imag_step)

    result = [[0] * width for y in xrange(height)]
    for y in xrange(height):
        zi = ai + y * imag_step
        for x in xrange(width):
            zr = ar + x * real_step
            z = complex(zr, zi)
            c = z
            for i in xrange(max_iter):
                if abs(z) > 2.0:
                    break
                z = z * z + c
            result[y][x] = i

    return result

def save_img(image, file_name='out.png'):
    from PIL import Image
    im = Image.new("RGB", (len(image[0]), len(image)))
    out = im.load()

    for y in xrange(len(image)):
        for x in xrange(len(image[0])):
            c = image[y][x]
            out[x,y] = c, c, c
    im.save(file_name, 'PNG')

def save_to_file(image, file_name='out.txt'):
    with atomic:
        s = "\n".join(map(str, image))
    with open(file_name, 'w') as f:
        f.write(s)


def merge_imgs(imgs):
    res = []
    for img in imgs:
        for y in img:
            res.append(y)
    return res


def run(threads=2, stripes=64, w=4096, h=4096):
    global out_image
    threads = int(threads)
    stripes = int(stripes)
    assert stripes >= threads
    ar, ai = -2.0, -1.5
    br, bi = 1.0, 1.5
    width, height = int(w), int(h)

    set_thread_pool(ThreadPool(threads))
    step = (bi - ai) / stripes
    res = []
    ai = -1.5
    bi = ai + step
    parallel_time = time.time()
    for i in xrange(stripes):
        res.append(Future(calculate,
                          a=(ar, ai + i * step),
                          b=(br, bi + i * step),
                          im_size=(width, int(height / stripes))
            ))

    res = [f() for f in res]
    parallel_time = time.time() - parallel_time

    set_thread_pool(None)
    out_image = merge_imgs(res)
    return parallel_time


def main(argv):
    # warmiters threads args...
    warmiters = int(argv[0])
    threads = int(argv[1])
    stripes, w, h = int(argv[2]), int(argv[3]), int(argv[4])

    print "params (iters, threads, s, w, h):", warmiters, threads, stripes, w, h

    print "do warmup:"
    for i in range(3):
        print "iter", i, "time:", run(threads, stripes, w, h)

    print "turn off jitting"
    import gc
    turn_jitting_off()
    print "do", warmiters, "real iters:"
    times = []
    for i in range(warmiters):
        gc.collect()
        times.append(run(threads, stripes, w, h))
    print "warmiters:", times

if __name__ == '__main__':
    main(sys.argv[1:])

# if __name__ == '__main__':
#     image = run(int(sys.argv[1]), int(sys.argv[2]))
#     #save_to_file(out_image)
#     save_img(out_image)
