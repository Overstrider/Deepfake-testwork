from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import scipy, cv2, os, sys, argparse, audio
from os import listdir, path
import xml.etree.ElementTree as ET
import os
import json

"""Config"""
with open("config.json","r") as fp:
    conf = json.load(fp)


parser = argparse.ArgumentParser(description='Inference code to lip-sync videos in the wild using ttfs models')

parser.add_argument('--name', type=str, 
					help='Name of the video and audio', required=True)

parser.add_argument('--text', type=str, 
					help='Text to audio', required=True)

args = parser.parse_args()

text = args.text

import xml.etree.cElementTree as ET

root = ET.Element("speak", version="1.0", xmlns="https://www.w3.org/2001/10/synthesis", attrib={"xml:lang": "pt-BR"})
ET.SubElement(root, "voice", name="pt-BR-AntonioNeural").text = args.text

tree = ET.ElementTree(root)
tree.write("ssml.xml")

audio_name = args.name+".wav"

speech_config = SpeechConfig(subscription=conf["azure_sub"], region=conf["azure_region"])

azure_synt = str(conf["azure_synth_output"])
speech_config.set_speech_synthesis_output_format(SpeechSynthesisOutputFormat[azure_synt])
synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=None)

ssml_string = open("ssml.xml", "r").read()
result = synthesizer.speak_ssml_async(ssml_string).get()

stream = AudioDataStream(result)
audio_url = "content/audio/"+audio_name
stream.save_to_wav_file(audio_url)


actor_url = "content/ator.mp4"

video_name = args.name+ ".mp4"
video_url = "results/ttfs/" + video_name

os.system(f'python inference.py --checkpoint_path checkpoints/ttfs_gan.pth --face {actor_url} --audio {audio_url} --outfile {video_url}')