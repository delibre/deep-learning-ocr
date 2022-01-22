function cropped = CropImage(im, bounds)
    
    s = size(im);

    for left = 1:s(1)
        if sum(im(left, :), 'all') ~= 0
            break;
        end
    end

    for right = s(1):-1:1
        if sum(im(right, :), 'all') ~= 0
            break;
        end
    end

    for top = 1:s(2)
        if sum(im(:, top), 'all') ~= 0
            break;
        end
    end

    for bottom = s(2):-1:1
        if sum(im(:, bottom), 'all') ~= 0
            break;
        end
    end

    cropped = imcrop(im, [top-bounds, left-bounds, bottom-top+2*bounds, right-left+2*bounds]);

end