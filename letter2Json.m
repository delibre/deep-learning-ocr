function letter2Json(letters, fileName)


    fileID = fopen(fileName,'w');
    fprintf(fileID, jsonencode(letters));
    fclose(fileID);

end