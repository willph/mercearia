# -*- coding: utf-8 -*-


import tkinter
import os,sys,subprocess
from sys import platform as _platform
import tkinter.filedialog as fdialog
from tkinter import ttk, Toplevel, StringVar, messagebox, Menu, Listbox, Text
import pymysql
from escposprinter import *

listaItens = []
listaPreco = []
linha = []

# Tratar 'Exception' (exceção) ,falha no carregamento do modulo reportlab.
try:
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus.flowables import KeepTogether 
    from reportlab.lib.styles import ParagraphStyle
except Exception:
  print('Not found module reportlab. See www.reportlab.com')
  messagebox.showwarning('ERRO','Not Found python module Reportlab. No Installed!\nSee version for python3.x')


janela = tkinter.Tk() #cria um objeto do tipo Tk
janela.geometry("600x600") #define o tamanho da janela no esquema X Y

janela.title("MERCEARIA DO WILL")

if _platform == "win32":
    janela.state("zoomed")
    janela.wm_iconbitmap("loja.ico")

elif _platform == "linux" or _platform == "linux2":
    janela.attributes('-zoomed', True)
    janela.wm_iconbitmap('@loja.icon')
    #janela.attributes('-fullscreen', True)

elif _platform == "darwin":
    janela.attributes('-zoomed', True)
    janela.wm_iconbitmap('@loja.icon')
    
    #testar linha acima, caso não funcione descomentar essa abaixo e comentar a de cima

    #janela.state("zoomed")
    #janela.wm_iconbitmap("loja.ico")

    
else:
    pass
   
def validate():
    
    cont=0
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
                cont+=1
                if cont > 1:
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
        
        precoEntry.focus()
        return False

    for y in qtdItemEntry.get():
        if y in '0123456789.,':
            if y == '.' or y == ',':
                cont+=1
                if cont > 1 or cont == 1:
                    messagebox.showwarning("ERRO", "DADO INVÁLIDO\n\nDIGITE A QUANTIDADE DO PRODUTO SEM , ou .")
                    qtdItemEntry.delete(0,"end")
                    qtdItemEntry.focus()
                    return False
            
        else:

            messagebox.showwarning("ERRO", "DADO INVÁLIDO\n\nDIGITE A QUANTIDADE DO PRODUTO")
            qtdItemEntry.delete(0,"end")
            qtdItemEntry.focus()
            return False

    if int(qtdItemEntry.get()) == 0:
        messagebox.showwarning("ERRO", "A QUANTIDADE NÃO PODE SER 0\n\nDIGITE A QUANTIDADE DO PRODUTO")
        qtdItemEntry.delete(0,"end")
        qtdItemEntry.focus()
        return False
        

    try:
        conexao = pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='merciaria')
        cursor = conexao.cursor()
        query = "SELECT qtd FROM produtos WHERE nome = %s"%("'"+(itemEntry.get())+"'")
        cursor.execute(query)
        result= cursor.execute(query)
        result= cursor.fetchone()
        vrfItem = int(result[0])
        if vrfItem == 0 or vrfItem < int(qtdItemEntry.get()):
            messagebox.showwarning("ERRO", "ESTOQUE INSUFICIENTE PARA "+(itemEntry.get())+"\n\n SÓ TEM %s"%(vrfItem)+" NO ESTOQUE.")
            qtdItemEntry.delete(0,"end")
            qtdItemEntry.focus()
            return False
    except:
        pass

    
    float(precoEntry.get())
    return True

def validate2():
    cont=0
    for x in dindinEntry.get():
        if x in '0123456789.':
            if x == '.':
                cont+=1
                if cont > 1:
                    messagebox.showwarning("ERRO", "DADO INVÁLIDO\n\nDIGITE O VALOR")
                    dindinEntry.delete(0,"end")
                    dindinEntry.focus()
                    return False

        else:
            messagebox.showwarning("ERRO", "DADO INVÁLIDO\n\nDIGITE O VALOR")
            dindinEntry.delete(0,"end")
            dindinEntry.focus()
            return False
        
    if float(dindinEntry.get()) == 0:
        messagebox.showwarning("ERRO", "O DINHEIRO NÃO PODE SER 0\n\nDIGITE O VALOR CORRETO")
        dindinEntry.delete(0,"end")
        dindinEntry.focus()
        return False
    
    float(dindinEntry.get())
    return True


def add(event=None):

    result1 = ""
    result2 = ""
    if event is None or True:
        if itemEntry.get() == result1:
            messagebox.showwarning("ERRO", "CAMPO VAZIO\n\nDIGITE O NOME DO PRODUTO")
            itemEntry.focus()
        elif precoEntry.get() == result2:
            messagebox.showwarning("ERRO", "CAMPO VAZIO\n\nDIGITE O VALOR DO PRODUTO")
            precoEntry.focus()
        elif validate():
            listaItens.append(itemEntry.get())
            listaPreco.append((precoEntry.get(), qtdItemEntry.get()))
            listagem.config(state="normal")
            listagem.insert("insert",(str(len(listaItens))+" - "+itemEntry.get()+" - R$ "+str("%.2f"%float(precoEntry.get()))+
                                      " - Qtd: " +str(int(qtdItemEntry.get()))+" - SubTotal: "+str("%.2f"%float(subTotal()))+"\n"))
            
            linha.append(str(len(listaItens))+" - "+itemEntry.get()+" - R$ "+str("%.2f"%float(precoEntry.get()))+
                         " - Qtd " +str(int(qtdItemEntry.get()))+" - SubTotal: "+str("%.2f"%float(subTotal())))
            
            exibeTotal.config(text=str("%.2f"%soma()))
            listagem.config(state="disabled")
            try:
                conexao = pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='merciaria')
                cursor = conexao.cursor()
                query = "UPDATE produtos SET qtd = qtd-%s"%(qtdItemEntry.get())+" WHERE nome = %s"%("'"+(itemEntry.get())+"'")
                cursor.execute(query)
                cursor.close()
                conexao.close()
                itemEntry.delete(0,"end")
                precoEntry.delete(0,"end")
                qtdItemEntry.delete(0,"end")
                itemEntry.focus()

            except:
                itemEntry.delete(0,"end")
                precoEntry.delete(0,"end")
                qtdItemEntry.delete(0,"end")
                itemEntry.focus()
                #pass
                return messagebox.showwarning("ERRO","Não foi possivel atualização do estoque!")
    pass
    
    
