import sys, getopt
import tarfile
import os
import webbrowser

def unpack(source):
    try: 
        tar = tarfile.open(source)
        tar.extractall()
        tar.close()
    except:
        sys.exit("Unable to extract the tarball. Contact your system administrator for assistance")

def create_tree(rootdir, tabcount=5, tree_text=''):
    path_text = tree_text
    first_file = ''
    try: 
        current_path = rootdir
        file_list = []
        folder_list = []
        with os.scandir(rootdir) as it:
            for entry in it:
                if not entry.name.startswith('.') and entry.is_dir():
                    folder_list.append(entry.name)              
                          
                if not entry.name.startswith('.') and entry.is_file():
                    file_list.append(entry.name)
                    
            it.close()

        for entry in folder_list:
            subdir_path = os.path.join(rootdir, entry)
            path_text = path_text + '\t'*tabcount + '<li><span class="folder">' + entry + '</span>\n'
            path_text = path_text + '\t'*(tabcount+1) + '<ul class="nested">\n'
            path_text = create_tree(subdir_path, tabcount+2, path_text)[0]
                 
        for entry in file_list:
            file_path = os.path.join(rootdir, entry)
            if (file_path.count(os.sep) == 1) and (file_list[0] == entry):
                path_text = path_text + '\t'*tabcount + '<li><span class="file currentfile" data-path="' + file_path + '">' + entry + '</span></li>\n'
                first_file = file_path
            else:
                path_text = path_text + '\t'*tabcount + '<li><span class="file" data-path="' + file_path + '">' + entry + '</span></li>\n'
 
        path_text = path_text + '\t'*(tabcount-1) + '</ul>\n'
        path_text = path_text + '\t'*(tabcount-2) + '</li>\n'
        return ([path_text, first_file])                        
    except:
        sys.exit("Unable to open folder {}. Contact your system administrator for assistance".format(rootdir))        


def get_styles(tabcount=3):
    css_text = ''
    css_text = css_text + '\t'*tabcount + 'html, body {margin: 0px;}\n'
    css_text = css_text + '\t'*tabcount + 'iframe {border: none; margin: none; padding: none;}\n'
    css_text = css_text + '\t'*tabcount + '.row {display: flex; margin: none; padding: none;}\n'
    css_text = css_text + '\t'*tabcount + '.titlerow {height: 5%; width: 100%; float: right; background-color: navy; color: white; text-align: center; padding: 5px; padding-top: 15px; line-height: 1.2; position: fixed;}\n'
    css_text = css_text + '\t'*tabcount + '.column {float: left;}\n'
    css_text = css_text + '\t'*tabcount + '.left {width: 20%; height: 92%; margin-top: 3.77%; background: aqua; position: fixed; padding: 2px; line-height: 1.5; border-right: 6px solid green; overflow: auto;}\n'
    css_text = css_text + '\t'*tabcount + '.right {width: 80%; height: 90%; margin-top: 3.77%; margin-left: 20%; background: silver; padding: 10px 5px 5px 10px; margin-bottom: 2px; overflow: auto;}\n'
    css_text = css_text + '\t'*tabcount + 'ul, #dcFileList {list-style-type: none;}\n'
    css_text = css_text + '\t'*tabcount + '#dcFileList {margin: 0; padding: 2px;}\n'
    css_text = css_text + '\t'*tabcount + '.folder {cursor: pointer; user-select: none; padding-left: 2px;}\n'
    css_text = css_text + '\t'*tabcount + '.folder::before {content: "\\1F4C1"; color: black; display: inline-block; margin-right: 3px;}\n'
    css_text = css_text + '\t'*tabcount + '.folder-open::before {content: "\\1F4C2"; color: black; display: inline-block; margin-right: 3px;}\n'
    css_text = css_text + '\t'*tabcount + '.nested {display: none;}\n'
    css_text = css_text + '\t'*tabcount + '.active {display: block;}\n'
    css_text = css_text + '\t'*tabcount + 'li ul{margin: 0; padding: 5px 15px;}\n'
    css_text = css_text + '\t'*tabcount + '.file {cursor: pointer; user-select: none;}\n'
    css_text = css_text + '\t'*tabcount + '.file::before {content: "\\1F5CE"; color: black; display: inline-block; margin-right: 3px;}\n'
    css_text = css_text + '\t'*tabcount + '.currentfile {font-weight: bold;}\n'
    return (css_text)


