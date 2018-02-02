import tkinter
from sys import platform as _platform
from tkinter import StringVar, ttk, messagebox, Scrollbar, Listbox
import pymysql

listaItens = []
itemPesq = []
updateExcluir = []
item =""
preco = 0.0

janela = tkinter.Tk() #cria um objeto do tipo Tk
 #define o tamanho da janela no esquema X Y

janela.title("CONTROLE ||| MERCEARIA DO WILL |||")

if _platform == "win32":
    janela.geometry("460x300")
    janela.wm_iconbitmap("loja.ico")

elif _platform == "linux" or _platform == "linux2":
    janela.geometry("520x280")
    janela.wm_iconbitmap('@loja.icon')
    #janela.attributes('-fullscreen', True)

elif _platform == "darwin":
    janela.geometry("520x280")
    janela.wm_iconbitmap('@loja.icon')
    
    #testar linha acima, caso não funcione descomentar essa abaixo e comentar a de cima

    #janela.state("zoomed")
    #janela.wm_iconbitmap("loja.ico")

    
else:
    pass

def fechar():
    result = messagebox.askyesno("FECHAR PROGRAMA", "Tem certeza que deseja fechar o programa?")
    if result == True:
        janela.destroy()
    pass

def capsLock(event):
    txt.set(txt.get().upper())
    txt2.set(txt2.get().upper())
    pass

def validate():
    cont=0
    cont2=0
    cont3=0
    contName=0
    for af in itemEntry.get():
        if af in '0123456789.,QWERTYUIOPASDFGHJKLZXCVBNM ':
            if af == ',':
                contName+=1
                if contName != 0:
                    messagebox.showwarning("ERRO", "DADO INVÁLIDO\n\nDIGITE O NOME DO PRODUTO SEM VIRGULA. USO DE PONTO É PERMITIDO")
                    itemEntry.delete(0,"end")
                    itemEntry.focus()
                    return False
                
        else:
            messagebox.showwarning("ERRO", "DADO INVÁLIDO\n\nDIGITE O NOME DO PRODUTO SEM CARACTERES ESPECIAIS OU ACENTO")
            itemEntry.delete(0,"end")
            itemEntry.focus()
            return False

    for x in precoEntry.get():
        if x in '0123456789.':
            if x == '.':
                cont2+=1
                if cont2 > 1:
                    messagebox.showwarning("ERRO", "DADO INVÁLIDO\n\nDIGITE O VALOR DO PRODUTO")
                    precoEntry.delete(0,"end")
                    precoEntry.focus()
                    return False

        else:
            messagebox.showwarning("ERRO", "DADO INVÁLIDO\n\nDIGITE O VALOR DO PRODUTO")
            precoEntry.delete(0,"end")
            precoEntry.focus()
            return False
        
    if float(precoEntry.get()) == 0:
        messagebox.showwarning("ERRO", "VALOR DO PRODUTO NÃO PODE SER 0.\n\nDIGITE O VALOR DO PRODUTO")
        precoEntry.delete(0,"end")
        precoEntry.focus()
        return False

    for y in qtdEntry.get():
        if y in '0123456789.,':
            if y == '.' or y == ',':
                cont+=1
                if cont > 1 or cont == 1:
                    messagebox.showwarning("ERRO", "DADO INVÁLIDO\n\nDIGITE A QUANTIDADE DO PRODUTO SEM , ou .")
                    qtdEntry.delete(0,"end")
                    qtdEntry.focus()
                    return False
            
        else:

            messagebox.showwarning("ERRO", "DADO INVÁLIDO\n\nDIGITE A QUANTIDADE DO PRODUTO")
            qtdEntry.delete(0,"end")
            qtdEntry.focus()
            return False
        
    if int(qtdEntry.get()) == 0:
        messagebox.showwarning("ERRO", "A QUANTIDADE NÃO PODE SER 0\n\nDIGITE A QUANTIDADE DO PRODUTO")
        qtdEntry.delete(0,"end")
        qtdEntry.focus()
        return False
    
    for z in tipoItemEntry.get():
        if z in '0123456789.,QWERTYUIOPASDFGHJKLZXCVBNM':
            if z == '0' or z == '1' or z == '2' or z == '3' or z == '4' or z == '5' or z == '6' or z == '7' or z == '8' or z == '9' or z == '0' or z == ',' or z == '.':
                cont3+=1
                if cont3 > 1 or cont3 == 1:
                    messagebox.showwarning("ERRO", "DADO INVÁLIDO\n\nDIGITE O TIPO DO PRODUTO SEM NUMEROS PONTOS OU VIRGULAS")
                    tipoItemEntry.delete(0,"end")
                    tipoItemEntry.focus()
                    return False
        else:
            messagebox.showwarning("ERRO", "DADO INVÁLIDO\n\nDIGITE O TIPO DO PRODUTO SEM CARACTERES ESPECIAIS")
            tipoItemEntry.delete(0,"end")
            tipoItemEntry.focus()
            return False
    
    float(precoEntry.get())
    return True