def soma(total = 0.0):
    for i in range(len(listaPreco)):
        qtd=int(listaPreco[i][1])
        valor=float(listaPreco[i][0])
        total+=valor*qtd
    return total

def subTotal(total = 0.0):
    for i in range(len(listaPreco)):
        qtd=int(listaPreco[i][1])
        valor=float(listaPreco[i][0])
        total= valor*qtd
    return total


def troco(event=None):
    result = ""

    if event is None or True:
        if dindinEntry.get() == result:
            messagebox.showwarning("CAMPO VAZIO", "DIGITE O DINHEIRO PARA FINALIZAR A COMPRA")
            dindinEntry.focus()

        elif len(listaItens) == 0:
            messagebox.showinfo("TELA VAZIA", "ADICIONE PRIMEIRO UM PRODUTO")
            dindinEntry.delete(0,"end")
            itemEntry.focus()

        elif validate2():
            if float(dindinEntry.get()) < soma():
                messagebox.showwarning("ERRO", "VALOR MENOR QUE A VENDA.")
                dindinEntry.delete(0,"end")
                dindinEntry.focus()
            else:
                troco1 = float(dindinEntry.get()) - soma()
                dindinEntry.delete(0,"end")
                exibeTroco.config(text=str("%.2f"%troco1))

    pass

def remover():
    if len(listaItens) == 0:
        messagebox.showwarning("CAMPO VAZIO", "NÃO TEM PRODUTO PARA EXCLUIR.")
        itemEntry.focus()
        
    if len(listaItens) != 0:
        listagem.config(state="normal")
        listagem.delete(str(len(listaItens))+'.0',"end")
        listaItens.pop()
        listagem.delete(str(len(listaPreco))+'.0',"end")
        listaPreco.pop()
        exibeTotal.config(text=str("%.2f"%soma()))
        listagem.config(state="disabled")

    if len(listaItens) != 0:
        listagem.config(state="normal")
        listagem.insert("insert",("\n"))
        listagem.config(state="disabled")

    pass

def limparTotal(event=None):
    if len(listaItens) == 0:
        messagebox.showinfo("TELA VAZIA", "A TELA JÁ ESTA LIMPA")
        itemEntry.focus()

    else:
        result = messagebox.askyesno("NOVA COMPRA", "Tem certeza que deseja apagar todos os dados?")
        if result == True:
            listagem.config(state="normal")
            listagem.delete('1.0',"end")
            del listaItens[:]
            listagem.delete('1.0',"end")
            del listaPreco[:]
            exibeTotal.config(text="0.00")
            exibeTroco.config(text="0.00")
            listagem.config(state="disabled")
            itemEntry.focus()
    pass

def salvar(event=None):
    arq_nome = tkinter.filedialog.asksaveasfile(mode='w', defaultextension='.txt', filetypes=[('Arquivo Notepad *.txt', '*.txt')])
    if arq_nome is None:
        pass
    else:
        arq = open(arq_nome.name,'w')
        arq.write("                             Lista de Compras\n\n\n\n")
        arq.write(listagem.get('1.0','end'))
        arq.write("\nTotal: R$ "+str("%.2f"%soma())+"\n")
        arq.close()

        
def imprimir(event=None):
    if _platform == "win32":
        homeDir = os.environ["USERPROFILE"]
        arq = open(homeDir+"\\AppData\\Local\\Temp\\imprimir.doc",'w')
        arq.write("                             Lista de Compras\n\n\n\n")
        arq.write(listagem.get('1.0','end'))
        arq.write("\nTotal: R$ "+str("%.2f"%soma())+"\n")
        arq.close()
        os.startfile(homeDir+"\\AppData\\Local\\Temp\\imprimir.doc", "print")
    
        #os.remove("imprimir.doc")

    elif _platform == "linux" or _platform == "linux2":
        #messagebox.showwarning('FALHA','Sistema ainda não foi implementado')
        """ Seiko Epson Corp. Receipt Printer M129 Definitions (EPSON TM-T88IV) """
        Epson = printer.Network("192.168.129.208")
        # Print text
        Epson.text("\n")
        Epson.text("\n")
        Epson.text("\n")
        Epson.text("                             Lista de Compras\n\n\n\n")
        Epson.text(listagem.get('1.0','end'))
        Epson.text("\nTotal: R$ "+str("%.2f"%soma())+"\n")
        Epson.cut(mode="u")
        #Epson.close()



