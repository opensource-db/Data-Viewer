**#Viewing the Data Collector Output Using Data Viewer**

To analyze the contents of the Data Collector tarball in a more readable format, you can use the Data Viewer tool. 
This tool generates an HTML report from the tarball output, making it easy to review the collected data.

**#Steps to Build and Run the Data Viewer**

Build the Data Viewer binary using PyInstaller:

pyinstaller --onefile dataviewer.py

After the build completes, the binary will be located in the dist/ directory.

#Run the Data Viewer with the tarball file:

./dist/dataviewer <path-to-tarball-file>

