__author__ = 'Gusev Ivan'

from lxml import etree
import re
import numpy as np
import pandas as pd


tree = etree.parse('banks_train/bank (1).xml')
root = tree.getroot()