def gerarRelEstoque(event=None):
    contEstoq = []
    if _platform == "win32":
        homeDir = os.environ["USERPROFILE"]
        doc = SimpleDocTemplate(homeDir+"\\Documents\\Rel_Estoque.pdf")
        Story = [Spacer(1,0*inch)]
        styles = getSampleStyleSheet()

        linha1 = Paragraph('<para align=center>RELATÓRIO CONTROLE DE ESTOQUE</para>', styles['Title'])
        Story.append(KeepTogether(linha1))
        Story.append(Spacer(0,0.8 * inch))

        
        linha2 = Paragraph('<para align=left><font size= 11><b>QTD | NOME</b></font></para>', styles['Normal'])
        Story.append(KeepTogether(linha2))
        Story.append(Spacer(0,0.1 * inch))
        
        try:
            conexao = pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='merciaria')
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM `produtos` ORDER BY `produtos`.`nome` ASC") #executando o código SQL na conexão atual
                    
            for linha in cursor:
                nome = linha[1]
                qtd = linha[3]
                itemPdt = linha[4]
                contEstoq.append((nome,qtd,itemPdt))

        except:
            return messagebox.showwarning("FALHA","NÃO FOI POSSIVEL LOCALIZAR PRODUTO. PRODUTO INEXISTENTE, SERVIDOR OFF-LINE OU BANCO DE DADOS INEXISTENTE")

        for item in range(len(contEstoq)):
            linha3 =  Paragraph(""+str(contEstoq[item][1])+" "+contEstoq[item][2]+" - "+contEstoq[item][0]+"", styles['BodyText'])
            Story.append(KeepTogether(linha3))
            
        
        doc.build(Story)
        cursor.close()
        conexao.close()
        messagebox.showinfo("SALVO", """SUA PRATAFORMA É WINDOWS

ARQUIVO GERADO COM SUCESSO NA PASTA 'MEUS DOCUMENTOS'
COM NOME Rel_Estoque.pdf
""")
    elif _platform == "linux" or _platform == "linux2":
        homeDir = os.environ["HOME"]
        doc = SimpleDocTemplate(homeDir+"/Documentos/Rel_Estoque.pdf")
        Story = [Spacer(1,0*inch)]
        styles = getSampleStyleSheet()

        linha1 = Paragraph('<para align=center>RELATÓRIO CONTROLE DE ESTOQUE</para>', styles['Title'])
        Story.append(KeepTogether(linha1))
        Story.append(Spacer(0,0.8 * inch))

        
        linha2 = Paragraph('<para align=left><font size= 11><b>QTD | NOME</b></font></para>', styles['Normal'])
        Story.append(KeepTogether(linha2))
        Story.append(Spacer(0,0.1 * inch))
        
        try:
            conexao = pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='merciaria')
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM `produtos` ORDER BY `produtos`.`nome` ASC") #executando o código SQL na conexão atual
                    
            for linha in cursor:
                nome = linha[1]
                qtd = linha[3]
                itemPdt = linha[4]
                contEstoq.append((nome,qtd,itemPdt))
                

        except:
            return messagebox.showwarning("FALHA","NÃO FOI POSSIVEL LOCALIZAR PRODUTO. PRODUTO INEXISTENTE, SERVIDOR OFF-LINE OU BANCO DE DADOS INEXISTENTE")

        for item in range(len(contEstoq)):
            linha3 =  Paragraph(""+str(contEstoq[item][1])+" "+contEstoq[item][2]+" - "+contEstoq[item][0]+"", styles['BodyText'])
            Story.append(KeepTogether(linha3))
            
        
        doc.build(Story)
        cursor.close()
        conexao.close()
        messagebox.showinfo("SALVO", """SUA PLATAFORMA É LINUX

ARQUIVO GERADO COM SUCESSO NA PASTA 'DOCUMENTOS'
COM NOME minhasCompras.pdf
""")

    elif _platform == "darwin":
        homeDir = os.environ["HOME"]
        doc = SimpleDocTemplate(homeDir+"/Documents/Rel_Estoque.pdf")
        Story = [Spacer(1,0*inch)]
        styles = getSampleStyleSheet()

        linha1 = Paragraph('<para align=center>RELATÓRIO CONTROLE DE ESTOQUE</para>', styles['Title'])
        Story.append(KeepTogether(linha1))
        Story.append(Spacer(0,0.8 * inch))

        
        linha2 = Paragraph('<para align=left><font size= 11><b>QTD | NOME</b></font></para>', styles['Normal'])
        Story.append(KeepTogether(linha2))
        Story.append(Spacer(0,0.1 * inch))
        
        try:
            conexao = pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='merciaria')
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM `produtos` ORDER BY `produtos`.`nome` ASC") #executando o código SQL na conexão atual
                    
            for linha in cursor:
                nome = linha[1]
                qtd = linha[3]
                itemPdt = linha[4]
                contEstoq.append((nome,qtd,itemPdt))

        except:
            return messagebox.showwarning("FALHA","NÃO FOI POSSIVEL LOCALIZAR PRODUTO. PRODUTO INEXISTENTE, SERVIDOR OFF-LINE OU BANCO DE DADOS INEXISTENTE")

        for item in range(len(contEstoq)):
            linha3 =  Paragraph(""+str(contEstoq[item][1])+" "+contEstoq[item][2]+" - "+contEstoq[item][0]+"", styles['BodyText'])
            Story.append(KeepTogether(linha3))
            
        
        doc.build(Story)
        cursor.close()
        conexao.close()
        messagebox.showinfo("SALVO", """SUA PLATAFORMA É MACINTOSH

ARQUIVO GERADO COM SUCESSO NA PASTA 'DOCUMENTOS'
COM NOME minhasCompras.pdf
""")
        
    else:
        
        messagebox.showinfo("ERRO", """
PLATAFORMA NÃO INDENTIFICADA ARQUIVO VAI SER
GERADO E VOCÊ IRA ESCOLHER ONDE DESEJA SALVAR
""")    
        arq_nome = tkinter.filedialog.asksaveasfile(defaultextension='.pdf', filetypes =[('Arquivo PDF *.pdf', '*.pdf')])
        if arq_nome is None:
            pass
        else:
            doc = SimpleDocTemplate(arq_nome.name)
            Story = [Spacer(1,0*inch)]
            styles = getSampleStyleSheet()

        linha1 = Paragraph('<para align=center>RELATÓRIO CONTROLE DE ESTOQUE</para>', styles['Title'])
        Story.append(KeepTogether(linha1))
        Story.append(Spacer(0,0.8 * inch))

        
        linha2 = Paragraph('<para align=left><font size= 11><b>QTD | NOME</b></font></para>', styles['Normal'])
        Story.append(KeepTogether(linha2))
        Story.append(Spacer(0,0.1 * inch))
        
        try:
            conexao = pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='merciaria')
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM `produtos` ORDER BY `produtos`.`nome` ASC") #executando o código SQL na conexão atual
                    
            for linha in cursor:
                nome = linha[1]
                qtd = linha[3]
                itemPdt = linha[4]
                contEstoq.append((nome,qtd,itemPdt))

        except:
            return messagebox.showwarning("FALHA","NÃO FOI POSSIVEL LOCALIZAR PRODUTO. PRODUTO INEXISTENTE, SERVIDOR OFF-LINE OU BANCO DE DADOS INEXISTENTE")

        for item in range(len(contEstoq)):
            linha3 =  Paragraph(""+str(contEstoq[item][1])+" "+contEstoq[item][2]+" - "+contEstoq[item][0]+"", styles['BodyText'])
            Story.append(KeepTogether(linha3))
            
        
        doc.build(Story)
        cursor.close()
        conexao.close()
    itemEntry.focus()

    
