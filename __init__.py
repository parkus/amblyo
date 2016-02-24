import matplotlib as _mpl
import matplotlib.pyplot as _plt
import numpy as _np
import random
import time

_plt.ion()
_text_ratio = 0.708 # ratio of capital letter height to font size for standard matplotlib font
_height_text_2020 = _np.pi/180.*(5./60.)*(20.*12.*72.) # height of text person with 20/20 vision can see in pts
_step_grow = 1.1
_step_shrink = 0.8

# get physical screen size
use_default = raw_input("Use default screen size of 15.4\" (standard size of 2015 Macbook Pro 15\")?")
if 'y' in use_default or '' == use_default:
    _diag_screen_in = 15.4
else:
    _diag_screen_in = float(raw_input("Enter screen size in inches: "))


use_default = raw_input("Use default screen size of 1440x900 (standard resolution of 2015 Macbook Pro 15\")?")
if 'y' in use_default or '' == use_default:
    _width_screen_pixels, _height_screen_pixels = 1440., 900.
else:
    res = raw_input("Enter screen resolution (pixels) as WxH: ")
    res = map(float, res.split('x'))
    _width_screen_pixels, _height_screen_pixels = map(float, res)
_ar = _height_screen_pixels/_width_screen_pixels # screen aspect ratio

# now derive other screen info
_width_screen_in = _np.sqrt(_diag_screen_in**2/(1 + _ar**2)) # screen width in
_height_screen_in = _ar * _width_screen_in
_dpi = _width_screen_pixels/_width_screen_in

# set matplotlib to use proper screen resolution
_mpl.rcParams['figure.dpi'] = _dpi

_optoalphabet = ['C', 'D', 'E', 'F', 'L', 'O', 'P', 'T', 'Z']


def _setup_figure():
    # set up a figure the size of the screen
    width_fig, height_fig = _width_screen_in - 1.0, _height_screen_in - 1.0
    fig = _plt.figure(figsize=[width_fig, height_fig], facecolor='w')
    ax = _plt.axes(position=[0.0,0.0,1.0,1.0])
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    raw_input('Please maximize the figure and resize the terminal so it takes up just a small portion at the top or ' \
              'bottom. Press enter when finished.')
    w, h = fig.get_figwidth()*72., fig.get_figheight()*72.
    ax.set_xlim(-w/2, w/2)
    ax.set_ylim(-h/2, h/2)
    ax.autoscale(enable=False)
    return fig, ax


def _optolet(letter, xy, size, color='k', bgcolor='w'):
    lw = size/5
    xy = _np.array(xy)

    def sqrs(xys_rel, cc, **kw):
        xys_rel = _np.array(xys_rel) - _np.array([[0.5, 0.5]]*len(xys_rel))
        patches = []
        for xy_rel in xys_rel:
            xy_abs = xy + xy_rel*lw
            patches.append(_mpl.patches.Rectangle(xy_abs, lw, lw, fc=cc, ec='none', **kw))
        return patches
    fgsqrs = lambda xys_rel: sqrs(xys_rel, color)
    bgsqrs = lambda xys_rel: sqrs(xys_rel, bgcolor, zorder=10)
    def relarc(xy_rel, w, h, **kw):
        xy_abs = xy + _np.array(xy_rel)*lw + _np.array([0,0.35])
        return _mpl.patches.Arc(xy_abs, w*lw, h*lw, color=color, lw=lw, **kw)

    if letter == 'C':
        patches = [relarc((0,0), 4, 4)] + fgsqrs(((2,1), (2,2))) + bgsqrs(((1,0),(2,0)))
    elif letter == 'D':
        patches = [relarc((0,0), 4, 4, theta1=-90, theta2=90)] + \
                   fgsqrs(((-1,-2), (-1,-1), (-1,0), (-1,1), (-1,2), (-2,-2), (-2,2), (-0.5,-2), (-0.5,2)))
    elif letter == 'E':
        patches = fgsqrs(((-2,-2), (-2,2), (-1,-2), (-1,-1), (-1,0), (-1,1), (-1,2), (0,-2), (1,-2), (2,-2), (2,-1),
                           (0,0), (0,2), (1,2), (2,2), (2,1)))
    elif letter == 'F':
        patches = fgsqrs(((-2,-2), (-2,2), (-1,-2), (-1,-1), (-1,0), (-1,1), (-1,2), (0,-2), (0,0), (0,2), (1,2),
                           (2,2), (2,1)))
    elif letter == 'L':
        patches = fgsqrs(((-2,-2), (-2,2), (-1,-2), (-1,-1), (-1,0), (-1,1), (-1,2), (0,-2), (1,-2), (2,-2), (2,-1),
                           (0,2)))
    elif letter == 'O':
        patches = [relarc((0,0), 4, 4)]
    elif letter == 'P':
        patches = [relarc((1,1), 2, 2, theta1=-90, theta2=90)] + \
                   fgsqrs(((-2,-2), (-2,2), (-1,-2), (-1,-1), (-1,0), (-1,1), (-1,2), (0,-2), (0,0), (0,2), (0.5,0),
                           (0.5,2)))
    elif letter == 'T':
        patches = fgsqrs(((-1,-2), (1,-2), (0,-2), (0,-1), (0,0), (0,1), (0,2), (0,-2), (0,2), (-2,2), (-2,1),
                          (-1,2), (1,2), (2,2), (2,1)))
    elif letter == 'Z':
        s = _np.sqrt(2)
        vertices = _np.array(((-2.5,-1.5), (3.5-s,2.5), (2.5,1.5), (-3.5+s,-2.5))) * lw + xy[_np.newaxis, :]
        patches = [_mpl.patches.Polygon(vertices, fill=True, ec='none', fc=color)] \
                   + fgsqrs(((-2,-2), (-1,-2), (0,-2), (1,-2), (2,-2), (2,-1), (-2,2), (-1,2), (0,2), (1,2), (2,2),
                             (-2,1)))
    else:
        raise Exception("Letter not in optotype alphabet.")

    return patches