def add():
    listbox.bind('<<ListboxSelect>>', selist)
    nome= itemEntry.get()
    conexao = pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='merciaria')
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos WHERE nome LIKE " +"'%"+ itemEntry.get()+ "%'" + "")
    lvefic = []
    
    for linhaa in cursor:
        lvefic.append(linhaa[1])
        
    result1 = ""
    result2 = ""
    result3 = ""
    result4 = ""
    
    if itemEntry.get() == result1:
        messagebox.showwarning("ERRO", "CAMPO VAZIO\n\nDIGITE O NOME DO PRODUTO")
        itemEntry.focus()
    elif precoEntry.get() == result2:
        messagebox.showwarning("ERRO", "CAMPO VAZIO\n\nDIGITE O VALOR DO PRODUTO")
        precoEntry.focus()
    elif qtdEntry.get() == result2:
        messagebox.showwarning("ERRO", "CAMPO VAZIO\n\nDIGITE A QUANTIDADE DO PRODUTO")
        qtdEntry.focus()
    elif tipoItemEntry.get() == result2:
        messagebox.showwarning("ERRO", "CAMPO VAZIO\n\nDIGITE O TIPO DO PRODUTO")
        tipoItemEntry.focus()

    elif validate():
        if len(lvefic) >= 1:
            if nome != lvefic[0]:
                listaItens.append(itemEntry.get())
                item = itemEntry.get()
                preco = (float(precoEntry.get()))
                qtd = (int(qtdEntry.get()))
                tipoPdt = tipoItemEntry.get()
                listbox.insert("end",(str(len(listaItens))+" - "+itemEntry.get()+" - R$ "+str("%.2f"%float(precoEntry.get()))+" - Qtd: "+str(int(qtdEntry.get()))+" - Tipo: "+tipoItemEntry.get()+""))
                itemEntry.delete(0,"end")
                precoEntry.delete(0,"end")
                qtdEntry.delete(0,"end")
                tipoItemEntry.delete(0,"end")
                itemEntry.focus()
                try:
                    cursor = conexao.cursor()
                    query = "INSERT INTO produtos (nome, preco, qtd, tipoProduto) VALUES(%s,%s,%s,%s)"%("'"+item+"'",preco,qtd,"'"+tipoPdt+"'")
                    cursor.execute(query)
                    return messagebox.showinfo("CADASTRADO","Produto cadastrado com sucesso!")
                except:
                    return messagebox.showwarning("ERRO","Ocorreu um erro na inserção do produto!")
            else:
                itemEntry.delete(0,"end")
                precoEntry.delete(0,"end")
                qtdEntry.delete(0,"end")
                tipoItemEntry.delete(0,"end")
                itemEntry.focus()
                messagebox.showwarning("ERRO","PRODUTO JA ESTA CADASTRADO!")
        else:
            listaItens.append(itemEntry.get())
            item = itemEntry.get()
            preco = (float(precoEntry.get()))
            qtd = (int(qtdEntry.get()))
            tipoPdt = tipoItemEntry.get()
            listbox.insert("end",(str(len(listaItens))+" - "+itemEntry.get()+" - R$ "+str("%.2f"%float(precoEntry.get()))+" - Qtd: "+str(int(qtdEntry.get()))+" - Tipo: "+tipoItemEntry.get()+""))
            itemEntry.delete(0,"end")
            precoEntry.delete(0,"end")
            qtdEntry.delete(0,"end")
            tipoItemEntry.delete(0,"end")
            itemEntry.focus()
            try:
                cursor = conexao.cursor()
                query = "INSERT INTO produtos (nome, preco, qtd, tipoProduto) VALUES(%s,%s,%s,%s)"%("'"+item+"'",preco,qtd,"'"+tipoPdt+"'")
                cursor.execute(query)
                return messagebox.showinfo("CADASTRADO","Produto cadastrado com sucesso!")
            except:
                return messagebox.showwarning("ERRO","Ocorreu um erro na inserção do produto!")
    cursor.close()
    conexao.close()