def gerarPdf(event=None):
    if _platform == "win32":
        homeDir = os.environ["USERPROFILE"]
        doc = SimpleDocTemplate(homeDir+"\\Documents\\minhasCompras.pdf")
        Story = [Spacer(1,0*inch)]
        styles = getSampleStyleSheet()

        linha1 = Paragraph('<para align=center>LISTA DE COMPRAS</para>', styles['Title'])
        Story.append(KeepTogether(linha1))
        Story.append(Spacer(0,0.8 * inch))
        for x in linha:
            linha2 =  Paragraph(x, styles['Normal'])
            Story.append(KeepTogether(linha2))

        Story.append(Spacer(0,0.5 * inch))
        linha3 = Paragraph('<para align=left><font size= 12><b>TOTAL:</b> R$ '+str("%.2f"%soma())+'</font></para>', styles['BodyText'])
        Story.append(KeepTogether(linha3))

        doc.build(Story)
        messagebox.showinfo("SALVO", """SUA PRATAFORMA É WINDOWS

ARQUIVO GERADO COM SUCESSO NA PASTA 'MEUS DOCUMENTOS'
COM NOME minhasCompras.pdf
""")
    elif _platform == "linux" or _platform == "linux2":
        homeDir = os.environ["HOME"]
        doc = SimpleDocTemplate(homeDir+"/Documentos/minhasCompras.pdf")
        Story = [Spacer(1,0*inch)]
        styles = getSampleStyleSheet()

        linha1 = Paragraph('<para align=center>LISTA DE COMPRAS</para>', styles['Title'])
        Story.append(KeepTogether(linha1))
        Story.append(Spacer(0,0.8 * inch))
        for x in linha:
            linha2 =  Paragraph(x, styles['Normal'])
            Story.append(KeepTogether(linha2))

        Story.append(Spacer(0,0.5 * inch))
        linha3 = Paragraph('<para align=left><font size= 12><b>TOTAL:</b> R$ '+str("%.2f"%soma())+'</font></para>', styles['BodyText'])
        Story.append(KeepTogether(linha3))

        doc.build(Story)
        messagebox.showinfo("SALVO", """SUA PLATAFORMA É LINUX

ARQUIVO GERADO COM SUCESSO NA PASTA 'DOCUMENTOS'
COM NOME minhasCompras.pdf
""")

    elif _platform == "darwin":
        homeDir = os.environ["HOME"]
        doc = SimpleDocTemplate(homeDir+"/Documents/minhasCompras.pdf")
        Story = [Spacer(1,0*inch)]
        styles = getSampleStyleSheet()

        linha1 = Paragraph('<para align=center>LISTA DE COMPRAS</para>', styles['Title'])
        Story.append(KeepTogether(linha1))
        Story.append(Spacer(0,0.8 * inch))
        for x in linha:
            linha2 =  Paragraph(x, styles['Normal'])
            Story.append(KeepTogether(linha2))

        Story.append(Spacer(0,0.5 * inch))
        linha3 = Paragraph('<para align=left><font size= 12><b>TOTAL:</b> R$ '+str("%.2f"%soma())+'</font></para>', styles['BodyText'])
        Story.append(KeepTogether(linha3))

        doc.build(Story)
        messagebox.showinfo("SALVO", """SUA PLATAFORMA É MACINTOSH

ARQUIVO GERADO COM SUCESSO NA PASTA 'DOCUMENTOS'
COM NOME minhasCompras.pdf
""")
        
    else:
        
        messagebox.showinfo("ERRO", """
PLATAFORMA NÃO INDENTIFICADA ARQUIVO VAI SER
GERADO E VOCÊ IRA ESCOLHER ONDE DESEJA SALVAR
""")    
        arq_nome = tkinter.filedialog.asksaveasfile(defaultextension='.pdf', filetypes =[('Arquivo PDF *.pdf', '*.pdf')])
        if arq_nome is None:
            pass
        else:
            doc = SimpleDocTemplate(arq_nome.name)
            Story = [Spacer(1,0*inch)]
            styles = getSampleStyleSheet()

            linha1 = Paragraph('<para align=center>LISTA DE COMPRAS</para>', styles['Title'])
            Story.append(KeepTogether(linha1))
            Story.append(Spacer(0,0.8 * inch))
            for x in linha:
                linha2 =  Paragraph(x, styles['Normal'])
                Story.append(KeepTogether(linha2))

            Story.append(Spacer(0,0.5 * inch))
            linha3 = Paragraph('<para align=left><font size= 12><b>TOTAL:</b> R$ '+str("%.2f"%soma())+'</font></para>', styles['BodyText'])
            Story.append(KeepTogether(linha3))

            doc.build(Story)
    itemEntry.focus()
        
