clear; close all; clc;
im = imread("learning/all.png");
im = imread("learning/Obraz-0003.png");
%im = imresize(im, [5000, 5050]);
letters = FindLetterImages(im);


% !python3 letter_classification/app.py letter_classification/custom-dataset-model.h5 &
%client(letters)


