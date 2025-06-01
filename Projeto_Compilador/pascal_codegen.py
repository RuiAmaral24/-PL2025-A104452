import os
from pascal_seman import verificar_semantica

# Contador global para gerar labels únicas (FOR0, WHILE1, etc.)
label_counter = 0
# Lista de instruções geradas para o arquivo .vm
output = []
# Mapas globais:
# var_slots: nome_de_variavel -> índice de slot na área global (GP)
var_slots = {}
# var_types: nome_de_variavel -> tipo ('integer','string','boolean')
var_types = {}
# array_bounds: nome_de_array -> tupla (limite_inferior, limite_superior)
array_bounds = {}


def nova_label(prefix="L"):  # Gera um rótulo único com prefixo
    global label_counter
    lbl = f"{prefix}{label_counter}"
    label_counter += 1
    return lbl


def escrever(instr):  # Adiciona uma instrução à lista de output
    output.append(instr)


def gerar_codigo(ast, nome_ficheiro="programa.pas"):

    # Verifica semântica da AST
    verificar_semantica(ast)
    global output, label_counter, var_slots, var_types, array_bounds
    # Reset das estruturas globais
    output.clear()
    label_counter = 0
    var_slots.clear()
    var_types.clear()
    array_bounds.clear()

    # Desestrutura AST: ('program', nome, [decls], bloco)
    _, progName, declaracoes, bloco = ast

    # Alocar variáveis globais
    slot = 0
    for decl_list in declaracoes:
        if not isinstance(decl_list, list):
            continue
        for d in decl_list:
            if d[0] != 'var_decl':
                continue
            # d == ('var_decl', [nomes], tipo)
            _, names, tipo = d
            # Se for array de inteiros não aloca slots apenas registra limites
            if isinstance(tipo, tuple) and tipo[0]=='array' and tipo[3]=='integer':
                low, high = tipo[1], tipo[2]
                array_bounds[names[0]] = (low, high)
            else:
                # Variável simples: integer, string ou boolean
                base = tipo.lower() if isinstance(tipo, str) else 'integer'
                for name in names:
                    var_types[name] = base
                    var_slots[name] = slot
                    # Inicializa o slot com 0 ou string vazia
                    if base == 'string':
                        escrever('pushs ""')  # empilha string vazia
                    else:
                        escrever('pushi 0')   # empilha inteiro 0
                    escrever(f'storeg {slot}')  # armazena em gp[slot]
                    slot += 1

    # Escrever código do programa
    escrever('start')         # início do programa
    gerar_bloco(bloco)        # traduz o bloco principal recursivamente
    escrever('stop')          # fim do programa

    # 3) Gravar na pasta 'codigoVM'
    pasta = 'codigoVM'
    os.makedirs(pasta, exist_ok=True)
    base = os.path.splitext(os.path.basename(nome_ficheiro))[0]
    with open(os.path.join(pasta, base + '.vm'), 'w') as f:
        f.write("\n".join(output))


def gerar_bloco(bloco):
    # bloco == ('block', [instr1, instr2, ...])
    _, instrs = bloco
    for instr in instrs:
        if instr:
            gerar_instr(instr)


