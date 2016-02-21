amblyo
======

Written by Parke Loyd 2015 November

This module is intended for visual training to improve the acuity of amblyopic eyes. It might also be helpful for those hoping to improve their scores on standard eye exams. Note that I make absolutely no claims that this works. I hope it does. At the moment, it consists simply of games where the user guesses the letters presented on the screen and then size or contrast is adjusted according to whether the user guessed a sufficient fraction of the letters correctly.

The letters are displayed in exactly the same way as on the standard Snellen eye exam chart, in groups of 9 letters (same as the chart). If you use this software and you ever see me at a bar, you should buy me endless beers to thank me for the hours of excruciatingly boring labor I put in to writing the code to replicate these letters. There is no Snellen font -- the letters are very specialized to the application of measuring visual acuity. Thankfully, Snellen charts use only 9 letters of the alphabet (C, D, E, F, L, O, P, T, Z). Note that many modern eye charts deviate from this, including that used by the FAA medical exams and probably the DMV as well. 

You can play two versions of the size and contrast games. One is just a timed game (timed only because I have to force myself to play it for x minutes). In this version, the game shows you what letters you got right and wrong so you can guess again and hopefully better learn how to make out the fuzzy blobs. The other version simply adjusts the size/contrast round by round in smaller and smaller steps until it has honed in on your limiting size/contrast to the desired fractional precision that you specify.

When you import the module, you get the chance to set your screen size and resolution. These settings must be correct for the module to get the true sizes of the letters correct. I couldn't figure out any easy way to get this information directly from the system, so you will just have to look it up and measure it for your screen. If you don't care about the letter sizes being accurate, you needn't worry about it. If you want to use this program to actually get a good sense of what you would score on the Snellen exam (e.g. 20/30), then your settings must be accurate. Also, note that you must also place your screen 20 feet distant (you'll need a remote keyboard) in order for the 20/## scale to be accurate.

Use the `snellen_game` and `snellen_contrast_game` functions to play these games. Here is what my daily sessions of two timed games and two "exams" looks like:

```python
import amblyo
amblyo.snellen_contrast_game(start_contrast=10.0, size=20.0, p=7./9., timer=8)
amblyo.snellen_contrast_game(start_contrast=10.0, size=20.0, p=7./9., exam=0.15)
amblyo.snellen_game(startsize=11.0, p=7./9, timer=8)
amblyo.snellen_game(startsize=11.0, p=7./9, exam=0.02)
```

You will need the numpy and matplotlib packages to use this module. 

I should really make a web app version of this in javascript so that it can be more widely shared. But instead I keep going climbing/backpacking/beer drinking instead. That probably won't change. Apologies.

