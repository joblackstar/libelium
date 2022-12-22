# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 17:05:14 2020

@author: jonas
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 16:13:24 2020

@author: BRWU
"""
#l'import de sys est uniquement pour gérer les fichiers d'entrée et de sortie
import sys

#imports pour gérer le format de la feuille, et l'unité de mesure
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

#gére le style du document et des paragraphes
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle

#gérer une police unicode pour les caractères chinois.
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
pdfmetrics.registerFont(UnicodeCIDFont('STSong-Light'))

def pdf(filein,fileout):
    txt = open(filein, 'r').read() #on ouvre le fichier en lecture 
    docpdf = SimpleDocTemplate(fileout, # on defini les caracteristiques de notre documents
                               pagesize = A4)
    style = getSampleStyleSheet()
    style.add(ParagraphStyle(name='Chinese',
                             fontName='STSong-Light',
                             fontSize=12,
                             leading=14),
                             wordWrap = 'CJK')


#nous lisons ligne à ligne notre texte et nous alimentons une liste, 
#liste qui sera à son tour lue pour constituer le document pdf en applicant le style défini plus haut.
    story = []
    paragraphs = txt.split("\n")
    for para in paragraphs:
        story.append(Paragraph(para, style["Chinese"]))
        story.append(Spacer(0, cm * .3))
    docpdf.build(story)

if __name__ == "__main__":
    
        filein = 'test.pdf'
        fileout = 'sortie.pdf'
        pdf(filein,fileout)