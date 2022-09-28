# Bangor2022

## 🎞️ Stimuli

The zip folder [IndividualStimuli.zip](task/stimuli/IndividualStimuli.zip) contains the stimuli files used for this study. The stimuli set consists of short video files intended to represent social gestures. For each of the $16$ gestures, $4$ videos exist from different actors ($2$ women, $2$ robots), resulting in a total of $68$ video files. More detailed information can be found in [GesturesIndividualStimuli.xlsx](task/stimuli/GesturesIndividualStimuli.xlsx) in the sheet " ". 

$4$ of the stimuli files were omitted either because the representation of the gesture was not meaningful enough or simply because there was no congruent partner for this gesture. More details about the pairings of gestures can be found in [GesturesIndividualStimuli.xlsx](task/stimuli/GesturesIndividualStimuli.xlsx) in the sheet " ". 

### Stimuli creation

We then edited the remaining video files in [Kdenlive](https://kdenlive.org/) so that the on and off times of the various gestures are roughly the same for the different actors. Here it is important to mention that the edited videos need to be exported with a video codec that allows an alpha channel, otherwise the new videos will not be transparent. Therefore, we created the following custom render preset to export the edited videos: 

```
f=mov vcodec=prores_ks qscale=%quality acodec=pcm_s16le vprofile=4444 vendor=apl0
pix_fmt=yuva444p10le mlt_image_format=rgba vf= unpremultiply=inplace=1
```

 (for a tutorial on how to create render presets see https://docs.kdenlive.org/en/exporting/render.html#create-custom-render-presets)

Next, the videos are cropped and resized so that the highest point of the first frame (the actor's head) in the resized video is 740 pixels high. The width of the resized video is calculated according to the new height, ensuring that the height-to-width ratio remains the same. This all happens automatically when you run the [crop_and_resize.py](task/stimuli/crop_and_resize.py) script. 

With the remaining script [create_dyads.py](task/stimuli/create_dayds.py) the final dyad stimuli files can be created. 

According to the pairings, two gestures are combined and arranged on a gray, $1920 \times 1080$ pixel background. For a uniform distance we calculate the center of the bounding box around the actor in the first frame and position both video files in the new composition so that their "head centers" are $400$ pixels apart. This means that the "head center" of the left gesture is at $660$ pixels on the y-axis and the "head center" of the left gesture is at $1260$ pixels. Both gestures have an additional margin of $170$ pixels to the bottom. Furthermore, both videos are adjusted to a uniform length of $3$ seconds and the right gesture is mirrored so that both actors are looking at each other. This way we end up with $192$ dyad stimuli files. 

In order to run our scripts, you first have to install FFmpeg, which is a software utility for transcoding multimedia files (you can download various builds from their website https://ffmpeg.org/). To install it on Ubuntu, enter the following command:

```
sudo apt install ffmpeg
```

Then install the required python modules from requirements.txt:

```
pip install -r requirements.txt
```

Next, you need to navigate to the directory with the [IndividualStimuliCutted.zip](task/stimuli/IndividualStimuliCutted.zip) file inside and extract it there. If the `unzip` command isn't already installed on your system, run:

```  
sudo apt-get install unzip
```

Otherwise you can simply do:

```
cd task/stimuli
unzip IndividualStimuliCutted.zip
```

Now you can create the dyad files by running:

```
python3 crop_and_resize.py
python3 create_dyads.py
```