def _get_letter_pos(size, n):
    centers = _np.arange(-n, (n+1))*size
    return centers[1::2]


def _optostrip(size, letters, ax, color='k', bgcolor='w'):
    centers = _get_letter_pos(size, len(letters))

    ax.cla()
    for center, letter in zip(centers, letters):
        patches = _optolet(letter, [center, 0.0], size, color, bgcolor)
        [ax.add_patch(patch) for patch in patches]
    _plt.draw()


def _highlight_correct(size, correct, ax):
    centers = _get_letter_pos(size, len(correct))
    xlim, ylim = ax.get_xlim(), ax.get_ylim()

    off = size*2
    for center, cor in zip(centers, correct):
        color = 'g' if cor else 'r'
        ax.hlines([-off, off], center-size/2.0, center+size/2.0, color=color, lw=size/2.0)
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    _plt.draw()


def _get_n(size, fig):
    nmax = (fig.get_figwidth() * 72. / size + 1) // 2
    return int(nmax) if nmax < 9 else 9


def _acuity2size(acuity_str):
    dist = float(acuity_str.split('/')[1])
    ratio = dist/20.
    size = _height_text_2020 * ratio
    return size


def _size2actuity(points):
    ratio = points/_height_text_2020
    dist = ratio * 20.
    return '20/{:.2g}'.format(dist)


def _test_letters(letters):
    userstr = raw_input('Enter you guess at the letters (or "q" to end game): ')

    if userstr.lower() == 'q':
        raise Exception('Game ended at user request.')

    correct = [letter == uletter.upper() for letter, uletter in zip(letters, userstr)]
    n_correct = sum(correct)
    return correct, n_correct


def _draw_test(fig, ax, size, color, bgcolor, exam, p):
    n = _get_n(size, fig)
    letters = [random.choice(_optoalphabet) for _ in range(n)]
    _optostrip(size, letters, ax, color=color, bgcolor=bgcolor)

    correct, n_correct = _test_letters(letters)
    passed = n_correct/float(len(letters)) >= p

    if not exam and len(correct) > 0:
        while n_correct < len(letters) and len(correct) > 0:
            _highlight_correct(size, correct, ax)
            correct, n_correct = _test_letters(letters)
    return passed


