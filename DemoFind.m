clear; close all; clc;
im = imread("learning/Obraz-0002.png");
%im = imresize(im, [5000, 5050]);
letters = FindLetterImages(im);