def gerarDoc(event=None):
    if _platform == "win32":
        homeDir = os.environ["USERPROFILE"]
        arq = open(homeDir+"\\Documents\\minhasCompras.doc",'w')
        arq.write("                             Lista de Compras\n\n\n\n")
        arq.write(listagem.get('1.0','end'))
        arq.write("\nTotal: R$ "+str("%.2f"%soma())+"\n")
        arq.close()
        messagebox.showinfo("SALVO", """SUA PRATAFORMA É WINDOWS

ARQUIVO GERADO COM SUCESSO NA PASTA 'MEUS DOCUMENTOS'
COM NOME minhasCompras.doc
""")
    elif _platform == "linux" or _platform == "linux2":
        homeDir = os.environ["HOME"]
        arq = open(homeDir+"/Documentos/minhasCompras.doc",'w')
        arq.write("                             Lista de Compras\n\n\n\n")
        arq.write(listagem.get('1.0','end'))
        arq.write("\nTotal: R$ "+str("%.2f"%soma())+"\n")
        arq.close()
        messagebox.showinfo("SALVO", """SUA PLATAFORMA É LINUX

ARQUIVO GERADO COM SUCESSO NA PASTA 'DOCUMENTOS'
COM NOME minhasCompras.doc
""")
        
    elif _platform == "darwin":
        homeDir = os.environ["HOME"]
        arq = open(homeDir+"/Documents/minhasCompras.doc",'w')
        arq.write("                             Lista de Compras\n\n\n\n")
        arq.write(listagem.get('1.0','end'))
        arq.write("\nTotal: R$ "+str("%.2f"%soma())+"\n")
        arq.close()
        messagebox.showinfo("SALVO", """SUA PLATAFORMA É MACINTOSH

ARQUIVO GERADO COM SUCESSO NA PASTA 'DOCUMENTOS'
COM NOME minhasCompras.doc
""")

    else:
        
        messagebox.showinfo("ERRO", """
PLATAFORMA NÃO INDENTIFICADA ARQUIVO VAI SER
GERADO E VOCÊ IRA ESCOLHER ONDE DESEJA SALVAR
""")
        arq_nome = tkinter.filedialog.asksaveasfile(mode='w', defaultextension='.doc', filetypes =[('Microsoft Word *.doc', '*.doc')])
        if arq_nome is None:
            pass
        else:
            arq = open(arq_nome.name,'w')
            arq.write("                             Lista de Compras\n\n\n\n")
            arq.write(listagem.get('1.0','end'))
            arq.write("\nTotal: R$ "+str("%.2f"%soma())+"\n")
            arq.close()

    itemEntry.focus()
        
                   

def sobre():
    messagebox.showinfo("SOBRE", """
CODIGO FEITO POR:      

WILMERSON FELIPE
CARLOS EDUARDO
JADEMIR MOURA
WANDESON RICARDO


""")


def fechar():
    result = messagebox.askyesno("FECHAR PROGRAMA", "Tem certeza que deseja fechar o programa?")
    if result == True:
        janela.destroy()
    pass

def capsLock(event):
    txt.set(txt.get().upper())
    pass

def capsLock2(event):
    txt2.set(txt2.get().upper())
    pass

