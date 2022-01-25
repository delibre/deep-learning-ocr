function letter2Json(letters, fileName)


    fileID = fopen(fileName,'w');
    fprintf(fileID, mps.json.encode(letters));
    fclose(fileID);

end