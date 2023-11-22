from tkinter import *
from sympy.parsing.sympy_parser import parse_expr
from sympy import symbols, sympify
from pyeda.inter import *
from math import pi, cos, sin, prod


def resultado(var, listaSimbolos, eqI):
    # troca o símbolo Equal (do pyeda) para Equivalente (do sympy)
    eq = sympify(str(expr(eqI)).replace("Equal","Equivalent"))
    sim1 = ['=>','<=>','|','&','^']
    sim2 = ['⇒','⇔','∨','∧','⊻']

    # substitui os símbolos digitados para um só caractere
    for s in range(5):
        eqI = eqI.replace(sim1[s], sim2[s])

    # coloca a equação intermediária ou principal no início da lista
    res = [' '.join(eqI[1:-1]).upper()]

    # coloca os respectivos valores da equação intermediária ou principal na lista
    for i in range(2**len(var[0])):
        res.append(str(int(eq.subs(listaSimbolos[i])==True)))
    return res

def equacoesIntermediaria(eq, var, listaSimbolos):
    try:
        # algoritmo de identificação dos parênteses para criar as
        # e o erro de parênteses incompleto equações intermediárias
        tab = [ [ str(i[j][1]) for i in listaSimbolos ] for j in range(len(var[0])) ]
        for i in range(len(tab)):
            tab[i].insert(0,var[0][i])
        sep = []
        for f in range(len(eq)):
            if eq[f] == '(':
                inicio = f
                pos = 1
                f2 = f
                while pos != 0:
                    f2+=1
                    if eq[f2] == '(':
                        pos+=1
                    if eq[f2] == ')':
                        pos-=1
                sep.append([inicio,f2])
        sep = sep[::-1]
        try:
            return tab + [ resultado(var, listaSimbolos, ''.join(eq[i[0]:i[1]+1])) for i in sep ]
    
        except:
            # caso haja erro de algo não suportado, coloca uma mensagem de erro na tela
            txt3 = Label(calculadora, text='*Operação não suportada', fg = '#BB0000', bg = '#2f2f2f')
            txt3.config(font=('Calibri', 20))
            txt3.place(relx= 0.07, rely = 0.60)
            return None
    except:
        # caso haja erro de parênteses incompleto, coloca uma mensagem de erro na tela
        txt3 = Label(calculadora, text='*Parênteses fora do lugar', fg = '#BB0000', bg = '#2f2f2f')
        txt3.config(font=('Calibri', 20))
        txt3.place(relx= 0.07, rely = 0.60)
        return None


def geradorTabelaVerdade(eq, var):
    listaSimbolos = []

    for i in range(2**len(var[0])): # for que abrange todas as possibilidades de valores das variáveis

        # função matemática que gera os valores em ordem crescente da tabela verdade:
        # 000 -> 001 -> 010 -> 011 -> 100 ...
        # cria uma lista de cada variável simbólica com cada valor possível dela ( 0 ou 1)
        # e salva no formato ( var, val ), sendo var a variável simbólica e val o valor
        x = [(var[1][j], int(sin(pi*i/2**(len(var[0])-1-j)+0.1)>0 )) for j in range(len(var[0]))]
        listaSimbolos.insert(0,x)
        
    return equacoesIntermediaria(eq, var, listaSimbolos)

def calculadoraLogica(eq): #criadorVariaveis():
    alfa = [chr(65+i) for i in range(26)] + ['e']
    variaveis = []

    # apaga os espaços em branco
    eq = list(eq.replace(" ", ""))

    # confere quais e quantas são as variáveis
    for e in eq:
        for a in alfa:
            if e == a:
                variaveis.append(a)

    # salva as variáveis em uma lista
    variaveis = list(dict.fromkeys(variaveis))

    # salva os símbolos das variáveis em uma lista
    simbolos = [symbols(variaveis[i]) for i in range(len(variaveis))]

    return geradorTabelaVerdade(eq, [variaveis, simbolos])


# criando a função calcula para gerar a tabela verdade