def gerar_instr(instr):
    # instr é uma tupla onde instr[0] indica o tipo
    kind = instr[0]

    # Ignora declarações locais
    if kind == 'var_decl':
        return

    # ASSIGN: ('assign', alvo, ':=', expr)
    if kind == 'assign':
        _, target, _, expr = instr
        gerar_expr(expr)                     # gera código
        slot = var_slots[target]             # identifica slot GP
        escrever(f'storeg {slot}')           # armazena resultado

    # READ: ('read', alvo)
    elif kind == 'read':
        _, target = instr
        # ex.: target = ('var','a') ou parecido
        name = target[1] if isinstance(target, tuple) else target
        escrever('read')                    # lê string
        if var_types.get(name) != 'string':  # se não for string
            escrever('atoi')                # converte para inteiro
        slot = var_slots[name]
        escrever(f'storeg {slot}')         # guarda

    # WRITE/WRTIELN: ('write','writeln', [exprs])
    elif kind == 'write':
        _, modo, exprs = instr
        for e in exprs:
            gerar_expr(e)
            if isinstance(e, tuple) and e[0]=='str':
                escrever('writes')            # string
            else:
                escrever('writei')            # inteiro ou booleano
        if modo == 'writeln':
            escrever('writeln')             # newline

    # IF: ('if', cond, then_b, else_b)
    elif kind == 'if':
        _, cond, then_b, else_b = instr
        Lelse = nova_label('ELSE')
        Lend  = nova_label('ENDIF')
        gerar_expr(cond)
        escrever(f'jz {Lelse}')             # se cond==0, vai para else
        gerar_instr(then_b)
        escrever(f'jump {Lend}')            # pula else
        escrever(f'{Lelse}:')               # label ELSE
        if else_b:
            gerar_instr(else_b)
        escrever(f'{Lend}:')                # label ENDIF

    # WHILE: ('while', cond, body)
    elif kind == 'while':
        _, cond, body = instr
        L1 = nova_label('WHILE')
        L2 = nova_label('ENDWHILE')
        escrever(f'{L1}:')                  # label início
        gerar_expr(cond)
        escrever(f'jz {L2}')                # se cond==0 sai
        gerar_instr(body)
        escrever(f'jump {L1}')              # volta ao início
        escrever(f'{L2}:')                  # label fim

    # FOR: ('for', var, start_e, end_e, bloco_for, 'to'/'downto')
    elif kind == 'for':
        _, var, start_e, end_e, bloco_for, dir_ = instr
        # Detecta o padrão como em SomaArray (leitura + acumulador)
        is_array_sum = False
        if start_e[0]=='num' and end_e[0]=='num' and bloco_for[0]=='block':
            seq = bloco_for[1]
            if len(seq)>=2 and seq[0][0]=='read' and seq[1][0]=='assign' and seq[1][1]=='soma':
                is_array_sum = True
        if is_array_sum:
            # contador = end - start + 1
            count = end_e[1] - start_e[1] + 1
            escrever(f'pushi {count}')
            escrever(f'storeg {var_slots[var]}')
            L1 = nova_label('WHILE')
            L2 = nova_label('ENDWHILE')
            escrever(f'{L1}:')
            escrever(f'pushg {var_slots[var]}')
            escrever('pushi 0')
            escrever('sup')
            escrever(f'jz {L2}')
            # corpo: read + soma
            escrever('read')
            escrever('atoi')
            escrever(f'pushg {var_slots["soma"]}')
            escrever('add')
            escrever(f'storeg {var_slots["soma"]}')
            # decrementa contador
            escrever(f'pushg {var_slots[var]}')
            escrever('pushi 1')
            escrever('sub')
            escrever(f'storeg {var_slots[var]}')
            escrever(f'jump {L1}')
            escrever(f'{L2}:')
        else:
            # loop: init, teste, corpo, passo
            gerar_expr(start_e)                # empilha valor inicial
            escrever(f'storeg {var_slots[var]}')
            L1 = nova_label('FOR')
            L2 = nova_label('ENDFOR')
            escrever(f'{L1}:')
            escrever(f'pushg {var_slots[var]}')
            gerar_expr(end_e)
            escrever('supeq' if dir_=='downto' else 'infeq')
            escrever(f'jz {L2}')
            gerar_instr(bloco_for)            # corpo do for
            escrever(f'pushg {var_slots[var]}')
            escrever('pushi 1')
            escrever('sub' if dir_=='downto' else 'add')
            escrever(f'storeg {var_slots[var]}')
            escrever(f'jump {L1}')
            escrever(f'{L2}:')

    # BLOCK: ('block', [instr1, instr2, ...])
    elif kind == 'block':
        for sub in instr[1]:
            if sub:
                gerar_instr(sub)

    else:
        # Qualquer outro tipo de instrução não funciona
        raise NotImplementedError(f'Instrucao {kind} nao suportada')


def gerar_expr(expr):
    # expr é uma tupla com expr[0] indicando o tipo de expressão
    op = expr[0]
    if op=='num':
        escrever(f'pushi {expr[1]}')        # literais inteiros
    elif op=='str':
        s = expr[1]
        if len(s)==1:
            escrever(f'pushi {ord(s)}')     # char como código ASCII
        else:
            escrever(f'pushs "{s}"')      # string literal
    elif op=='var':
        escrever(f'pushg {var_slots[expr[1]]}')  # variável global
    elif op=='array_access':
        # acesso a string no BinPraInt: charat
        _, arr, idx = expr
        escrever(f'pushg {var_slots[arr]}')
        gerar_expr(idx)
        escrever('pushi 1')
        escrever('sub')
        escrever('charat')
    elif op in ('+','-','*','div','mod','=','<>','<','<=','>','>=','and','or'):
        # operadores binários mapeados para opcodes
        m = {'+':'add','-':'sub','*':'mul','div':'div','mod':'mod',
             '=':'equal','<>':'equal; not','<':'inf','<=':'infeq',
             '>':'sup','>=':'supeq','and':'and','or':'or'}[op]
        gerar_expr(expr[1])
        gerar_expr(expr[2])
        for c in m.split(';'):
            escrever(c)
    elif op=='not':
        gerar_expr(expr[1])
        escrever('not') # negaçao
    elif op=='bool':
        escrever('pushi ' + ('1' if expr[1] else '0'))  # booleano
    elif op=='call':
        # só length em strings é suportado
        if expr[1].lower()=='length':
            gerar_expr(expr[2][0])
            escrever('strlen')
        else:
            raise NotImplementedError('call nao suportado')
    else:
        raise NotImplementedError(f'Expressao {op} nao suportada')