def snellen_game(startsize='20/40', timer=15, p=7./9, exam=False):
    """
    Play game that simulates eye exam.

    Play by typing the letters you think you see on the screen and hitting enter. Incorrect guesses will be
    highlghted in red, correct ones in green. You can continue guessing the letters until you get them all correct or
    hit enter to progress to the next round. Size is adjusted according to whether you guessed greater than a fraction
    p of the letters correctly on the first try. The game runs until the timer expires or user types 'q'.

    In exam mode, correct and incorrect letters are not highlighted. Instead, each guess begins a new round. The game
    is continued until the size of text at which the user can correctly guess, on average, a fraction p of the
    letters has been narrowed down to a relative precision specified by the exam keyword.

    :param startsize: starting size either as visual measurement (e.g. 20/60) or size in points
    :param timer: timer length in min
    :param p: fraction you must get correct for size of next line to be reduced
    :param exam: the relative precision desired for an exam. initiates exam instead of timer mode.
    :return: none
    """

    size_step = startsize/10.

    fig, ax = _setup_figure()

    tstart = time.time()

    msmt_type = 'visual' if type(startsize) is str else 'points'
    size = _acuity2size(startsize) if msmt_type == 'visual' else float(startsize)
    _passed = True
    record = []
    while True:

        if exam:
            relative_accuracy = size_step/size
            if relative_accuracy < exam:
                print '\nResolution measured to be {} to a precision of {:.2g}%.'.format(sizestr, 100*exam)
                break
        elif (time.time() - tstart)/60. > timer:
            print "\nOut of time."
            break

        sizestr = _size2actuity(size) if msmt_type == 'visual' else '{:.3g}'.format(size)
        print 'size = {}'.format(sizestr)
        passed = _draw_test(fig, ax, size, color='k', bgcolor='w', exam=exam, p=p)

        size = size - size_step if passed else size + size_step
        size_step = size_step * _step_grow if passed == _passed else size_step * _step_shrink
        _passed = passed

    n = 10
    avg = sum(record[-n:])/float(n)

    _plt.close(fig)


def snellen_contrast_game(start_contrast=32, size=10.0, timer=15, p=7./9, exam=False):
    """
    Practice contrast sensitivity using Snellen letters with gray letters on gray background.

    Play by typing the letters you think you see on the screen and hitting enter. Incorrect guesses will be
    highlghted in red, correct ones in green. You can continue guessing the letters until you get them all correct or
    hit enter to progress to the next round. Contrast is adjusted according to whether you guessed greater than a
    fraction  p of the letters correctly on the first try. The game runs until the timer expires or user types 'q'.

    In exam mode, correct and incorrect letters are not highlighted. Instead, each guess begins a new round. The game
    is continued until the contrast at which the user can correctly guess, on average, a fraction p of the letters has
    been narrowed down to a relative precision specified by the exam keyword.

    :param start_contrast: contrast of letters from background, 0-256
    :param size: text size in points (1/72 in.)
    :param timer: timer for length of game
    :param p: fraction of letters user must guess correctly to pass a given line
    :param exam: the relative precision desired for an exam. initiates exam instead of timer mode.
    :return: none
    """

    contrast_step = start_contrast/2
    contrast = start_contrast

    fig, ax = _setup_figure()

    tstart = time.time()

    _passed = True
    record = []
    while True:
        record.append(contrast)

        if exam:
            precision = float(contrast_step)/contrast
            if precision < exam or contrast_step == 1:
                print ('\nContrast threshold measured to be {}/256 to a precision of {:.2g}%.'
                       ''.format(contrast, 100*precision))
                break
        elif (time.time() - tstart)/60. > timer:
            print "\nOut of time."
            break

        ax.cla()
        n = _get_n(size, fig)
        brighter = contrast/2
        darker = contrast - brighter
        color = [(256/2 - brighter)/256.0]*3 + [1.0]
        bgcolor = [(256/2 + darker)/256.0]*3 + [1.0]
        ax.set_axis_bgcolor(bgcolor)

        print 'contrast = {}/256'.format(contrast)
        passed = _draw_test(fig, ax, size, color=color, bgcolor=bgcolor, exam=exam, p=p)

        _contrast = contrast
        istep = round(contrast_step)

        contrast = contrast - istep if passed else contrast + istep
        if contrast > 256: contrast = 256
        if contrast < 1: contrast = 1
        contrast_step = contrast_step*_step_grow if passed == _passed else contrast_step*_step_shrink
        if contrast_step < 1: contrast_step = 1


        if passed and _passed and _contrast == 1:
            print "Smallest posible contrast reached. Reducing text size instead and resetting start contrast."
            contrast = start_contrast
            contrast_step = 256/2
            size *= 0.8

        _passed = passed

    n = 10
    avg = sum(record[-n:])/float(n)
    print '\nAverage of last {} measurements = {:.3g}'.format(n, avg)

    _plt.close(fig)