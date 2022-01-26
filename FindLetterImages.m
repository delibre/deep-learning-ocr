function letters = FindLetterImages(im)

    % wstępna obróbka obrazu
    im = double(im);
    im = 1 - (im-min(im, [], 'all')) / (max(im, [], 'all') - min(im, [], 'all'));
    im = rgb2gray(im);
    im = imfilter(im, [-1, -1, -1; -1, 9, -1; -1, -1, -1]/3);
    im(im<0)=0;
    im(im>1)=1;
    originalIm = im;

    % binaryzacja
    binary = imbinarize(im, 'adaptive', 'Sensitivity', 0.5);
    im = imbinarize(im .* binary, 0.1);
    im = bwmorph(im, 'clean');
    clear binary
    
    % usuwanie marginesów
    mask = ones(size(im));
    mask(1, :) = 0;
    mask(end, :) = 0;
    mask(:, 1) = 0;
    mask(:, end) = 0;
    im = im & imerode(mask, ones(15));
    clear mask;
    
    % wykrywanie linii
    mask = zeros(15);
    for i=1:15
        mask(7, i) = 1;
    end
    lineMask = imdilate(im, mask);
    lineMask = imdilate(lineMask, ones(3));
    %lineMask = imclose(lineMask, ones(5));
    lineMask = imdilate(lineMask, mask);
    lineMask = imclose(lineMask, mask);
    l = bwlabel(lineMask')';
    count = max(l, [], 'all');
    lineCount = 1;
    linesTemp = cell([count, 1]);
    area = sum(lineMask, 'all');
    
    for i=1:count
        if sum(l==i, 'all') > area/64
            linesTemp{lineCount} = (l==i) & im;
            lineCount = lineCount + 1;
        end
    end
    lineCount = lineCount-1;
    lines = cell([lineCount, 1]);
    originalLines = cell([lineCount, 1]);
    for i=1:lineCount
        cropped = CropImages(linesTemp{i}, originalIm, 10);
        s = size(cropped{1});
        destHeight = 300;
        s(2) = floor(s(2)/s(1)*destHeight);
        s(1) = destHeight;
        lines{i} = imresize(cropped{1}, s);
        originalLines{i} = imresize(cropped{2}, s);
    end
    clear linesTemp linesMask;
    
    letters = cell([lineCount, 1]);
     
    mask = mask';
    
    % wykrywanie znaków
    for i=1:lineCount
        %disp(string(i) + '/' + string(lineCount)); %%%%%%%%%%%%%%%%%%%%%%
        letterMask = originalLines{i} .* lines{i};
        wordMask = bwlabel(imdilate(letterMask, [mask', mask', mask', mask', mask']));
        wordIndex = 2;

         lineSize = size(letterMask);
         for k=1:lineSize(2)
            if sum(letterMask(:, k)) <= 0.8
                letterMask(:, k) = 0;
            end
         end

         letterMask = imbinarize(letterMask, 'adaptive');
         letterMask = imclose(letterMask, ones(2));

         lineSize = size(letterMask);
         for k=1:lineSize(2)
            if sum(letterMask(:, k)) <= 1
                letterMask(:, k) = 0;
            end
         end

%         imwrite(lines{i}, 'testspace/' + string(i) + '.png'); %%%%%%%%%%%%%
%         imwrite(letterMask, 'testspace/mask' + string(i) + '.png'); %%%%%%%%%%%%%
     
        area = sum(lines{i}, 'all');
        l = bwlabel(letterMask);
        count = max(l, [], 'all');
        letterCount = 1;
    
        tempLettersInLine = cell([letterCount, 1]);
        for j=1:count
            if sum(l==j, 'all') > area/200
                cropped = CropImages(imdilate(imdilate(l==j, ones(5)), mask) & lines{i}, originalLines{i}, 5);
                currentWordIndex = round(mean(wordMask(l==j), 'all'));
                if currentWordIndex ~= wordIndex
                    wordIndex = currentWordIndex;
                    tempLettersInLine{letterCount} = zeros([32, 16]);                 
                    letterCount = letterCount + 1;
                end
                tempLettersInLine{letterCount} = imresize(cropped{2}, [32, 16]);
                tempLettersInLine{letterCount} = tempLettersInLine{letterCount} / max(tempLettersInLine{letterCount}, [], 'all');
                letterCount = letterCount + 1;
            end
        end
        letterCount = letterCount -1;
        lettersInLine = cell([letterCount, 1]);
        %disp('Found: ' + string(letterCount)) %%%%%%%%%%%%%%%%%
        for j=1:letterCount
            lettersInLine{j} = tempLettersInLine{j};
           % imwrite(lettersInLine{j}, 'testspace/letters/' + string(i) + "x" + string(j) + '.png'); %%%%%%%%%%%%%
        end
        clear tempLettersInLine;
        letters{i} = lettersInLine;
    end 

end