def leiame(event=None):
    ajunew = Toplevel()
    ajunew.title('LEIA-ME')
    if _platform == "win32":
        ajunew.geometry("400x400")
        ajunew.wm_iconbitmap("loja.ico")

    elif _platform == "linux" or _platform == "linux2":
        ajunew.geometry("380x325")
        ajunew.wm_iconbitmap('@loja.icon')
        #janela.attributes('-fullscreen', True)

    elif _platform == "darwin":
        ajunew.geometry("380x325")
        ajunew.wm_iconbitmap('@loja.icon')
        
        #testar linha acima, caso não funcione descomentar essa abaixo e comentar a de cima

        #janela.state("zoomed")
        #janela.wm_iconbitmap("loja.ico")

        
    else:
        pass


    textHelp= """
----------------SOBRE O SOFTWARE---------------

Este software foi desenvolvido para ajudar na
lista de compra dos usuarios. Com ele você
pode gerar PDF, DOC, salvar em
arquivo TXT ou imprimir.


----------------TECLA DE ATALHO----------------

Pesquisar Produto => ALT + P
Nova Compra => ALT + N
Inserir o Dinheiro => ALT + D
Gerar relatório do estoque => CTRL + R
Gerar PDF => CTRL + F
Gerar DOC => CTRL + D
Salvar em TXT => CTRL + S
Imprimir => CTRL + P
Sair => ALT + F4
Ajuda => F1


"""
    
    ajuframe = ttk.Frame(ajunew, padding = '3 3 12 12')
    ajuframe.pack()
    ajuframe.columnconfigure(0, weight = 1)
    
    ajuframe2 = ttk.Frame(ajunew, padding = '3 3 12 12')
    ajuframe2.pack(anchor="w")
    frameItensAju = Text(ajuframe2)
    frameItensAju.insert("insert", textHelp)
    frameItensAju.config(state="disabled")
    frameItensAju.pack(anchor="w")
    ajunew.focus()


    
def pesquisar(event=None):

    def esc(event):
        new.destroy()
    
    def sel(event):
        if len(itemEntry.get()) != 0 or len(precoEntry.get()) != 0:
            itemEntry.delete(0,"end")
            precoEntry.delete(0,"end")
            index = listbox.curselection()[0]
            seltext = listbox.get(index).split("-")
            selItem = seltext[0]
            selPreco = (seltext[1]).replace("R$","").replace(" ","")
            itemEntry.insert(0, selItem)
            precoEntry.insert(0, selPreco)
            listbox.delete(0, "end")
            new.destroy()
            qtdItemEntry.focus()
            
        else:
            index = listbox.curselection()[0]
            seltext = listbox.get(index).split("-")
            selItem = seltext[0]
            selPreco = (seltext[1]).replace("R$","").replace(" ","")
            itemEntry.insert(0, selItem)
            precoEntry.insert(0, selPreco)
            listbox.delete(0, "end")
            new.destroy()
            qtdItemEntry.focus()
    
    
    def conectar(event2=None):
        itemPesq=[]
        listbox.delete(0, "end")
        if event2 is None or True:
            
            try:
                conexao = pymysql.connect(host='localhost',port=3306,user='root',passwd='',db='merciaria')
                cursor = conexao.cursor()
                cursor.execute("SELECT * FROM produtos WHERE nome LIKE " +"'%"+ itemPesquisa.get()+ "%'" + " ORDER BY nome ASC") #executando o código SQL na conexão atual
                
                for linha in cursor:
                    idproduto = linha[0]
                    nome = linha[1]
                    preco = linha[2]
                    qtd = linha[3]
                    tipoPdt = linha[4]
                    itemPesq.append((idproduto,nome,preco,qtd,tipoPdt))
                    
                for item in range(len(itemPesq)):
                    
                    listbox.insert("end", ""+itemPesq[item][1]+"- R$ "+str("%.2f"%itemPesq[item][2])+" - Qtd: "+str(itemPesq[item][3])+" "+itemPesq[item][4]+"")
                
                listbox.bind('<<ListboxSelect>>', sel)
                itemPesquisa.delete(0,"end")
                
                cursor.close()
                conexao.close()
            except:
                
                return messagebox.showwarning("FALHA","NÃO FOI POSSIVEL LOCALIZAR PRODUTO. PRODUTO INEXISTENTE, SERVIDOR OFF-LINE OU BANCO DE DADOS INEXISTENTE")
                

        
    #janela.withdraw()
    new = Toplevel()
    new.title('PESQUISA DE MERCADORIA')
    if _platform == "win32":
        new.geometry("400x325")
        new.wm_iconbitmap("loja.ico")

    elif _platform == "linux" or _platform == "linux2":
        new.geometry("530x320")
        new.wm_iconbitmap('@loja.icon')
        #janela.attributes('-fullscreen', True)

    elif _platform == "darwin":
        new.geometry("400x325")
        new.wm_iconbitmap('@loja.icon')
        
        #testar linha acima, caso não funcione descomentar essa abaixo e comentar a de cima

        #janela.state("zoomed")
        #janela.wm_iconbitmap("loja.ico")

        
    else:
        pass
    mainframe = ttk.Frame(new, padding = '3 3 12 12')
    mainframe.pack()
    mainframe.columnconfigure(0, weight = 1)
    itemPesquisa = ttk.Entry(mainframe, width="65", justify="center", textvariable=txt2)#cria o campo de entrada de texto
    itemPesquisa.bind("<KeyRelease>", capsLock2)
    itemPesquisa.bind("<Return>", conectar)
    itemPesquisa.grid(column = 1, row = 1, sticky = 'w')
    ttk.Button(mainframe, text = 'Pesquisar', command = conectar).grid(column = 1, row = 1, sticky = 'ne')
    mainframe2 = ttk.Frame(new, padding = '3 3 12 12')
    mainframe2.pack(anchor="w")
    frameItensPesq = tkinter.Label(mainframe2, text="Lista de Produtos")
    frameItensPesq.pack(anchor="w")

    frameItensPesq2 = tkinter.Label(mainframe2, text="")
    frameItensPesq2.pack(side="left")
    
    listbox = Listbox(frameItensPesq2, width="70", height="15")
    listbox.pack(side="left", fill="y")

    scrollbar = ttk.Scrollbar(frameItensPesq2, orient="vertical")
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side="right", fill="y")

    listbox.config(yscrollcommand=scrollbar.set)
    itemPesquisa.focus()
    new.resizable(0,0)
    new.bind_all('<Key-Escape>',  esc)

