"""
Copyright (C) 2019 NVIDIA Corporation.  All rights reserved.
Licensed under the CC BY-NC-SA 4.0 license (https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode).
"""

import datetime
import dominate
from dominate.tags import *
import os
import glob
import subprocess

class HTML:
    def __init__(self, web_dir, title, refresh=0):
        if web_dir.endswith('.html'):
            web_dir, html_name = os.path.split(web_dir)
        else:
            web_dir, html_name = web_dir, 'index.html'
        self.title = title
        self.web_dir = web_dir
        self.html_name = html_name

        self.img_dir = self.web_dir #os.path.join(self.web_dir, 'images')
        if len(self.web_dir) > 0 and not os.path.exists(self.web_dir):
            os.makedirs(self.web_dir)
        if len(self.web_dir) > 0 and not os.path.exists(self.img_dir):
            os.makedirs(self.img_dir)

        self.doc = dominate.document(title=title)
        with self.doc:
            1 #h1(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
        if refresh > 0:
            with self.doc.head:
                meta(http_equiv="refresh", content=str(refresh))

    def get_image_dir(self):
        return self.img_dir

    def add_header(self, str):
        with self.doc:
            h3(str)
    
    def add_header_large(self, str):
        with self.doc:
            h1(str)
    def add_link(self, link):                    
        with self.doc:
            with a(href=link):
                p(link)


    def add_table(self, border=1):
        self.t = table(border=border, style="table-layout: fixed;")
        self.doc.add(self.t)

    def add_images(self, ims, txts, links, width=192):
        self.add_table()
        with self.t:
            with tr():
                for im, txt, link in zip(ims, txts, links):
                    with td(style="word-wrap: break-word;", halign="center", valign="top"):
                        with p():
                            with a(href=os.path.join('../', link)):
                                img(style="width:%dpx" % width, src=os.path.join('../', im))
                            br()
                            p(txt) #.encode('utf-8'))

    def save(self):
        html_file = os.path.join(self.web_dir, self.html_name)
        f = open(html_file, 'wt')
        f.write(self.doc.render())
        f.close()




def run(data_root, data_list, prompt_list, token, num_entity):
    output_name = "hsinping_outputs"
    model = ["stable-diffusion","dreambooth","custom-diffusion"]
    

    html = HTML(f'outputs/{token}.html', f'{token}')
    prompt = [p.strip() for p in open(prompt_list).readlines()]
    name = [p.split('|')[1] for p in open(data_list).readlines()]
    for entity in range(num_entity):
        html.add_header_large(f'{token}/{entity:03} {name[entity]}')

        ref = glob.glob(f'{data_root}/{entity:03}/*')
        ims = []
        txts = []
        links = []
        for n in range(len(ref)):
            ims.append(ref[n])
            txts.append(f'ref #{n}')
            links.append(ref[n])
        html.add_images(ims, txts, links)

        for n in range(len(prompt)):
            html.add_header(prompt[n].replace('<sks>', name[entity]))
            ims = []
            txts = []
            links = []
            for m in model:
                o = glob.glob(f"../{m}/{output_name}/{token}/{entity:03}_{n:02}_*")[:2]
                for l in range(2):
                    ims.append(o[l])
                    txts.append(f'{m} #{l}')
                    links.append(o[l])
            html.add_images(ims, txts, links)
    html.save()
    #subprocess.call(f"cd outputs; pandoc -V geometry:margin=0.2in -V linestretch=0.8 {token}.html -o {token}.pdf", shell=True)


data_root = "../select_set/oxford_flower_eval"
data_list = "../select_set/oxford_flower_list"
prompt_list = "../select_set/oxford_flower_prompt"
token = "flower"
num_entity = 5
run(data_root, data_list, prompt_list, token, num_entity)


data_root = "../select_set/gldv2_eval"
data_list = "../select_set/gldv2_list"
prompt_list = "../select_set/gldv2_prompt"
token = "landmark"
num_entity = 5
run(data_root, data_list, prompt_list, token, num_entity)


data_root = "../select_set/inaturalist_insect_eval"
data_list = "../select_set/inaturalist_insect_list"
prompt_list = "../select_set/inaturalist_insect_prompt"
token = "insect"
num_entity = 5
run(data_root, data_list, prompt_list, token, num_entity)


data_root = "../select_set/inaturalist_plant_eval"
data_list = "../select_set/inaturalist_plant_list"
prompt_list = "../select_set/inaturalist_plant_prompt"
token = "plant"
num_entity = 5
run(data_root, data_list, prompt_list, token, num_entity)


data_root = "../select_set/car196_eval"
data_list = "../select_set/car196_list"
prompt_list = "../select_set/car196_prompt"
token = "car"
num_entity = 5
run(data_root, data_list, prompt_list, token, num_entity)


data_root = "../select_set/food101_eval"
data_list = "../select_set/food101_list"
prompt_list = "../select_set/food101_prompt"
token = "dish"
num_entity = 5
run(data_root, data_list, prompt_list, token, num_entity)


data_root = "../select_set/aircraft_eval"
data_list = "../select_set/aircraft_list"
prompt_list = "../select_set/aircraft_prompt"
token = "aircraft"
num_entity = 5
run(data_root, data_list, prompt_list, token, num_entity)


data_root = "../select_set/sports100_eval"
data_list = "../select_set/sports100_list"
prompt_list = "../select_set/sports100_prompt"
token = "sport"
num_entity = 5
run(data_root, data_list, prompt_list, token, num_entity)
