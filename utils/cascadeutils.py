import os

def generate_negative_description_file():
    try:
        # Open output file for writing, will overwrite all existing data
        with open('neg.txt', 'w') as f:
            # Loop over all filenames
            for filename in os.listdir('../images/negative'):
                f.write('images/negative/' + filename + '\n')
        print("File 'neg.txt' generated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
generate_negative_description_file()
            #from cascadeutils import generate_negative_description_file
            #generate_negative_description_file
            #E:/yuh/opencv/build/x64/vc15/bin/opencv_annotation.exe --annotations=pos.txt --images=images/positive/
            #E:/yuh/opencv/build/x64/vc15/bin/opencv_createsamples.exe -info pos.txt -w 24 -h 24 -num 1000 -vec pos.vec
            #E:/yuh/opencv/build/x64/vc15/bin/opencv_createsamples.exe -vec pos.vec -info pos.txt -num

#E:/yuh/opencv/build/x64/vc15/bin/opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -w 24 -h 24 -precalcValBufSize 6000 -precalcIdxBufSize 6000 -numPos 600 -numNeg 1200 -numStages 12 -maxFalseAlarmRate 0.4 -minHitRate 0.999
    #E:/yuh/opencv/build/x64/vc15/bin/opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -w 24 -h 24 -precalcValBufSize 6000 -precalcIdxBufSize 6000 -numPos 600 -numNeg 1200 -numStages 12 -maxFalseAlarmRate 0.3 -minHitRate 0.995 -verbose 1