def qtdfocus(event):
    qtdItemEntry.focus()

def precofocus(event):
    precoEntry.focus()
    
def dindinF(event):
    dindinEntry.focus()
    
    

txt = StringVar()
txt2 = StringVar()


# Menu toolbar --------------------------
# Criando menu
menubar = tkinter.Menu(janela,tearoff=False) #Implementa barra de menu
janela.config(menu=menubar) # configura

fileMenu = tkinter.Menu(menubar, tearoff=False) # Insere um elemento na barra de menu
editarMenu = tkinter.Menu(menubar, tearoff=False)
relMenu = tkinter.Menu(menubar, tearoff=False)
ajudaMenu = tkinter.Menu(menubar, tearoff=False)
menubar.add_cascade(label='Arquivo',menu=fileMenu) # Cria lista de opções do menu (pra Arquivo)
menubar.add_cascade(label='Compra', menu=editarMenu)
menubar.add_cascade(label='Relatorio', menu=relMenu)
menubar.add_cascade(label='Ajuda', menu=ajudaMenu)
fileMenu.add_command(label='Salvar', command=salvar, accelerator="Ctrl+S")
fileMenu.add_command(label='Imprimir', command=imprimir, accelerator="Ctrl+P")

fileMenu.add_separator()

fileMenu.add_command(label='Sair', command=fechar, accelerator="Alt+F4") # Adiciona comando (em Arquivo-> Exit)
editarMenu.add_command(label='Gerar .doc', command=gerarDoc, accelerator="Ctrl+D")
editarMenu.add_command(label='Gerar .pdf', command=gerarPdf, accelerator="Ctrl+F")

relMenu.add_command(label='Gerar Rel. de Estoque', command=gerarRelEstoque, accelerator="Ctrl+R")

ajudaMenu.add_command(label='Leia-me', command=leiame)
ajudaMenu.add_command(label='Sobre', command=sobre)


#---------------TECLAS DE ATALHOS-----------------------

janela.bind_all('<Control-Key-s>', salvar)
janela.bind_all('<Control-Key-d>', gerarDoc)
janela.bind_all('<Control-Key-f>', gerarPdf)
janela.bind_all('<Control-Key-p>', imprimir)
janela.bind_all('<Key-F1>', leiame)
janela.bind_all('<Alt-Key-p>', pesquisar)
janela.bind_all('<Alt-Key-n>', limparTotal)
janela.bind_all('<Alt-Key-d>', dindinF)
janela.bind_all('<Control-Key-r>', gerarRelEstoque)
#--------------------------------------------------------

titulo = tkinter.Label(janela, text="", height="1") #cria um label em Janela
titulo.pack(anchor="ne")#adiciona o titulo a janela

frameInserir = tkinter.Frame(janela, width="50")
frameInserir.pack(anchor="nw")

framePreco = tkinter.Frame(janela)
framePreco.pack(anchor="nw")

frameLista = tkinter.Frame(janela)
frameLista.pack(anchor="center")

frameTotal = tkinter.Frame(janela)
frameTotal.pack(anchor="sw")


dindinFrame = tkinter.Frame(janela)
dindinFrame.pack(anchor="s")

encFrame = tkinter.Frame(janela)
encFrame.pack(anchor="s")

frameTroco = tkinter.Frame(janela)
frameTroco.pack(anchor="sw")

frameLimpar = tkinter.Frame(janela)
frameLimpar.pack(anchor="s")

#frameFechar = tkinter.Frame(janela)
#frameFechar.pack(anchor="s")
if _platform == "win32":
    nomeItem = tkinter.Label(frameInserir, text="PRODUTO: ")
    nomeItem.pack(side="left")

    itemEntry = ttk.Entry(frameInserir, width="62", justify="center", textvariable=txt)#cria o campo de entrada de texto
    itemEntry.bind("<KeyRelease>", capsLock)
    itemEntry.bind("<Return>", qtdfocus)
    itemEntry.focus()
    itemEntry.pack(side="left")#insere o campo de texto na tela
    
    qtdItem = tkinter.Label(frameInserir, text="Qtd: ")
    qtdItem.pack(side="left")

    qtdItemEntry = ttk.Entry(frameInserir, width="5", justify="center")
    qtdItemEntry.bind("<Return>", precofocus)
    qtdItemEntry.pack(side="left")

    precoItem = tkinter.Label(framePreco, text="PREÇO:       ")
    precoItem.pack(side="left")

    precoEntry = ttk.Entry(framePreco, width="37", justify="center")
    precoEntry.bind("<Return>", add)
    precoEntry.pack(side="left")
            
    btRemover = ttk.Button(framePreco,text="Excluir", command=remover)
    btRemover.pack(side="right")

    bt = ttk.Button(framePreco,text="Adicionar",command=add)#cria o botao
    bt.pack(side="right")#adiciona o botão ao Frame
    
