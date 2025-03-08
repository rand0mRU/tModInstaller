import wget, tkinter, requests, os, zipfile, os.path, os, shutil, glob, subprocess
from tkinter import *
from tkinter import ttk, messagebox, filedialog
with open("path.txt","r") as file:
    terraria_path = file.readline()
    print(terraria_path)
def setPath():
    global terraria_path
    terraria_path = filedialog.askdirectory(title="Path to Terraria...")
    if terraria_path!="" and os.path.isfile(terraria_path+"/Terraria.exe"): pass
    else: 
        messagebox.showwarning("Set path","Please, set correct path to terraria.exe")
        setPath()
    with open("path.txt","w") as file:
        file.write(terraria_path)
        print(terraria_path)


    
def openFolder():
    path = os.path.realpath(terraria_path+"/../")
    os.startfile(path)

if terraria_path!="" and os.path.isfile(terraria_path+"/Terraria.exe"): pass
else:
    messagebox.showinfo("Set path","Please, set path to terraria.exe")
    setPath()


def start():
    subprocess.call(f"{terraria_path}/../tModLoader_{box1.get()}/start-tModLoader.bat")

def startServer():
    subprocess.call(f"{terraria_path}/../tModLoader_{box1.get()}/start-tModLoaderServer.bat")

def remove():
    if messagebox.askyesno("Continue", f"Are you sure won to remove tModLoader {box1.get()}?"):
        try:
            shutil.rmtree(f"{terraria_path}/../tModLoader_{box1.get()}")
        except (FileNotFoundError, PermissionError) as err:
            messagebox.showerror("Error",err)
        else:
            messagebox.showinfo("Successfully",f"tModLoader {box1.get()} was removed!")
    else:
        messagebox.showerror("Remove failed","Remove failed: canceled by user")
    updateVersions()

def transfer():
    if box3.get()==box4.get(): messagebox.showwarning("Warning","Please select two different versions for porting")
    else:
        if os.path.isfile(f"{terraria_path}/../tModLoader_{box3.get()}/steam_appid.txt"):
            if os.path.isfile(terraria_path+f"/../tModLoader_{box4.get()}/steam_appid.txt"):
                
                with open(f"{terraria_path}/../tModLoader_{box3.get()}/steam_appid.txt","r") as file:
                    fold = file.readline()
                with open(f"{terraria_path}/../tModLoader_{box4.get()}/steam_appid.txt","r") as file:
                    fold1 = file.readline()

                allfiles = os.listdir(f"{terraria_path}/../tModLoader_{box3.get()}/steamapps/workshop/content/{fold}")
    
                # iterate on all files to move them to destination folder
                for f in allfiles:
                    src_path = os.path.join(f"{terraria_path}/../tModLoader_{box3.get()}/steamapps/workshop/content/{fold}", f)
                    dst_path = os.path.join(f"{terraria_path}/../tModLoader_{box4.get()}/steamapps/workshop/content/{fold1}", f)
                    try:
                        shutil.copytree(src_path, dst_path)
                    except PermissionError as err:
                        messagebox.showerror("Error",err)
                    except FileNotFoundError as err:
                        messagebox.showerror("Error",err)

                if allfiles==[]:
                    messagebox.showwarning("Warning",f"Mods in tModLoader {box3.get()} not found!")

                messagebox.showinfo("Successfully", f"Successfully made transfer from {box3.get()} into {box4.get()}!")

            else: 
                messagebox.showerror("Transfer failed",f"Transfer failed: tModLoader {box4.get()} are not initilazied! Go into the game to initialise it")
        else: 
            messagebox.showerror("Transfer failed",f"Transfer failed: tModLoader {box3.get()} are not initilazied! Go into the game to initialise it")