def get_scripts(tabcount=3):
    script_text = ''
    script_text = script_text + '\t'*tabcount + "var toggler = document.getElementsByClassName('folder');\n"
    script_text = script_text + '\t'*tabcount + "var i;\n"
    script_text = script_text + '\t'*tabcount + "for (i = 0; i < toggler.length; i++) {\n"
    script_text = script_text + '\t'*tabcount + ' '*4 + "toggler[i].addEventListener('click', function() {\n"
    script_text = script_text + '\t'*tabcount + ' '*8 + "this.parentElement.querySelector('.nested').classList.toggle('active');\n"
    script_text = script_text + '\t'*tabcount + ' '*8 + "this.classList.toggle('folder-open');\n"
    script_text = script_text + '\t'*tabcount + ' '*4 + "});\n"
    script_text = script_text + '\t'*tabcount + "}\n"
    script_text = script_text + '\t'*tabcount + "var fileswitcher = document.getElementsByClassName('file');\n"
    script_text = script_text + '\t'*tabcount + "var i;\n"
    script_text = script_text + '\t'*tabcount + "for (i = 0; i < fileswitcher.length; i++) {\n"
    script_text = script_text + '\t'*tabcount + ' '*4 + "fileswitcher[i].addEventListener('click', function() {\n"
    script_text = script_text + '\t'*tabcount + ' '*8 + "document.getElementById('if1').setAttribute('src', this.getAttribute('data-path'));\n"
    script_text = script_text + '\t'*tabcount + ' '*8 + "const collection = document.getElementsByClassName('currentfile');\n"
    script_text = script_text + '\t'*tabcount + ' '*8 + "for (let i = 0; i < collection.length; i++) {\n"
    script_text = script_text + '\t'*tabcount + ' '*12 + "collection[i].classList.remove('currentfile');\n"
    script_text = script_text + '\t'*tabcount + ' '*8 + "}\n"
    script_text = script_text + '\t'*tabcount + ' '*8 + "this.classList.add('currentfile');\n"
    script_text = script_text + '\t'*tabcount + ' '*4 + "});\n"
    script_text = script_text + '\t'*tabcount + "}\n"
    return(script_text)


def create_html(tar_file, target):
    target_html = target + ".html"
    with open(target_html, "w") as hfile:
        hfile.write('<!DOCTYPE html>\n')
        hfile.write('<html>\n')
        hfile.write('\t<head>\n')
        hfile.write('\t\t<title>Data Collector</title>\n')
        hfile.write('\t\t<link rel="stylesheet" href="styles.css">\n')
        hfile.write('\t\t<style>\n')
        css_text = get_styles(3)
        hfile.write(css_text)
        hfile.write('\t\t</style>\n')   
        hfile.write('\t</head>\n')
        hfile.write('\t<body>\n')
        hfile.write('\t\t<div class="titlerow">{}</div>\n'.format(tar_file))
        hfile.write('\t\t<div class="row">\n')
        hfile.write('\t\t\t<div class="column left">\n')
        hfile.write('\t\t\t\t<p></p>\n')
        hfile.write('\t\t\t\t<p></p>\n')
        hfile.write('\t\t\t\t<ul id="dcFileList">\n')
        retlist = create_tree(target, 5, '')
        hfile.write(retlist[0])
        hfile.write('\t\t\t\t</ul>\n')
        hfile.write('\t\t\t</div>\n')
        hfile.write('\t\t\t<div class="column right">\n')
        hfile.write('\t\t\t\t<iframe id="if1" src="{}" width="100%" height="710px"></iframe>\n'.format(retlist[1]))
        hfile.write('\t\t\t</div>\n')
        hfile.write('\t\t</div>\n')
        hfile.write('\t\t<script>\n')
        script_text = get_scripts(3)
        hfile.write(script_text)
        hfile.write('\t\t</script>\n')
        hfile.write('\t</body>\n')
        hfile.write('</html>\n')
         
def main(argv):
    print("Generating HTML Output ...")
    folder_name = '-'.join((argv[0].split('-'))[0:-1])
    unpack(argv[0])    
    create_html(argv[0], folder_name)
    print("Done ...")
    webbrowser.open(folder_name + ".html", new=2) 

if __name__ == "__main__":
   main(sys.argv[1:])