def selist(event):
        if len(listbox.curselection()) == 0:
            pass
        else:
            index = listbox.curselection()[0]
            seltext = listbox.get(index).split("-")
            idItem = seltext[0]
            selItem = seltext[1]
            selPreco = (seltext[2]).replace("R$","").replace(" ","")
            selQtd = (seltext[3]).replace("Qtd:","").replace(" ","")
            selTipoQtd = (seltext[4]).replace("Tipo:","").replace(" ","")
            updateExcluir.append((idItem).replace(" ", ""))
            itemEntry.insert(0, selItem)
            itemEntry.delete(0)
            itemEntry.delete(len(itemEntry.get())-1)
            precoEntry.insert(0, selPreco)
            qtdEntry.insert(0, selQtd)
            tipoItemEntry.insert(0, selTipoQtd)
            listbox.delete(0, "end")
            
def pesq():
    listbox.delete(0, "end")
    
    try:
        conexao = pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='merciaria')
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produtos WHERE nome LIKE " +"'%"+ itemEntry.get()+ "%'" + " ORDER BY nome ASC")

        for linha in cursor:
            idproduto = linha[0]
            nome = linha[1]
            preco = linha[2]
            qtd = linha[3]
            tipoPdt = linha[4]
            itemPesq.append((idproduto,nome,preco,qtd,tipoPdt))
        
        for item in range(len(itemPesq)):

            listbox.insert("end", ""+str(itemPesq[item][0])+" - "+itemPesq[item][1]+" - R$ "+str("%.2f"%itemPesq[item][2])+" - Qtd: "+str(itemPesq[item][3])+" - Tipo: "+itemPesq[item][4]+"")
        listbox.bind('<<ListboxSelect>>', selist)

        del itemPesq[:]
        itemEntry.delete(0,"end")
        precoEntry.delete(0,"end")
        qtdEntry.delete(0,"end")
        tipoItemEntry.delete(0,"end")
    
        
    except:
        return messagebox.showwarning("FALHA","NÃO FOI POSSIVEL LOCALIZAR PRODUTO. PRODUTO INEXISTENTE, SERVIDOR OFF-LINE OU BANCO DE DADOS INEXISTENTE")
    cursor.close()
    conexao.close()


def update():
    
    try:
        conexao = pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='merciaria')
        cursor = conexao.cursor()
        query = "UPDATE produtos SET nome = '"+itemEntry.get()+"', preco = %s"%float(precoEntry.get())+", qtd = %s"%int(qtdEntry.get())+" WHERE id = %s"%(updateExcluir[0])
        cursor.execute(query)
        cursor.close()
        conexao.close()
        itemEntry.delete(0,"end")
        precoEntry.delete(0,"end")
        qtdEntry.delete(0,"end")
        tipoItemEntry.delete(0,"end")
        itemEntry.focus()
        del updateExcluir[:]
        del itemPesq[:]
        return messagebox.showinfo("ATUALIZADO","Produto atualizado com sucesso!")
    except:
        return messagebox.showwarning("ERRO","Ocorreu um erro na atualização do produto!")
    cursor.close()
    conexao.close()