elif _platform == "linux" or _platform == "linux2":
    nomeItem = tkinter.Label(frameInserir, text="PRODUTO:")
    nomeItem.pack(side="left")

    itemEntry = ttk.Entry(frameInserir, width="58", justify="center", textvariable=txt)#cria o campo de entrada de texto
    itemEntry.bind("<KeyRelease>", capsLock)
    itemEntry.bind("<Return>", precofocus)
    itemEntry.focus()
    itemEntry.pack(side="left")#insere o campo de texto na tela

    qtdItem = tkinter.Label(frameInserir, text=" Qtd: ")
    qtdItem.pack(side="left")

    qtdItemEntry = ttk.Entry(frameInserir, width="5", justify="center")
    qtdItemEntry.bind("<Return>", precofocus)
    qtdItemEntry.pack(side="left")

    precoItem = tkinter.Label(framePreco, text="PREÇO:     ")
    precoItem.pack(side="left")

    precoEntry = ttk.Entry(framePreco, width="37", justify="center")
    precoEntry.bind("<Return>", add)
    precoEntry.pack(side="left")
            
    btRemover = ttk.Button(framePreco,text="Excluir", command=remover)
    btRemover.pack(side="right")

    bt = ttk.Button(framePreco,text="Adicionar",command=add)#cria o botao
    bt.pack(side="right")#adiciona o botão ao Frame

elif _platform == "darwin":

    nomeItem = tkinter.Label(frameInserir, text="PRODUTO: ")
    nomeItem.pack(side="left")

    itemEntry = ttk.Entry(frameInserir, width="62", justify="center", textvariable=txt)#cria o campo de entrada de texto
    itemEntry.bind("<KeyRelease>", capsLock)
    itemEntry.bind("<Return>", qtdfocus)
    itemEntry.focus()
    itemEntry.pack(side="left")#insere o campo de texto na tela
    
    qtdItem = tkinter.Label(frameInserir, text="Qtd: ")
    qtdItem.pack(side="left")

    qtdItemEntry = ttk.Entry(frameInserir, width="5", justify="center")
    qtdItemEntry.bind("<Return>", precofocus)
    qtdItemEntry.pack(side="left")

    precoItem = tkinter.Label(framePreco, text="PREÇO:       ")
    precoItem.pack(side="left")

    precoEntry = ttk.Entry(framePreco, width="37", justify="center")
    precoEntry.bind("<Return>", add)
    precoEntry.pack(side="left")
            
    btRemover = ttk.Button(framePreco,text="Excluir", command=remover)
    btRemover.pack(side="right")

    bt = ttk.Button(framePreco,text="Adicionar",command=add)#cria o botao
    bt.pack(side="right")#adiciona o botão ao Frame

else:
    nomeItem = tkinter.Label(frameInserir, text="PRODUTO: ")
    nomeItem.pack(side="left")

    itemEntry = ttk.Entry(frameInserir, width="62", justify="center", textvariable=txt)#cria o campo de entrada de texto
    itemEntry.bind("<KeyRelease>", capsLock)
    itemEntry.bind("<Return>", qtdfocus)
    itemEntry.focus()
    itemEntry.pack(side="left")#insere o campo de texto na tela
    
    qtdItem = tkinter.Label(frameInserir, text="Qtd: ")
    qtdItem.pack(side="left")

    qtdItemEntry = ttk.Entry(frameInserir, width="5", justify="center")
    qtdItemEntry.bind("<Return>", precofocus)
    qtdItemEntry.pack(side="left")

    precoItem = tkinter.Label(framePreco, text="PREÇO:       ")
    precoItem.pack(side="left")

    precoEntry = ttk.Entry(framePreco, width="37", justify="center")
    precoEntry.bind("<Return>", add)
    precoEntry.pack(side="left")
            
    btRemover = ttk.Button(framePreco,text="Excluir", command=remover)
    btRemover.pack(side="right")

    bt = ttk.Button(framePreco,text="Adicionar",command=add)#cria o botao
    bt.pack(side="right")#adiciona o botão ao Frame
    

btPesquisar = ttk.Button(titulo, text="Pesquisar", command=pesquisar)
btPesquisar.pack()

frameItens = tkinter.LabelFrame(frameLista, text="Itens:")
frameItens.pack()

listagem = Text(frameItens, width="800", height="24", font=("Times New Roman",10))
scroll = ttk.Scrollbar(frameItens, command=listagem.yview)
listagem.config(yscrollcommand=scroll.set, state="disabled")
scroll.pack(side="right", fill="y")
listagem.pack()


LabelTotal = tkinter.Label(frameTotal, text="Total: R$")
LabelTotal.pack(side="left")

exibeTotal = tkinter.Label(frameTotal, text="0.00")
exibeTotal.pack(side="left")

dindinLabel = tkinter.Label(dindinFrame, text="Dinheiro: R$")
dindinLabel.pack(side="left")

dindinEntry = ttk.Entry(dindinFrame, width="14", justify="right")
dindinEntry.bind("<Return>", troco)
dindinEntry.pack(side="left")

dindinBotao = ttk.Button(encFrame,text="ENCERRAR COMPRA", command=troco, width="25")
dindinBotao.pack()

trocoTotal = tkinter.Label(frameTroco, text="Troco: R$")
trocoTotal.pack(side="left")

exibeTroco = tkinter.Label(frameTroco, text="0.00")
exibeTroco.pack(side="left")

limpaTela = ttk.Button(frameLimpar, text="NOVA COMPRA", command=limparTotal, width="25")
limpaTela.pack()

#fechaTela = tkinter.Button(frameFechar, text="FECHAR PROGRAMA", command=fechar, width="20", height="2")
#fechaTela.pack(anchor="s")

janela.protocol("WM_DELETE_WINDOW", fechar)
janela.mainloop()
