
# copy files
import shutil
shutil.copyfile('sourceDir/sourceFile', 'destDir/destFile')

# copy files to network location on Windows without mapping a drive
import shutil
shutil.copyfile(networkPath + 'sourceDir/sourceFile', 'destDir/destFile')
