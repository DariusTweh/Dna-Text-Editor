import tkinter as tk 
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk
import tkinter.messagebox
import datetime
#MENU BAR CLASS
class MenuBar(tk.Menu):
    
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        #CREATE FILE MENU 
        fileMenu = tk.Menu(self, tearoff=False) 
        self.currentTime= datetime.datetime.now()
        self.DnaSequence =""#holds original Dna sequence for protein
        self.RnaReady = False
        self.sequence1=""
        self.sequence2=""
        self.sequenceNumber=0
        self.CopyText =""
        self.PasteText =""
        self.CutText=""
        self.filepath="" #FILEPPATH TO BE ACCESSED FROM DIFFERENT FUNCTIONS IN MENUBAR
        #VARIABLE THATS TRANSCRIBE/TRANSLATE"N"= NEW FILE OR "C" TRANSCRIBE/TRASNLATE CURRENT FILE,
        CommandType ="x"
        #TRANSCRIBE/TRANSLATE MENU DROP DOWN TO TRANSCRIBE TEXT FILES
        TranscribeMenu = tk.Menu(self,tearoff=False)
        TranslateMenu = tk.Menu(self,tearoff=False)
        CompareSeq= tk.Menu(self,tearoff=False)
        RepeatSearch=tk.Menu(self,tearoff=False)
        Edit=tk.Menu(self,tearoff=False)
        #CASCADE CREATES A LABEL THAT DROPS DOWN A LIST OF ACTIONS MENU = MENUTAB IT BELONGS TOO
        self.add_cascade(label="File",underline=0, menu=fileMenu)
        self.add_cascade(label="Edit",underline=1,menu=Edit)
        self.add_cascade(label="Transcribe",underline=0,menu=TranscribeMenu)
        self.add_cascade(label="Translate",underline=1,menu=TranslateMenu)
        self.add_cascade(label="Compare sequences",underline=1,menu=CompareSeq)
        self.add_cascade(label="Repeats",underline=1,menu=RepeatSearch)
    #FILEMENU SPECIFIES THE PARENT MENU.ADD_COMMAND = DROP DOWN ACTIONS FOR THAT MENU
        fileMenu.add_command(label="Open File",underline=1,command=lambda: self.OpenFile(parent))
        fileMenu.add_command(label="Save as....",underline=1,command=lambda: self.SaveFile(parent))
        fileMenu.add_command(label="Save",underline=1,command=lambda: self.Save(parent))
        fileMenu.add_command(label="Exit", underline=1, command=lambda: parent.quit())
        Edit.add_command(label="Copy",underline=1,command=lambda: self.EditFunctions(parent,CommandType="C"))
        Edit.add_command(label="Paste",underline=1,command=lambda: self.EditFunctions(parent,CommandType="P"))
        Edit.add_command(label="Cut",underline=1,command=lambda: self.EditFunctions(parent,CommandType="CT"))
        TranscribeMenu.add_command(label="Transcribe Existing File...",underline=1,command=lambda: self.Transcribe(parent,CommandType="N"))
        TranscribeMenu.add_command(label="Current Text",underline=1,command=lambda: self.Transcribe(parent,CommandType="C"))
        TranscribeMenu.add_command(label="Reverse Transcription",underline=1,command=lambda: self.Transcribe(parent,CommandType="D"))
        TranscribeMenu.add_command(label="Transcribe Highlighted Nucleotides",underline=1,command=lambda: self.Transcribe(parent,CommandType="S"))
        TranslateMenu.add_command(label="Translate Exsiting File...",underline=1,command=lambda: self.Translation(parent,CommandType="N"))
        TranslateMenu.add_command(label="Current Text",underline=1,command=lambda: self.Translation(parent,CommandType="C"))
        TranslateMenu.add_command(label="Reverse Translation",underline=1,command=lambda: self.Translation(parent,CommandType="F"))
        CompareSeq.add_command(label="Compare 2 DNA Files..",underline=1,command=lambda: self.CompFiles(parent,CommandType='F'))
        CompareSeq.add_command(label="Highlight sequences to compare",underline=1,command=lambda: self.CompHighlight(parent,CommandType='H'))
        RepeatSearch.add_command(label="Find repeats within current sequence",underline=1,command=lambda: self.RepeatSeq(parent,CommandType="R"))
        RepeatSearch.add_command(label="Remove highlight from repeats",underline=1,command=lambda: self.RepeatSeq(parent,CommandType="D"))
