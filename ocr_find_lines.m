clc;    % Clear the command window.
close all;  % Close all figures (except those of imtool.)
clear;  % Erase all existing variables. Or clearvars if you want.
workspace;  % Make sure the workspace panel is showing.
format long g;
format compact;
fontSize = 20;
tic;
fullFileName = fullfile(pwd, 'learning/Obraz-0001.png'); % fullfile(pwd, 'Reagan_letter2Koch.png');

grayImage = imread(fullFileName);
% Get the dimensions of the image.
% numberOfColorBands should be = 1.
[rows, columns, numberOfColorBands] = size(grayImage);
if numberOfColorBands > 1
    % It's not really gray scale like we expected - it's color.
    % Convert it to gray scale by taking only the green channel.
    grayImage = grayImage(:, :, 2); % Take green channel.
end
% Display the original gray scale image.
subplot(2, 3, 1);
imshow(grayImage, []);
title('Original Grayscale Image', 'FontSize', fontSize, 'Interpreter', 'None');
axis on;

% Set up figure properties:
% Enlarge figure to full screen.
set(gcf, 'Units', 'Normalized', 'OuterPosition', [0 0 1 1]);
% Get rid of tool bar and pulldown menus that are along top of figure.
set(gcf, 'Toolbar', 'none', 'Menu', 'none');
% Give a name to the title bar.
set(gcf, 'Name', 'Demo by ImageAnalyst', 'NumberTitle', 'Off')

% Crop off the top part of the image to get rid of the emblem on the letter.
grayImage = grayImage(200:end,:);
[rows, columns, numberOfColorBands] = size(grayImage);

% Histogram the image.
thresholdValue = 200;
subplot(2, 3, 2);
histogram(grayImage);
grid on;
title('Histogram of Gray Scale Image', 'FontSize', fontSize, 'Interpreter', 'None');
hold on;
line([thresholdValue, thresholdValue], ylim, 'Color', 'r', 'LineWidth', 2);
hold off;

% Threshold the image
binaryImage = grayImage > thresholdValue;
subplot(2, 3, 2);
imshow(binaryImage);
title('Binary Image', 'FontSize', fontSize, 'Interpreter', 'None');
axis on;

% Sum the image horizontally.
verticalProfile = mean(binaryImage, 2);

subplot(2, 3, 3);
plot(verticalProfile, 'b-');
grid on;
xlabel('Line in image', 'FontSize', fontSize);
ylabel('Mean', 'FontSize', fontSize);
title('Vertical Profile', 'FontSize', fontSize, 'Interpreter', 'None');

% Create logical vector of what lines have text and which do not based on threshold.
rowsWithText = verticalProfile < 0.9;

% Find top and bottom line.
topLines = find(diff(rowsWithText) == 1);
bottomLines = find(diff(rowsWithText) == -1);

% Looping for extracting lines and then characters in the line.
for k = 1 : length(topLines)
    topRow = topLines(k);
    bottomRow = bottomLines(k);
    thisLine = binaryImage(topRow:bottomRow, :);
    % Show line over binary image.
    subplot(2, 3, 2);
    hold on;
    line([1, columns], [topRow, topRow], 'Color', 'r', 'LineWidth', 2);
    line([1, columns], [bottomRow, bottomRow], 'Color', 'r', 'LineWidth', 2);
    subplot(2, 3, 4);
    imshow(thisLine, []);
    axis on;
    caption = sprintf('Line %d of the text', k);
    title(caption, 'FontSize', fontSize, 'Interpreter', 'None');

    % Sum the segmented image vertically to find individual characters.
    horizontalProfile = sum(thisLine, 1);
    subplot(2, 3, 5);
    plot(horizontalProfile, 'b-');
    grid on;
    caption = sprintf('Horizontal Profile of Line %d of the text', k);
    title(caption, 'FontSize', fontSize, 'Interpreter', 'None');

    theThreshold = 0.9 * abs(topRow-bottomRow);
    columnWithText = horizontalProfile < theThreshold;
    leftCharacter = find(diff(columnWithText) == 1);
    rightCharacter = find(diff(columnWithText) == -1);
    if isempty(leftCharacter) || isempty(rightCharacter)
        continue;
    end
    promptMessage = sprintf('This is the image between rows %d and %d, inclusive.\nDo you want to find letters within this line,\nor Cancel to abort processing?', topRow, bottomRow);
    titleBarCaption = 'Continue?';
    button = questdlg(promptMessage, titleBarCaption, 'Yes', 'No', 'Cancel', 'No');
    if strcmpi(button, 'Cancel')
        return;
    elseif strcmpi(button, 'Yes')
        % Find individual characters
        subplot(2, 3, 6);
        numCharactersOnThisLine = length(leftCharacter);
        for m = 1 : numCharactersOnThisLine  % loop for segmenting each individual character
            leftColumn = leftCharacter(m);
            rightColumn = rightCharacter(m);
            thisCharacter = thisLine(:, leftColumn:rightColumn);
            imshow(thisCharacter, []);
            axis on;
            caption = sprintf('Character %d of %d of the text on line %d.', m, numCharactersOnThisLine, k);
            title(caption, 'FontSize', fontSize, 'Interpreter', 'None');
            promptMessage = sprintf('Do you want to find the next letter,\nor Cancel to abort processing?');
            titleBarCaption = 'Continue?';
            button = questdlg(promptMessage, titleBarCaption, 'Continue', 'Skip to next line', 'Continue');
            if strcmpi(button, 'Skip to next line')
                break;
            end
        end
    end

end

