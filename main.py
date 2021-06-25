import glob
import os
import shutil

ImageDir = 'Images'
TempDir = 'imageTemp'
VideoDir = 'out'
ImagesPerSecond = 3


def copyfolder():
    if not os.path.exists(TempDir):
        print("+ Copying Images")
        shutil.copytree(ImageDir, TempDir)
        return True
    return False


def allimages():
    dates = {}
    files = glob.glob('{}/*.png'.format(ImageDir))
    for f in files:
        dates[os.path.basename(f)] = os.stat(f)[
            -1]  # https://stackoverflow.com/questions/237079/how-to-get-file-creation-modification-date-times-in-python
    print("+ Listing Images")
    return dates


def sortimages(screens):
    sort_images = sorted(screens.items(),
                         key=lambda x: x[1])  # https://careerkarma.com/blog/python-sort-a-dictionary-by-value/
    sorted_screens = {}
    for i in sort_images:
        sorted_screens[i[0]] = i[1]
    print("+ Sorting Images")
    return sorted_screens


def renamesimages(sorted_images):
    i = 0
    previouspath = os.getcwd()
    os.chdir(
        TempDir)  # https://stackoverflow.com/questions/22630841/os-rename-fails-to-rename-files-for-a-certain-directory
    for image in sorted_images:
        newname = str(i).zfill(10) + '.png'
        os.rename(image, newname)
        i += 1
        print("+ Renaming: ", image, " --> ", newname)
    os.chdir(previouspath)


def combinescreens():
    new_speed = 1 / ImagesPerSecond
    os.system(
        'ffmpeg -y -loglevel warning -thread_queue_size 10000 -r 1/{} -s 1920x1080 -framerate 60 -i "{}/%010d.png"  {}/{}.mp4'
            .format(new_speed, TempDir, VideoDir, VideoDir
                    ))
    print("+ Combining Images in to mp4")


def cleancopy():
    shutil.rmtree(TempDir)
    print("+ Removing copy")


def main():
    if copyfolder():
        renamesimages(sortimages(allimages()))
    combinescreens()
    cleancopy()
    print("+ " + os.path.basename(__file__) + " completed!")


if __name__ == "__main__":
    # execute only if run as a script
    main()