def funcaoCalcula():
    txt3.place_forget()
    #se a pessoa não digitar nada na expressão, vai retornar vazio
    if a1.get() == '':
        return
    #a variável equação vai armazenar a expressão colocado pelo o usuário
    equacao = a1.get()

    #simbolos suportados pelo nosso programa
    sim1 = ['E','-','+','*','x']
    sim2 = ['e','~','|','&','^']
    
    #laço para validar nosso simbolos
    for s in range(1,5):
        equacao = equacao.replace(sim1[s],sim2[s])
    equacao = equacao.upper()
    
    equacao = equacao.replace(sim1[0],sim2[0])
    
    #vai pegar a expressão digitada e vai mandar para a função calculadoraLogica()
    resultado =  calculadoraLogica('(' + equacao + ')')
    if resultado == None:
        return

    #na hora de digitação da expressão, se tiver um parênteses errado, o programa vai avisar
    txt2 = Label(calculadora, text='*Parênteses fora do lugar', fg = '#2f2f2f', bg = '#2f2f2f')
    txt2.config(font=('Calibri', 20))
    txt2.place(relx= 0.07, rely = 0.60)
    
    
    #armazenando os valores das linhas
    linhas = len(resultado)
    #armazenando os valores das colunas
    colunas = len(resultado[0])


    #criação de um sub-menu do menu principal
    tabela = Toplevel(calculadora)
    tabela.title('Resultado')

    #iniciação de criação do frame, que é a parte de interface gráfica
    frame1 = Frame(tabela, bg="#222222")
    frame1.grid(sticky='news')
    
    #criação de um frame
    frame_canvas = Frame(frame1)
    frame_canvas.grid(row=2, column=0, sticky='nw')

    frame_canvas.grid_rowconfigure(0, weight=1)
    frame_canvas.grid_columnconfigure(0, weight=1)
    
    frame_canvas.grid_propagate(False)

    bWidth = 10
    bHeigth = 2

    #adiciona um fundo ao frame
    contGeometryW = sum([ bWidth+int(len(resultado[i][0])*0.8) for i in range(linhas) ])*7.66 + 10

    
    fonteTaut = 15
    if colunas <= 3:
        contGeometryH = 127
        fonteTaut = 11
    elif colunas <= 5:
        contGeometryH = 210
    elif colunas <=9:
        contGeometryH = 372
    else:
        contGeometryH = 700

    #print(contGeometryH)
    
    canvas = Canvas(frame_canvas,width=contGeometryW, height = contGeometryH )
    canvas.pack(fill="both", expand=True)
    
    #coloca um scrollbar no frame
    vsb = Scrollbar(frame_canvas, orient="vertical", command=canvas.yview, width= 20)
    #hsb = Scrollbar(frame_canvas, orient="horizontal", command=canvas.xview, width= 20)

    vsb.grid(row=0, column=1, sticky='ns')
    #hsb.grid(row=1, column=0, sticky='ns')

    canvas.configure(yscrollcommand=vsb.set)#, xscrollcommand=hsb.set)

    #frame para colocar os botões
    frame_buttons = Frame(canvas)
    canvas.create_window((0, 0), window=frame_buttons, anchor='nw')

    #feito um laço para a criação do botão
    buttons = [[Button() for j in range(colunas)] for i in range(linhas)]

    #dois laços para colocar o botões em seus respectivos lugares
    for i in range(linhas):
        for j in range(colunas):
            largura2 = bWidth+int(len(resultado[i][0])*0.8)
            cor='#222222'; fonte='#F0F0F0'
            if j==0: 
                cor = '#e9952a'#'#8a8a8a'
            elif j%2==0:
                cor = '#3a3a3a'
            buttons[i][j] = Button(frame_buttons, text=(resultado[i][j].upper()), height = bHeigth, width = largura2, bg=cor, fg=fonte, font=('calibri', 10))
            buttons[i][j].grid(row=j, column=i, sticky='news')
        
    #atualiza os frames do botão
    frame_buttons.update_idletasks()

    #configura a região de scroll
    canvas.config(scrollregion=canvas.bbox("all"))

    # coloca todos o resultado final em uma lista e faz o produtório dela
    # se algum número for 0 nesse produtório, automaticamente toda a
    # multiplicação fica 0, então a equação não é uma taotologia
    resTautologia = prod( [ int(resultado[linhas-1][i]) for i in range(1, colunas) ] )
    if resTautologia == 0:
        resTautologia = resultado[linhas-1][0] + ' não é uma tautologia.'
    else:
        resTautologia = resultado[linhas-1][0] + ' é uma tautologia.'
    
    #label (texto) da tautologia 
    txttautologia = Label(tabela, text= resTautologia, justify='left', fg = '#f5f5f5', bg = '#888888')
    txttautologia.config(font=(fonte, fonteTaut))
    txttautologia.place(x= 0, y = contGeometryH+6)
    
    #resolução do sub-menu
    tabela.configure(bg = '#888888')
    tabela.geometry(str(int(contGeometryW))+'x'+str(contGeometryH+40))
    #tabela.resizable(False, False)


fonte = 'Calibri'

# inicia o Tkinter
calculadora = Tk()
calculadora.title('Calculadora Lógica')

res = (1500,800)

# cria os label (textos) na janela
txt1 = Label(calculadora, text=' Calculadora Lógica ', fg = '#DFDFDF', bg = '#3f3f3f', relief = RIDGE)
txt1.config(font=(fonte, 31,'bold'))
txt1.place(relx= 0.5, y = 70, anchor = CENTER)

txt2 = Label(calculadora, text='Equação:', fg = '#DFDFDF', bg = '#2f2f2f')
txt2.config(font=(fonte, 20))
txt2.place(relx= 0.07, rely = 0.35)

txt3 = Label(calculadora)

simSup = 'Símbolos suportados:\n(*, &) And\n(+, |) Or\n(-, ~) Not\n(x, ^) xor\n(0, 1) Valores\n( => ) Implicação\n(<=> ) Eqivalência'
txt4 = Label(calculadora, text= simSup, justify='left', fg = '#DFDFDF', bg = '#2f2f2f')
txt4.config(font=('Courier', 11))
txt4.place(relx= 0.74, rely = 0.60)

instr = 'Instruções:\n• Utilize qualquer letra do alfabeto,\nexceto as letras \'I\', \'O\', \'S\'.\n• As equações intermediárias são \ndeterminadas pelos parênteses.'
txt5 = Label(calculadora, text= instr, justify='left', fg = '#DFDFDF', bg = '#2f2f2f')
txt5.config(font=('Courier', 11))
txt5.place(relx= 0.065, rely = 0.73)

# cria a entrada da caixa de texto
a1 = Entry(calculadora, font = ('Courier',30),width=20, fg = 'white', bg = '#3f3f3f')
a1.place(relx=0.07,rely= 0.45)


# configurações da janela da calculadora
calculadora.config(bg = '#2f2f2f')
calculadora.geometry(str(res[0]//2)+'x'+str(res[1]//2))
calculadora.resizable(False, False)

botaoCalcula = Button(calculadora, text='Calcular', command=funcaoCalcula, height = 1, width = 9, fg = '#303030', bg = '#888888')
botaoCalcula.place(relx = 0.77, rely = 0.44)
botaoCalcula.config(font=(fonte, 20))

calculadora.mainloop()


