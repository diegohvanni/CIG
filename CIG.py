#Content Inserts Generator (CIG) by Diego H. Vanni - dvanni@paypal.com

#Imports
import json
import os
import tkinter as tk

#GUI STARTS

window = tk.Tk()
canvas = tk.Canvas(window, width = 400, height = 300,  relief = 'raised')
canvas.pack()

title = tk.Label(window, text='Content Inserts Generator (CIG)')
title.config(font=('helvetica', 20))
canvas.create_window(200, 25, window=title)

fieldLabel0 = tk.Label(window, text='Enter the \"CONTENT\" ticket number:')
fieldLabel0.config(font=('helvetica', 10))
canvas.create_window(100, 100, window=fieldLabel0)

entry1 = tk.Entry (window)
canvas.create_window(100, 120, window=entry1)

fieldLabel2 = tk.Label(window, text='Enter path for \"translation-l10n\" folder: ')
fieldLabel2.config(font=('helvetica', 10))
canvas.create_window(100, 150, window=fieldLabel2)

entry2 = tk.Entry (window)
canvas.create_window(100, 170, window=entry2)

signature = tk.Label(window, text='by Diego H. Vanni - dvanni@paypal.com')
signature.config(font=('helvetica', 10))
canvas.create_window(300, 290, window=signature)

# GUI ENDS

#defining "cig" function
def cig():

    ticketNumber = entry1.get() #getting Ticket Number from GUI
    URL = entry2.get() #getting Folder Path from GUI


#MAIN PROCESSING STARTS

    #creating output file using "UTF-8" encoding to avoid issues with special char
    o = open(URL+"/CONTENT - "+ticketNumber+" - DSQL.txt","w+", 1,"utf-8", "Save File Error!")

    #capturing folder structure for all available languages
    languages = {}
    langs = []
    for (dirpath, dirnames, filenames) in os.walk(URL+'/translation_delivery'):
        for d in dirnames:
            languages[d] = os.path.join(d)

    #converting dictionary onto array for iteration
    langs = list(languages.values())[1:len(languages)]


#Processing English

    data = {} #defining Empty Dictionary Object

    #parsing from file with exception
    try:
        with open(URL+"/en_source/hw_translation_file.json") as e:
            data = json.load(e)
    except ValueError:
        o.write("Bad JSON for: en")

    #declaring/setting single use variables
    totalKeys = len(data['content']) #get total keys
    walletNumber = data.get("walletNumber") #get walletNumber
    channel = data.get("channel") #get channel

    #iterating through all available keys on english file
    for x in range(totalKeys):
        if data['content'][x]['type'] == "Message_Body":
            html = 1 #is "message_body"
        else:
            html = 0 #is NOT "message_body"

        if data['content'][x]['description'] == "":
            desc = "null" #description is null/empty
        else:
            desc = "'"+data['content'][x]['description']+"'" #description is not null/empty

        #composing and writing output to file
        o.write("REPLACE INTO content_translations (keyName, walletNumber, type, status, description, channel, locale, content, fileContent, fileExtension, htmlEmailMessageType, serviceCallerIdentificationId, creationDate, latUpdated, version, migratedContent, migratedNonSecureContent, legacyUrls) VALUES ("
                +"'"+data['content'][x]['keyName']+"',"
                +str(walletNumber)+","
                +"'"+data['content'][x]['type']+"',"
                +"'"+"ENABLED"+"',"
                +desc+","
                +"'"+channel+"',"
                +"'en',"
                +"'"+data['content'][x]['content']+"',"
                +"null,"
                +"null,"
                +str(html)+","
                +str(0)+","
                +"now()"+","
                +"now(),"
                +"1,"
                +"null,"
                +"null,"
                +"null"
                +");\n\n")



#Processing additional Languages

    #iterating through all a additional language folders available
    for l in range(len(langs)):
        data = {} #defining Empty Dictionary Object

        #parsing from file with exception
        try:
            with open(URL+"/translation_delivery/"+langs[l]+"/hw_translation_file.json") as g:
                data = json.load(g)
        except ValueError:
            o.write("Bad JSON for:"+langs[l])

        #declaring/setting single use variables
        totalKeys = len(data['content']) #get total keys
        walletNumber = data.get("walletNumber") #get walletNumber
        channel = data.get("channel") #get channel

        #iterating through all available keys on additional english files
        for y in range(totalKeys):
            if data['content'][y]['type'] == "Message_Body":
                html = 1 #is "message_body"
            else:
                html = 0 #is NOT "message_body"

            if data['content'][y]['description'] == "":
                desc = "null" #description is null/empty
            else:
                desc = "'"+data['content'][y]['description']+"'" #description is not null/empty
            #composing and writing output to file
            o.write("REPLACE INTO content_translations (keyName, walletNumber, type, status, description, channel, locale, content, fileContent, fileExtension, htmlEmailMessageType, serviceCallerIdentificationId, creationDate, latUpdated, version, migratedContent, migratedNonSecureContent, legacyUrls) VALUES ("
                    +"'"+data['content'][y]['keyName']+"',"
                    +str(walletNumber)+","
                    +"'"+data['content'][y]['type']+"',"
                    +"'"+"ENABLED"+"',"
                    +desc+","
                    +"'"+channel+"',"
                    +"'"+langs[l]+"',"
                    +"'"+data['content'][y]['content']+"',"
                    +"null,"
                    +"null,"
                    +str(html)+","
                    +str(0)+","
                    +"now()"+","
                    +"now(),"
                    +"1,"
                    +"null,"
                    +"null,"
                    +"null"
                    +");\n\n")


    #throwing completion message to the GUI
    conclusionLabel = tk.Label(window, text='Done!')
    conclusionLabel.config(font=('helvetica', 10))
    canvas.create_window(200, 270, window=conclusionLabel)

    #closing output file
    o.close()

#declaring GUI button + action
button = tk.Button(text='Generate Stripts!', command=cig, bg='brown', fg='white', font=('helvetica', 10, 'bold'))
canvas.create_window(200, 250, window=button)

window.mainloop()