root = Tk()
root.title("tModInstaller")
root.geometry("600x175") 
releases_with_name = []
releases_url = f"https://api.github.com/repos/tModLoader/tModLoader/releases"
response = requests.get(releases_url)
releases = response.json()
for index, _ in enumerate(releases):
    if releases[index]['prerelease']:
        releases_with_name.append(f"{releases[index]['tag_name']} preview")
    else:
        releases_with_name.append(f"{releases[index]['tag_name']}")
# print(releases_with_name)

def download():
    for index, _ in enumerate(releases):
        if releases[index]['tag_name']==box.get().split(" ")[0]:
            release_index = index 
    if release_index is not None:
        install(releases, int(release_index))

def clearDir():
    try: shutil.rmtree("downloads")
    except FileNotFoundError: pass
    messagebox.showinfo("Successfully", "Successfully cleared downloads folder!")

lbl = ttk.Label(root,text="Download and install tModLoader").place(x=20,y=10)
box = ttk.Combobox(root,values=releases_with_name)
box.place(x=10,y=30)
box.current(0)
btn = ttk.Button(root,text="Install", command=download)
btn.place(x=160,y=29)
pgb = ttk.Progressbar(root, length=150, value=0)
pgb.place(x=245,y=30)
btnOpenFolder = ttk.Button(root,text="Open folder", command=openFolder)
btnOpenFolder.place(x=405,y=29)
btnClear = ttk.Button(root,text="Clear downloads", command=clearDir)
btnClear.place(x=490,y=29)

lbl1 = ttk.Label(root,text="Control tModLoader").place(x=20,y=60)
btn1 = ttk.Button(root,text="Start", command=start).place(x=160,y=79)
btn1 = ttk.Button(root,text="Run server", command=startServer).place(x=245,y=79)
btn2 = ttk.Button(root,text="Uninstall", command=remove).place(x=330,y=79)
box1 = ttk.Combobox(root,values=[])
box1.place(x=10,y=80)

lbl3 = ttk.Label(root,text="Transfer modifications").place(x=20,y=110)
lbl3_1 = ttk.Label(root,text="from").place(x=10,y=130)
box3 = ttk.Combobox(root,values=[])
box3.place(x=45,y=130)
lbl3_2 = ttk.Label(root,text="to").place(x=193,y=130)
box4 = ttk.Combobox(root,values=[])
box4.place(x=210,y=130)
btn3 = ttk.Button(root,text="Transfer", command=transfer)
btn3.place(x=360,y=129)


def updateVersions():
    versions = glob.glob(f"{terraria_path}/../tModLoader_*")
    versionsF = []
    for i in versions:
        versionsF.append(i.split("\\")[-1].split("tModLoader_")[-1])
    box1["values"] = versionsF
    box3["values"] = versionsF
    box4["values"] = versionsF
    try:
        box1.current(0)
        box3.current(0)
        box4.current(0)
    except:
        pass

updateVersions()

def install(releases, release_index):
    release = releases[release_index]
    assets = release.get('assets', [])

    asset = assets[1]

    download_url = asset.get('browser_download_url')
    if download_url:
        filename = download_url.split('/')[-1]
        download_path = f"./downloads/{release['tag_name']}"
        # print(download_path)
        pgb["value"] = 0

        os.makedirs(download_path, exist_ok=True)
        pgb["value"] = 10

        root.update_idletasks()
        # print(f"Downloading {release['tag_name']}...")
        print(wget.download(download_url, f"{download_path}/{filename}"))
        # print(" <|> Download complete!")
        pgb["value"] = 70

        root.update_idletasks()
        with zipfile.ZipFile(f"{download_path}/{filename}", 'r') as zip_ref:
            if release['prerelease']:
                zip_ref.extractall(f"{terraria_path}/../tModLoader_{release['tag_name']}-preview")
            else:
                zip_ref.extractall(f"{terraria_path}/../tModLoader_{release['tag_name']}")

        pgb["value"] = 100
        messagebox.showinfo("Installation completed",f"Succesfully installed tModLoader {release['tag_name']}!")
        pgb["value"] = 0

        updateVersions()

root.mainloop()