def excluir():
    
    try:
        conexao = pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='merciaria')
        cursor = conexao.cursor()
        query = "DELETE FROM produtos WHERE id = %s"%(updateExcluir[0])
        cursor.execute(query)
        cursor.close()
        conexao.close()
        itemEntry.delete(0,"end")
        precoEntry.delete(0,"end")
        qtdEntry.delete(0,"end")
        tipoItemEntry.delete(0,"end")
        itemEntry.focus()
        del updateExcluir[:]
        del itemPesq[:]
        return messagebox.showinfo("EXCLUIDO","Produto excluido com sucesso!")
    except:
        return messagebox.showwarning("ERRO","Ocorreu um erro na exclusão do produto!")
    cursor.close()
    conexao.close()


txt = StringVar()
txt2 = StringVar()

titulo = tkinter.Label(janela, text="", height="1")
titulo.pack(anchor="ne")

frameInserir = tkinter.Frame(janela, width="50")
frameInserir.pack(anchor="nw")

framePreco = tkinter.Frame(janela, width="50")
framePreco.pack(anchor="nw")

qtdItemFrame = tkinter.Frame(janela, width="50")
qtdItemFrame.pack(anchor="nw")

tipoItemFrame = tkinter.Frame(janela, width="50")
tipoItemFrame.pack(anchor="nw")

frameBt = tkinter.Frame(janela, width="50")
frameBt.pack(anchor="nw")

frameLista = tkinter.Frame(janela)
frameLista.pack(anchor="sw")

nomeItem = tkinter.Label(frameInserir, text="PRODUTO: ")
nomeItem.pack(side="left")

if _platform == "win32":
    itemEntry = ttk.Entry(frameInserir, width="50", justify="center", textvariable=txt)#cria o campo de entrada de texto
    itemEntry.bind("<KeyRelease>", capsLock)
    itemEntry.focus()
    itemEntry.pack(side="left")


    precoItem = tkinter.Label(framePreco, text="PREÇO:       ")
    precoItem.pack(side="left")

    precoEntry = ttk.Entry(framePreco, width="50", justify="center")
    precoEntry.pack(side="left")


    qtdItem = tkinter.Label(qtdItemFrame, text="QTD:           ")
    qtdItem.pack(side="left")

    qtdEntry = ttk.Entry(qtdItemFrame, width="50", justify="center")
    qtdEntry.pack(side="left")

    tipoItemLabel = tkinter.Label(tipoItemFrame, text="TIPO:          ")
    tipoItemLabel.pack(side="left")

    tipoItemEntry = ttk.Entry(tipoItemFrame, width="50", justify="center", textvariable=txt2)
    tipoItemEntry.bind("<KeyRelease>", capsLock)
    tipoItemEntry.pack(side="left")

elif _platform == "linux" or _platform == "linux2":
    itemEntry = ttk.Entry(frameInserir, width="38", justify="center", textvariable=txt)#cria o campo de entrada de texto
    itemEntry.bind("<KeyRelease>", capsLock)
    itemEntry.focus()
    itemEntry.pack(side="left")


    precoItem = tkinter.Label(framePreco, text="PREÇO:      ")
    precoItem.pack(side="left")

    precoEntry = ttk.Entry(framePreco, width="38", justify="center")
    precoEntry.pack(side="left")


    qtdItem = tkinter.Label(qtdItemFrame, text="QTD:          ")
    qtdItem.pack(side="left")

    qtdEntry = ttk.Entry(qtdItemFrame, width="38", justify="center")
    qtdEntry.pack(side="left")

    tipoItemLabel = tkinter.Label(tipoItemFrame, text="TIPO:          ")
    tipoItemLabel.pack(side="left")

    tipoItemEntry = ttk.Entry(tipoItemFrame, width="38", justify="center", textvariable=txt2)
    tipoItemEntry.bind("<KeyRelease>", capsLock)
    tipoItemEntry.pack(side="left")

elif _platform == "darwin":
    itemEntry = ttk.Entry(frameInserir, width="38", justify="center", textvariable=txt)#cria o campo de entrada de texto
    itemEntry.bind("<KeyRelease>", capsLock)
    itemEntry.focus()
    itemEntry.pack(side="left")


    precoItem = tkinter.Label(framePreco, text="PREÇO:      ")
    precoItem.pack(side="left")

    precoEntry = ttk.Entry(framePreco, width="38", justify="center")
    precoEntry.pack(side="left")


    qtdItem = tkinter.Label(qtdItemFrame, text="QTD:          ")
    qtdItem.pack(side="left")

    qtdEntry = ttk.Entry(qtdItemFrame, width="38", justify="center")
    qtdEntry.pack(side="left")

    tipoItemLabel = tkinter.Label(tipoItemFrame, text="TIPO:          ")
    tipoItemLabel.pack(side="left")

    tipoItemEntry = ttk.Entry(tipoItemFrame, width="38", justify="center", textvariable=txt2)
    tipoItemEntry.bind("<KeyRelease>", capsLock)
    tipoItemEntry.pack(side="left")

