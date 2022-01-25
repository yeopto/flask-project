#!/usr/bin/env python
# -*- coding: utf-8 -*-

def count_fruits(target):  
  fruits = ['사과','배','배','감','수박','귤','딸기','사과','배','수박']
  count = 0
  for fruits in fruits:
    if fruits == target:
      count += 1
  return count

subak_count = count_fruits('수박')
print(subak_count)