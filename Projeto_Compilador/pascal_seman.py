class ErroSemantico(Exception):
    pass

def verificar_semantica(ast):
    contexto = {
        'variaveis': {},  # nome -> tipo (por agora, só usa string, integer, boolean)
        'funcoes': {
            'length': 1, 'ord': 1, 'chr': 1,
            'pred': 1, 'succ': 1, 'abs': 1,
            'sqr': 1, 'sqrt': 1, 'round': 1, 'trunc': 1
        }
    }
    analisar_programa(ast, contexto)

def analisar_programa(ast, contexto):
    tipo, nome, declaracoes, bloco = ast

    # Primeira passagem: regista variáveis globais e funções
    for decl in declaracoes:
        if isinstance(decl, list):
            for d in decl:
                if d[0] == 'var_decl':
                    for var in d[1]:
                        contexto['variaveis'][var] = normalizar_tipo(d[2])
                elif d[0] == 'function':
                    nome_func = d[1]
                    params = d[2]
                    contexto['funcoes'][nome_func] = len(params)

    # Segunda passagem: analisar corpo das funções
    for decl in declaracoes:
        if isinstance(decl, list):
            for d in decl:
                if d[0] == 'function':
                    nome_func, params, tipo_retorno, func_decls, func_bloco = d[1:]
                    contexto_func = {
                        'variaveis': dict(contexto['variaveis']),  # herda variáveis globais
                        'funcoes': contexto['funcoes']
                    }
                    # adicionar parâmetros
                    for p in params:
                        for nome_param in p[1]:
                            contexto_func['variaveis'][nome_param] = normalizar_tipo(p[2])
                    # adicionar variáveis locais
                    for decl_interna in func_decls:
                        for vd in decl_interna:
                            if vd[0] == 'var_decl':
                                for var in vd[1]:
                                    contexto_func['variaveis'][var] = normalizar_tipo(vd[2])
                    # nome da função como variável (para atribuição do resultado)
                    contexto_func['variaveis'][nome_func] = normalizar_tipo(tipo_retorno)
                    analisar_bloco(func_bloco, contexto_func)

    analisar_bloco(bloco, contexto)

def normalizar_tipo(tipo):
    if isinstance(tipo, str):
        return tipo.lower()
    elif isinstance(tipo, tuple) and tipo[0] == 'array':
        return ('array', tipo[1], tipo[2], normalizar_tipo(tipo[3]))
    return tipo

def analisar_bloco(bloco, contexto):
    _, instrucoes = bloco
    for instr in instrucoes:
        if instr is not None:
            analisar_instrucao(instr, contexto)

def analisar_instrucao(instr, contexto):
    tipo = instr[0]

    if tipo == 'assign':
        _, var, _, expr = instr
        if isinstance(var, str):
            if var not in contexto['variaveis']:
                raise ErroSemantico(f"Variável '{var}' não declarada")
        elif isinstance(var, tuple):
            analisar_expressao(var, contexto)
        analisar_expressao(expr, contexto)

    elif tipo == 'read':
        _, var = instr
        if isinstance(var, tuple):
            analisar_expressao(var, contexto)
        elif isinstance(var, str):
            if var not in contexto['variaveis']:
                raise ErroSemantico(f"Variável '{var}' não declarada")

    elif tipo == 'write':
        _, _, exprs = instr
        for expr in exprs:
            analisar_expressao(expr, contexto)

    elif tipo == 'if':
        _, cond, then_instr, else_instr = instr
        tipo_cond = analisar_expressao(cond, contexto)
        if tipo_cond != 'boolean':
            raise ErroSemantico(f"A condição do IF deve ser booleana (recebido: {tipo_cond})")
        analisar_instrucao(then_instr, contexto)
        if else_instr:
            analisar_instrucao(else_instr, contexto)

    elif tipo == 'while':
        _, cond, corpo = instr
        tipo_cond = analisar_expressao(cond, contexto)
        if tipo_cond != 'boolean':
            raise ErroSemantico(f"A condição do WHILE deve ser booleana (recebido: {tipo_cond})")
        analisar_instrucao(corpo, contexto)

    elif tipo == 'for':
        _, var, inicio, fim, corpo, direcao = instr
        analisar_expressao(inicio, contexto)
        analisar_expressao(fim, contexto)
        analisar_instrucao(corpo, contexto)

    elif tipo == 'block':
        _, instrs = instr
        for i in instrs:
            if i is not None:
                analisar_instrucao(i, contexto)

    else:
        print(f"Instrução desconhecida: {instr}")

def analisar_expressao(expr, contexto):
    if not isinstance(expr, tuple):
        return inferir_tipo_literal(expr)

    tipo = expr[0]

    if tipo == 'var':
        nome = expr[1]
        if nome not in contexto['variaveis']:
            raise ErroSemantico(f"Variável '{nome}' não declarada")
        return contexto['variaveis'][nome]

    elif tipo == 'array_access':
        nome, indice = expr[1], expr[2]
        if nome not in contexto['variaveis']:
            raise ErroSemantico(f"Array '{nome}' não declarado")
        analisar_expressao(indice, contexto)
        tipo_array = contexto['variaveis'][nome]
        if isinstance(tipo_array, tuple) and tipo_array[0] == 'array':
            return tipo_array[3]
        return tipo_array

    elif tipo == 'call':
        nome, argumentos = expr[1], expr[2]
        if nome not in contexto['funcoes']:
            raise ErroSemantico(f"Função '{nome}' não declarada")
        esperados = contexto['funcoes'][nome]
        if len(argumentos) != esperados:
            raise ErroSemantico(f"Função '{nome}' chamada com {len(argumentos)} argumento(s), mas esperava {esperados}")
        for arg in argumentos:
            analisar_expressao(arg, contexto)
        return 'integer'

    elif tipo in ('+', '-', '*', 'div', 'mod'):
        t1 = analisar_expressao(expr[1], contexto)
        t2 = analisar_expressao(expr[2], contexto)
        if t1 == t2 == 'integer':
            return 'integer'
        raise ErroSemantico(f"Operação aritmética inválida entre {t1} e {t2}")

    elif tipo in ('=', '<>', '<', '<=', '>', '>='):
        t1 = analisar_expressao(expr[1], contexto)
        t2 = analisar_expressao(expr[2], contexto)
        if t1 != t2:
            raise ErroSemantico(f"Comparação entre tipos diferentes: {t1} e {t2}")
        return 'boolean'

    elif tipo in ('and', 'or'):
        t1 = analisar_expressao(expr[1], contexto)
        t2 = analisar_expressao(expr[2], contexto)
        if t1 == t2 == 'boolean':
            return 'boolean'
        raise ErroSemantico(f"Operação lógica inválida entre {t1} e {t2}")

    elif tipo == 'not':
        t = analisar_expressao(expr[1], contexto)
        if t != 'boolean':
            raise ErroSemantico(f"'not' aplicado a tipo inválido: {t}")
        return 'boolean'

    elif tipo == 'str':
        return 'string'
    elif tipo == 'num':
        return 'integer'
    elif tipo == 'bool':
        return 'boolean'

    raise ErroSemantico(f"Expressão desconhecida: {expr}")

def inferir_tipo_literal(expr):
    if isinstance(expr, int):
        return 'integer'
    elif isinstance(expr, float):
        return 'real'
    elif isinstance(expr, bool):
        return 'boolean'
    elif isinstance(expr, str):
        return 'string'
    return 'unknown'