else:
    itemEntry = ttk.Entry(frameInserir, width="38", justify="center", textvariable=txt)#cria o campo de entrada de texto
    itemEntry.bind("<KeyRelease>", capsLock)
    itemEntry.focus()
    itemEntry.pack(side="left")


    precoItem = tkinter.Label(framePreco, text="PREÇO:      ")
    precoItem.pack(side="left")

    precoEntry = ttk.Entry(framePreco, width="38", justify="center")
    precoEntry.pack(side="left")


    qtdItem = tkinter.Label(qtdItemFrame, text="QTD:          ")
    qtdItem.pack(side="left")

    qtdEntry = ttk.Entry(qtdItemFrame, width="38", justify="center")
    qtdEntry.pack(side="left")

    tipoItemLabel = tkinter.Label(tipoItemFrame, text="TIPO:          ")
    tipoItemLabel.pack(side="left")

    tipoItemEntry = ttk.Entry(tipoItemFrame, width="38", justify="center", textvariable=txt2)
    tipoItemEntry.bind("<KeyRelease>", capsLock)
    tipoItemEntry.pack(side="left")
    



if _platform == "win32":
    bt3 = ttk.Button(frameBt,text="Excluir",command=excluir, width="13")
    bt3.pack(side="right")
    bt2 = ttk.Button(frameBt,text="Atualizar",command=update, width="14")
    bt2.pack(side="right")
    bt1 = ttk.Button(frameBt,text="Adicionar",command=add, width="14")
    bt1.pack(side="right")
    bt = ttk.Button(frameBt,text="Pesquisar",command=pesq, width="14")
    bt.pack(side="right")


    
elif _platform == "linux" or _platform == "linux2":

    bt3 = ttk.Button(frameBt,text="Excluir",command=excluir, width="10")
    bt3.pack(side="right")
    bt2 = ttk.Button(frameBt,text="Atualizar",command=update, width="10")
    bt2.pack(side="right")
    bt1 = ttk.Button(frameBt,text="Adicionar",command=add, width="11")
    bt1.pack(side="right")
    bt = ttk.Button(frameBt,text="Pesquisar",command=pesq, width="11")
    bt.pack(side="right")

elif _platform == "darwin":
    bt3 = ttk.Button(frameBt,text="Excluir",command=excluir, width="10")
    bt3.pack(side="right")
    bt2 = ttk.Button(frameBt,text="Atualizar",command=update, width="10")
    bt2.pack(side="right")
    bt1 = ttk.Button(frameBt,text="Adicionar",command=add, width="11")
    bt1.pack(side="right")
    bt = ttk.Button(frameBt,text="Pesquisar",command=pesq, width="11")
    bt.pack(side="right")

else:
    bt3 = ttk.Button(frameBt,text="Excluir",command=excluir, width="10")
    bt3.pack(side="right")
    bt2 = ttk.Button(frameBt,text="Atualizar",command=update, width="10")
    bt2.pack(side="right")
    bt1 = ttk.Button(frameBt,text="Adicionar",command=add, width="11")
    bt1.pack(side="right")
    bt = ttk.Button(frameBt,text="Pesquisar",command=pesq, width="11")
    bt.pack(side="right")
    

yscrollbar = ttk.Scrollbar(frameLista)
yscrollbar.pack( side = "right", fill="y")
listbox = Listbox(frameLista, width="80", yscrollcommand = yscrollbar.set)
listbox.pack( side = "left", fill = "both" )
yscrollbar.config( command = listbox.yview )

janela.protocol("WM_DELETE_WINDOW", fechar)
janela.resizable(0,0)
janela.mainloop()
