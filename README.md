# Bangor2022

[[_TOC_]]

## :clapper: Stimuli

The stimuli used for this study were created from another set of stimuli that consist of videos in which either a single human or robotic actor performs a social gesture. There are $2$ women (*f01*, *f02*), $2$ men (*m01*, *m02*) and $2$ robots (*Pepper*, *Nao*) featured in this stimuli set. Additionally, there are $17$ different gestures in this set, for which at least one video per actor is available. For further information, refer to the sheet *"singles_all_gesture_files"* and *"singles_relevant_gesture_files"* in [AllStimuliFiles.xlsx](task/stimuli/AllStimuliFiles.xlsx). 

However, only $8$ of these gestures were actually used to design the interactions. They were selected based on meaningful representation across all actors and the availability of a congruent gesture for pairing. More on the pairing of the gestures in a [later section](#dyad-stimuli). In addition, $2$ actors were discarded: *Nao*, because the execution of his gestures was partly too rigid and hectic, and *m01*, because his proportions were not appropriate after he and the robots were scaled to the same size.

The remaining video files were then edited in [Kdenlive](https://kdenlive.org/) so that the on and off times of the various gestures were roughly the same for the different actors. Here it is important to mention that the edited videos need to be exported with a video codec that allows an alpha channel, otherwise the newly created videos will not be transparent. Therefore, the following custom render preset was created in order to export the edited videos: 

```shell
f=mov vcodec=prores_ks qscale=%quality acodec=pcm_s16le vprofile=4444 vendor=apl0
pix_fmt=yuva444p10le mlt_image_format=rgba vf= unpremultiply=inplace=1
```

 (for a tutorial on how to create render presets see https://docs.kdenlive.org/en/exporting/render.html#create-custom-render-presets)

The edited videos can be found in the zip folder [IndividualStimuliCutted.zip](task/stimuli/IndividualStimuliCutted.zip). These videos were then cropped and resized so that the highest point of the first frame (the actor's head) in the resized video was 740 pixels high. The width of the resized video was calculated according to the new height, ensuring that the height-to-width ratio remains the same. This all happens automatically when you run the [crop_and_resize.py](task/stimuli/crop_and_resize.py) script.  More on that later. 

## Dyad stimuli

The stimuli set used for this study consists of $384$ unique short video clips ($3$s) intended to represent dyadic social interactions.  Each clip shows two actors performing a predefined pair of gestures that represent a social interaction. 

Dyad stimuli depicted two actors engaging in one of 3 *interactive scenarios*: *Arguing* (i.e. both actors engaging in an angry/frustrated confrontation), *celebrating* (i.e. both actors celebrating together, excitedly), and *laughing* (i.e. both actors were laughing together, or at each other). 

The scenarios were chosen such that the intentions, emotions, and valence information conveyed by both individuals in a given scenario were always similar (e.g. angry/frustrated) rather than contrasting (e.g. angry/sad). This ensured that successful classification of the different scenarios was not driven by systematic differences in intentional, emotional, or valence content *between* interactors. Therefore, these scenarios represented three interactive scenarios that were intended to be easily distinguishable.

2 positive and 2 negative scenarios

social gestures. 

For each of the $16$ gestures, $4$ videos exist from different actors ($2$ women, $2$ robots), resulting in a total of $68$ video files. More detailed information can be found in [GesturesIndividualStimuli.xlsx](task/stimuli/GesturesIndividualStimuli.xlsx) in the sheet " ". 

$4$ of the stimuli files were omitted either because the representation of the gesture was not meaningful enough or simply because there was no congruent partner for this gesture. More details about the pairings of gestures can be found in [GesturesIndividualStimuli.xlsx](task/stimuli/GesturesIndividualStimuli.xlsx) in the sheet " ". 

### Stimuli creation

With the remaining script [create_dyads.py](task/stimuli/create_dayds.py) the final dyad stimuli files can be created. 

According to the pairings, two gestures are combined and arranged on a gray, $1920 \times 1080$ pixel background. For a uniform distance we calculate the center of the bounding box around the actor in the first frame and position both video files in the new composition so that their "head centers" are $400$ pixels apart. This means that the "head center" of the left gesture is at $660$ pixels on the y-axis and the "head center" of the left gesture is at $1260$ pixels. Both gestures have an additional margin of $170$ pixels to the bottom. Furthermore, both videos are adjusted to a uniform length of $3$ seconds and the right gesture is mirrored so that both actors are looking at each other. This way we end up with $192$ dyad stimuli files. 

In order to run our scripts, you first have to install FFmpeg, which is a software utility for transcoding multimedia files (you can download various builds from their website https://ffmpeg.org/). To install it on Ubuntu, enter the following command:

```shell
sudo apt install ffmpeg
```

Then install the required python modules from requirements.txt:

```shell
pip install -r requirements.txt
```

Next, you need to navigate to the directory with the [IndividualStimuliCutted.zip](task/stimuli/IndividualStimuliCutted.zip) file inside and extract it there. If the `unzip` command isn't already installed on your system, run:

```  shell
sudo apt-get install unzip
```

Otherwise you can simply do:

```shell
cd task/stimuli
unzip IndividualStimuliCutted.zip
```

Now you can create the dyad files by running:

```shell
python3 crop_and_resize.py
python3 create_dyads.py
```

## :microscope: Experiment design

```shell
./optseq2 --ntp 228 --tr 2 --psdwin 0 10 1 --ev 1G_HH 3 32 --ev 1G_HR 3 32 --ev 2G_SAME_HH 3 16 --ev 2G_SAME_HR 3 16 --ev 2G_DIFF_HH 3 16 --ev 2G_DIFF_HR 3 16 --ev Catch 3 8 --evc 0 0 0.5 0.5 -0.5 -0.5 0 --focb 100 --nsearch 1000000 --nkeep 24 --o OptSeqRun
```

