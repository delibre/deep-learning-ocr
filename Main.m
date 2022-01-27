clear; close all; clc;
fileName = input("Wpisz plik do przetworzenia: ");
im = imread(fileName);

letters = FindLetterImages(im);

letter2Json(letters, "temp.json")
!python3  letter_classification/appNoServer.py letter_classification/enhanced-custom-dataset-model.h5 temp.json
delete temp.json