#OPENS A FILE AND DISPLAYS CONTEXT IN TEXT BOX 
    def RepeatSeq(self,parent,CommandType):
        parent.TextBox.tag_config("Repeats",foreground="red",underline=1)
        if CommandType=='R': 
            repeatfound= False
            text = parent.TextBox.get("1.0",tk.END).splitlines()
            for line in text:
                    repeats=""
                    
                    for i in range(0,len(line)-2,3):
                            
                                if line[i:i+3]==line[i+3:i+6]:
                                
                                    repeats+=line[i:i+3]
                                    repeatfound = True
                                    
                                elif line[i+3:i+6]=="" and line[i:i+3]==line[i-3:i] or line[i+3:i+6]!=line[i:i+3] and line[i:i+3]==line[i-3:i]:
                                        repeats+=line[i:i+3]
                                        repeatfound=True
                                                
                                        startIndex = parent.TextBox.search(repeats,'1.0',END)
                                        while startIndex:

                                            offset = '+%dc'%len(repeats)
                                            EndIndex = startIndex+offset
                                            parent.TextBox.tag_add("Repeats",startIndex,EndIndex)
                                            startIndex = parent.TextBox.search(repeats,EndIndex ,END)
                                        repeats=""
                            
                                else:
                                    continue         
        elif CommandType =="D":
             parent.TextBox.tag_delete("Repeats")
    def OpenFile(self,parent):
            """Open a file for editing."""
            self.filepath = askopenfilename(
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if not self.filepath:
                return
            parent.TextBox.delete("1.0", tk.END)
            with open(self.filepath, mode="r", encoding="utf-8") as input_file:
                text = input_file.read()
                parent.TextBox.insert(tk.END, text)
                parent.title(f"DNA Editor - {self.filepath}")
#TRANSCRIBE DNA IN TEXT EDITOR TO RNA 
    def Transcribe(self,parent,CommandType):
    #IF N THEN OPEN A FILE FROM DESIRED DIRECTORY 
        if CommandType =="N":
            self.filepath = askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
            if not self.filepath:
                return
            with open(self.filepath,mode="r") as reader:
                line = reader.read()
                line = line.replace("T","U")
                parent.TextBox.delete("1.0",tk.END)
                parent.TextBox.insert(tk.END, line)
                parent.title(f"DNA Editor - {self.filepath} - {self.currentTime}") 
    #IF C TRANSCRIBE CURRENT FILE  
        elif CommandType =="C":
                    text = parent.TextBox.get("1.0",tk.END).splitlines()
                    self.DnaSequence = text
                    parent.TextBox.delete("1.0",tk.END)
                    if text[-1] =='':
                        text.pop()
                    
                    for line in text:
                        seq =line.upper()
                        seq =seq.replace("T","U")
                        parent.TextBox.insert(tk.END,seq+"\n")
                    parent.title(f"DNA Editor - {self.filepath} - {self.currentTime}")     
        #this converts current RNA sequence in text to DNA
        elif CommandType =='D':
                    text = parent.TextBox.get("1.0", tk.END).splitlines()
                    line = parent.TextBox.get("1.0", tk.END)
                    if text[-1]=='':
                        text.pop()
                    #this checks to see if theres any U bases in sequence if none then print error messagge
                    if 'U' not in line:
                            tkinter.messagebox.showinfo(title="Reverse transcription error",message="This sequence has not been converted to RNA\nPlease convert to RNA first then covert to DNA")
                    else:
                        parent.TextBox.delete("1.0",tk.END)
                        for i in text:
                            i = i.replace("U","T")
                            parent.TextBox.insert(tk.END,i+"\n")
        #this allows user to only transcribe a certain part on sequence by highlighting
        elif CommandType=="S":
            try:
                startIndex = parent.TextBox.index("sel.first")
                endIndex = parent.TextBox.index("sel.last")
                selection  = parent.TextBox.get(tk.SEL_FIRST,tk.SEL_LAST)
                selection = selection.upper()
                rna = selection.replace("T","U")
                parent.TextBox.delete(startIndex,endIndex)
                parent.TextBox.insert(startIndex,rna)
            except:
                pass
    def Translation(self,parent,CommandType):
        #table containing proteins
        rna_codon = {"UUU" : "F", "CUU" : "L", "AUU" : "I", "GUU" : "V",
                        "UUC" : "F", "CUC" : "L", "AUC" : "I", "GUC" : "V",
                        "UUA" : "L", "CUA" : "L", "AUA" : "I", "GUA" : "V",
                        "UUG" : "L", "CUG" : "L", "AUG" : "M", "GUG" : "V",
                        "UCU" : "S", "CCU" : "P", "ACU" : "T", "GCU" : "A",
                        "UCC" : "S", "CCC" : "P", "ACC" : "T", "GCC" : "A",
                        "UCA" : "S", "CCA" : "P", "ACA" : "T", "GCA" : "A",
                        "UCG" : "S", "CCG" : "P", "ACG" : "T", "GCG" : "A",
                        "UAU" : "Y", "CAU" : "H", "AAU" : "N", "GAU" : "D",
                        "UAC" : "Y", "CAC" : "H", "AAC" : "N", "GAC" : "D",
                        "UAA" : "STOP", "CAA" : "Q", "AAA" : "K", "GAA" : "E",
                        "UAG" : "STOP", "CAG" : "Q", "AAG" : "K", "GAG" : "E",
                        "UGU" : "C", "CGU" : "R", "AGU" : "S", "GGU" : "G",
                        "UGC" : "C", "CGC" : "R", "AGC" : "S", "GGC" : "G",
                        "UGA" : "STOP", "CGA" : "R", "AGA" : "R", "GGA" : "G",
                        "UGG" : "W", "CGG" : "R", "AGG" : "R", "GGG" : "G" 
                        }
        #if N open a new file to translate into protein
        if CommandType == "N":
            parent.TextBox.delete("1.0",tk.END)
            self.filepath = askopenfilename(
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if not self.filepath:
                return
            #reads first line of file
            with open(self.filepath,mode="r") as reader:
                protein =""
                sequence = reader.read()
            parent.TextBox.insert(tk.END,sequence)
            text = parent.TextBox.get("1.0",tk.END).splitlines()
            if text[-1]=='':
                text.pop()
            self.DnaSequence=text
            ##checks to see if its an RNA sequence
            if 'T' in sequence:
                tkinter.messagebox.showinfo(title="Translation error",message="This sequence has not been converted to RNA\nPlease convert to RNA first then convert back")
            else:
                parent.TextBox.delete("1.0",tk.END)
                #this translate codon into protein 
                for line in text:
                    for i in range(0,len(line),3):
                        codon = line[i:i+3]
                        try:
                            protein_fam = rna_codon[codon]
                            protein+=protein_fam       
                        except KeyError:
                            protein+=codon
                    parent.TextBox.insert(tk.END,protein+"\n")    
                    protein =""
        #translate current file if current file isnt saved then
        # it asks you to save file before translating      
        elif CommandType =="C":
            protein =""
            text = parent.TextBox.get("1.0",tk.END).splitlines()
            line =parent.TextBox.get("1.0",tk.END)
            line = line.upper() 
            self.DnaSequence=text
            if text[-1]=='':
                text.pop()
            ##checks to see if current sequence is an RNA sequence
            
            if "T" in line:
                self.RnaReady=False
            else:
                self.RnaReady=True
            ##prints out error box if current sequence is not RNAc
            if not self.RnaReady:
                tkinter.messagebox.showinfo(title="Translation error",message="This sequence has not been converted to RNA\nPlease convert to RNA first")
            else:
                parent.TextBox.delete("1.0",tk.END)
                for seq in text:
                    for i in range(0,len(seq),3):
                        codon = seq[i:i+3]
                        try:
                            protein+=rna_codon[codon]
                        except KeyError:
                            protein+=codon
                    parent.TextBox.insert(tk.END,protein+"\n")
                    protein=""           
        #this deletes current translation and replaces with DNA before 
        elif CommandType=="F":
            if self.DnaSequence =="":
                tkinter.messagebox.showwarning(title="Reverse Translation Error",message="Theres no previously translated RNA\n Transcribe RNA into protein before conversion")
            else:
                parent.TextBox.delete("1.0",tk.END)
                for line in self.DnaSequence:
                    parent.TextBox.insert(tk.END,line+"\n")               
   #saves file as new 
    def SaveFile(self,parent):
                    """Save the current file as a new file."""
                    filepath = asksaveasfilename(
                        defaultextension=".txt",
                        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
                    )
                    if not filepath:
                        return
                    with open(filepath, mode="w", encoding="utf-8") as output_file:
                        text = parent.TextBox.get("1.0", tk.END)
                        output_file.write(text)
                    parent.title(f"DNA Editor - {self.filepath} - {self.currentTime}")
    #get percent difference between 2 sequences
    def seq_diff(self,seq1,seq2):
        seqe_diff=0
        diff=0
        total=(len(seq1)+len(seq2))/2
        if len(seq1)>len(seq2):
            add_difference=abs(len(seq2)-len(seq1))
            size = len(seq2)
            for i in range(size):
                if seq2[i]!=seq1[i]:
                    diff+=1
            diff+=add_difference 
        elif len(seq1)<len(seq2):
            add_difference= abs(len(seq2)-len(seq1))
            size = len(seq1)
            for i in range(0,size):
                if seq1[i]!=seq2[i]:
                    diff+=1
            diff+=add_difference
                    
        else:
            size = len(seq1)
            for i in range(0,size):
                if seq1[i]!=seq2[i]:
                    diff+=1
        
        seqe_diff = round(((diff/total)*100),3)
        return seqe_diff
    #compare sequnces between 2 text files containing sequences
    def CompFiles(self,parent,CommandType='F'):
        sequence1=""
        sequence2=""
        for i in range(2):
            if i ==0:
                self.filepath = askopenfilename(
                    filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
                )
                with open(self.filepath,mode="r") as reader:
                    sequence1 = reader.read()
            else:
                self.filepath = askopenfilename(
                    filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
                )
                with open(self.filepath,mode="r") as reader:
                    sequence2 = reader.read()
        if self.seq_diff(sequence1,sequence2)==0:
            parent.CompareSeqDiff.config(text=f"The sequences are 100% match")
        else:
            parent.CompareSeqDiff.config(text=f"The difference between sequences is {self.seq_diff(sequence1,sequence2)}%")
    
            #read first file into first sequence
    #compare 2 highlighted sequences
    def CompHighlight(self,parent,CommandType='H'):        
        try:
            if self.sequenceNumber ==0:
                self.sequenceNumber+=1
                self.sequence1 = parent.TextBox.get(tk.SEL_FIRST,tk.SEL_LAST)
                tkinter.messagebox.showinfo(title="Comparing Highlighted Sequence",message="Highlight second strand to compare")
            elif self.sequenceNumber==1:
                self.sequenceNumber=0
                self.sequence2=parent.TextBox.get(tk.SEL_FIRST,tk.SEL_LAST)
                if self.seq_diff(self.sequence1,self.sequence2)==0:
                    parent.CompareSeqDiff.config(text=f"The sequences are 100% match")
                else:
                    parent.CompareSeqDiff.config(text=f"The difference between sequences is {self.seq_diff(self.sequence1,self.sequence2)}%")
                tkinter.messagebox.showinfo(title="Comparing Highlighted Sequence",message="complete :)")
        except:
            tkinter.messagebox.showinfo(title="Comparing Highlighted Sequence",message="You must highlight a portion of the sequence first")        
    #saves current file if current file doesnt exist it ask to save file
    def Save(self,parent):
      
        if  not self.filepath:
            self.filepath = asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            )
            with open(self.filepath, mode="w", encoding="utf-8") as output_file:
                text = parent.TextBox.get("1.0", tk.END)
                output_file.write(text)
            parent.title(f"DNA Editor - {self.filepath}- Saved - {self.currentTime}")
        else:
            with open(self.filepath, mode="w", encoding="utf-8") as output_file:
                text = parent.TextBox.get("1.0", tk.END)
                output_file.write(text)
            parent.title(f"DNA Editor - {self.filepath}- Saved - {self.currentTime}")
            print(self.filepath)
    def EditFunctions(self,parent,CommandType):
        if CommandType =="C":
            self.CopyText = parent.TextBox.get(SEL_FIRST,SEL_LAST)
        elif CommandType =="P":
            self.PasteText=self.CopyText
            parent.TextBox.insert(tk.END,self.PasteText)
        elif CommandType=="CT":
            parent.TextBox.delete(SEL_FIRST,SEL_LAST)
#Stats Frame
class StatsFrame(ttk.LabelFrame):
    def __init__(self,parent):
        ttk.LabelFrame.__init__(self,parent)
        #variables that count the nucleotides
        style=ttk.Style(parent)
        style.theme_use("clam")
        self.A_base=0
        self.C_base=0
        self.T_base=0
        self.G_base=0
        self.U_base=0
        CommandType=""
        #config frame size
        self.config(width=200,height=500,text="Stats")
        #creating section labels 
        self.statslabel = ttk.Label(self,text="Nucleotide Count")
        self.CG_AT_Content = ttk.Label(self,text="CG/AT content")
        #create seperator for section labels
        Ncount_sep = ttk.Separator(self,orient=HORIZONTAL)
        GC_sep = ttk.Separator(self,orient=HORIZONTAL)
        #update that update nucleotide count
        self.StatsUpdate = ttk.Button(self,text="Update total sequence",command=lambda: self.NucleotideCount(parent,CommandType="T"))
        self.SelctUpdate = ttk.Button(self,text="Update Highlighted sequence",command=lambda: self.NucleotideCount(parent,CommandType="S"))
        #labels that print nucletide and GC/AT count
        self.aCount = ttk.Label(self,text=f"A base: {self.A_base}")
        self.CCount = ttk.Label(self,text=f"C base: {self.C_base}")
        self.TCount = ttk.Label(self,text=f"T base: {self.T_base}") 
        self.GCount = ttk.Label(self,text=f"G base: {self.G_base}")
        self.UCount = ttk.Label(self,text=f"U base: {self.U_base}")
        self.totalNuc = ttk.Label(self,text=f"Total nucleotides:")
        self.GcCount= ttk.Label(self,text=f"GC count: {self.C_base + self.G_base}")
        self.AtCount= ttk.Label(self,text=f"AT count: {self.A_base+ self.T_base}")
        #placing labels into desired position
        self.grid(row=0,column=1)
        self.statslabel.place(x=0,y=0)
        Ncount_sep.place(x=0,y=15,width=190)
        self.aCount.place(x=0,y=20)
        self.CCount.place(x=0,y=40)
        self.TCount.place(x=0,y=60)
        self.GCount.place(x=0,y=80)
        self.UCount.place(x=0,y=100)
        self.totalNuc.place(x=0,y=120)
        self.CG_AT_Content.place(x=0,y=140)
        GC_sep.place(x=0,y=155,width=190)
        self.GcCount.place(x=0,y=160)
        self.AtCount.place(x=0,y=180)
        self.StatsUpdate.place(x=25,y=300)
        self.SelctUpdate.place(x=10,y=350)
    #this function counts nucleotides in text box and updates it in the stats frame 
    def NucleotideCount(self,parent,CommandType):
        current_text ="X"
        if CommandType=="T":
            current_text = parent.TextBox.get("1.0",tk.END)
            current_text = current_text.upper()
        elif CommandType=="S":

            try:
                current_text = parent.TextBox.get(SEL_FIRST,SEL_LAST)
                current_text = current_text.upper()
            except:
                pass
        if current_text =="":
            return
        for i in current_text:
            if i=='A':
                self.A_base+=1
            elif i=='T':
                self.T_base+=1
            elif i=="C":
                self.C_base+=1
            elif i=='G':
                self.G_base+=1
            elif i=='U':
                self.U_base+=1
        total = self.A_base+self.T_base+self.C_base+self.G_base+self.U_base
        if total  !=0 and self.T_base!=0:
            aPercent=round(self.A_base/total,3)
            gPercent=round(self.G_base/total,3)
            cPercent=round(self.C_base/total,3)
            tPercent=round(self.G_base/total,3)
            uPercent=0
        elif total!=0 and self.U_base!=0:
            aPercent=round(self.A_base/total,3)
            gPercent=round(self.G_base/total,3)
            cPercent=round(self.C_base/total,3)
            tPercent=0
            uPercent=round(self.U_base/total,3)
        else:
            aPercent =0
            gPercent=0
            cPercent=0
            tPercent=0
            uPercent=0
        self.GcCount.config(text=f"GC count: {self.C_base + self.G_base}")
        self.AtCount.config(text=f"AT count: {self.A_base+ self.T_base}")     
        self.aCount.config(text=f"A base: {self.A_base}......{aPercent}%")
        self.CCount.config(text=f"C base: {self.C_base}......{cPercent}%")
        self.TCount.config(text=f"T base: {self.T_base}......{tPercent}%")
        self.GCount.config(text=f"G base: {self.G_base}......{gPercent}%")
        self.UCount.config(text=f"U base: {self.U_base}......{uPercent}%")
        self.totalNuc.config(text=f"Total Nucleotides: {total}")
        #resets base count behind screen until next update
        self.A_base=0
        self.U_base=0
        self.C_base=0
        self.T_base=0
        self.G_base=0   
#main App
class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.iconphoto(False,tk.PhotoImage(file="C:icon\kartel (1).png"))
        menubar = MenuBar(self)
        style = ttk.Style(self)
        style.theme_use('alt')
        self.config(menu=menubar)
        self.config(width=800,height=800)
        self.resizable(False,False)
        self.title("Dna Editor")
        self.resizable=False
        self.TextFrame = ttk.LabelFrame(self,text="Sequence editor")
        self.CompareSeqLabel = ttk.Label(self.TextFrame,text="Seqeunce difference")
        self.CompareSeqDiff = ttk.Label(self.TextFrame,text="The difference between sequences is.. ")
        self.SeqCompareSep = ttk.Separator(self.TextFrame)
        self.StatsFrame = StatsFrame(self)
        self.TextBox = tk.Text(self.TextFrame,undo=True,autoseparators=True,maxundo=8)
        self.scrollbar = ttk.Scrollbar(self.TextFrame,orient=VERTICAL,command=self.TextBox.yview)
        self.TextBox.config(yscrollcommand=self.scrollbar.set)
        self.TextFrame.grid(row=0,column=0,sticky="nsew")
        self.CompareSeqLabel.grid(row=1,column=0)
        self.TextBox.grid(row=0,column=0)
        self.scrollbar.grid(row=0,column=1,sticky="NSW")
        self.SeqCompareSep.place(x=0,y=405,width=680)
        self.CompareSeqDiff.place(x=0,y=410)


       


#MAIN FUNCTIONN
if __name__ == "__main__":
    app=App()
    app.mainloop()

