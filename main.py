from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from glpi import criar_chamado, buscar_id_por_nome, buscar_id_usuario_por_login_ou_email

app = FastAPI()

MAPA_CATEGORIAS_TI = {
    "1": {  # Acessos
        "nome": "Acessos",
        "subcategorias": {
            "1": {"nome": "Equipamento", "id": 270},
            "2": {"nome": "Pacote Office", "id": 269},
            "3": {"nome": "Sistemas", "id": 271},
            "4": {"nome": "Software", "id": 272},
        }
    },

    "2": {  # Manutenção
        "nome": "Manutenção",
        "subcategorias": {
            "1": {"nome": "Câmera", "id": 278},
            "2": {"nome": "Catraca", "id": 279},
            "3": {"nome": "Conserto de equipamento", "id": 275},
            "4": {"nome": "Impressora", "id": 277},
            "5": {"nome": "Movimentação de equipamento", "id": 276},
            "6": {"nome": "Troca de equipamento", "id": 274},
        }
    },

    "3": {  # Infraestrutura
        "nome": "Infraestrutura",
        "subcategorias": {
            "1": {"nome": "Rede", "id": 280},
            "2": {"nome": "Telefonia", "id": 282},
            "3": {"nome": "Wifi", "id": 281},
        }
    }
}

MAPA_CATEGORIAS_ENGENHARIA_PATRIMONIO= {
    "1": {  # Equipamentos e mobiliário
        "nome": "Equipamentos e mobiliário",
        "subcategorias": {
            "1": {"nome": "Movimentação", "id": 345},
            "2": {"nome": "Troca", "id": 346},
            "3": {"nome": "Devolução", "id": 347},
        }
    },

    "2": {  # Manutenção de equipamentos
        "nome": "Manutenção de equipamentos",
        "subcategorias": {
            "1": {"nome": "Corretiva", "id": 348},
            "2": {"nome": "Preventiva", "id": 349},
        }
    },

    "3": {  # Solicitação
        "nome": "Solicitação",
        "subcategorias": {
            "1": {"nome": "Equipamentos e mobiliário", "id": 350},
            "2": {"nome": "Treinamento", "id": 351},
            "3": {"nome": "Utilização em Ações/Campanhas", "id": 352},
        }
    }
}

MAPA_CATEGORIAS_MANUTENCAO = {
    "1": {
        "nome": "Manutenção",
        "id": 132
    },

    "2": {
        "nome": "Limpeza / Higienização",
        "id": 341
    },
    "3":{
        "nome": "Hospitalidade",
        "id": 397
    }
}

MAPA_CATEGORIAS_FINANCEIRO = {
    "1": {
        "nome": "Solicitação",
        "subcategorias": {
            "1": {"nome": "Reembolso", "id": 332},
            "2": {"nome": "Pagamentos urgentes a fornecedores", "id": 333},
            "3": {"nome": "Antecipação a fornecedores", "id": 334},
            "4": {"nome": "Cadastro de cartão corporativo", "id": 335},
            "5": {"nome": "Aumento de limite para cartão corporativo", "id": 336},
        }
    },

    "2": {
        "nome": "Informações",
        "subcategorias": {
            "1": {"nome": "Alteração de dados bancários", "id": 337},
            "2": {"nome": "Consulta de status de pagamento", "id": 338},
            "3": {"nome": "Comprovante de pagamento", "id": 339},
            "4": {"nome": "Pagamento aos médicos", "id": 340},
        }
    }
}

MAPA_CATEGORIAS_SUPRIMENTOS = {
    "1": {
        "nome": "Solicitação de compra",
        "id": 365
    },

    "2": {
        "nome": "Solicitação de contratação de serviço",
        "id": 366
    },

    "3": {
        "nome": "Solicitação de orçamento",
        "id": 367
    }
}

MAPA_CATEGORIAS_JURIDICO = {
    "1": {
        "nome": "Contratos",
        "subcategorias": {
            "1": {"nome": "Análise", "id": 311},
            "2": {"nome": "Criação", "id": 312},
            "3": {"nome": "Aditivação/errata", "id": 317},
            "4": {"nome": "Distrato", "id": 318},
        }
    },

    "2": {
        "nome": "Parecer jurídico",
        "id": 313
    },

    "3": {
        "nome": "Editais de cotações",
        "subcategorias": {
            "1": {"nome": "Emenda parlamentar", "id": 319},
            "2": {"nome": "MIROSC", "id": 320},
            "3": {"nome": "Outros", "id": 321},
        }
    },

    "4": {
        "nome": "Solicitação de ofícios",
        "subcategorias": {
            "1": {"nome": "Comunicação externa", "id": 322},
            "2": {"nome": "Resposta a pedido oficial", "id": 323},
            "3": {"nome": "Outros", "id": 324},
        }
    },

    "5": {
        "nome": "Solicitação de prontuário médico / demanda de paciente",
        "subcategorias": {
            "1": {"nome": "Acesso a prontuário", "id": 325},
            "2": {"nome": "Solicitação de cópia de prontuário", "id": 326},
            "3": {"nome": "Correção de dados médicos", "id": 327},
            "4": {"nome": "Relatório médico", "id": 328},
            "5": {"nome": "Outros", "id": 329},
        }
    }
}

MAPA_CATEGORIAS_RH = {
    "1": {
        "nome": "Programação de férias (CLT)",
        "subcategorias": {
            "1": {"nome": "Novo período", "id": 357},
            "2": {"nome": "Alteração de data", "id": 358},
            "3": {"nome": "Cancelamento de data", "id": 359},
        }
    },

    "2": {
        "nome": "Plano de saúde e/ou odontológico",
        "subcategorias": {
            "1": {"nome": "Inclusão", "id": 360},
            "2": {"nome": "Alteração", "id": 361},
            "3": {"nome": "Exclusão", "id": 362},
        }
    },

    "3": {
        "nome": "Entrega de atestado",
        "subcategorias": {
            "1": {"nome": "Atestado médico", "id": 363},
            "2": {"nome": "Afastamento previdenciário", "id": 364},
        }
    },

    "4": {
        "nome": "Envio das notas fiscais PJ",
        "id": 356
    }
}

MAPA_CATEGORIAS_MARKETING = {
    "1": {
        "nome": "Marketing",
        "subcategorias": {
            "1": {"nome": "Apresentações institucionais", "id": 371},
            "2": {"nome": "Peças gráficas", "id": 372},
            "3": {"nome": "Campanhas", "id": 373},
            "4": {"nome": "Materiais promocionais", "id": 374},
            "5": {"nome": "Identidade visual", "id": 375},
            "6": {"nome": "Folders", "id": 376},
            "7": {"nome": "Banners", "id": 377},
            "8": {"nome": "Brindes", "id": 378},
            "9": {"nome": "Outros", "id": 379},
        }
    },

    "2": {
        "nome": "Comunicados oficiais",
        "subcategorias": {
            "1": {"nome": "Comunicados internos", "id": 387},
            "2": {"nome": "Avisos corporativos", "id": 388},
            "3": {"nome": "E-mails institucionais", "id": 389},
            "4": {"nome": "Notas oficiais", "id": 390},
            "5": {"nome": "Campanhas internas", "id": 391},
            "6": {"nome": "Mensagens da diretoria", "id": 392},
            "7": {"nome": "Comunicados organizacionais", "id": 393},
        }
    },

    "3": {
        "nome": "Inclusão de documentos/arquivos Portal interno de Comunicação",
        "subcategorias": {
            "1": {"nome": "Inclusão", "id": 380},
            "2": {"nome": "Atualização / substituição de documentos", "id": 381},
            "3": {"nome": "Políticas", "id": 382},
            "4": {"nome": "Procedimentos", "id": 383},
            "5": {"nome": "Treinamentos", "id": 384},
            "6": {"nome": "Comunicados", "id": 385},
            "7": {"nome": "Vídeos e demais arquivos na plataforma", "id": 386},
        }
    }
}

MAPA_FORMULARIOS = {
    "1": "Serviços de TI",
    "2": "Engenharia clínica / Patrimônio",
    "3": "Manutenção",
    "4": "Financeiro",
    "5": "Suprimentos",
    "6": "Jurídico",
    "7": "Recursos Humanos",
    "8": "Marketing"
}

MAPA_TIPOS = {
    "1": {
        "nome": "Incidente",
        "id": 1
    },
    "2": {
        "nome": "Requisição",
        "id": 2
    }
}

MAPA_URGENCIAS = {
    "1": {
        "nome": "Muito alta",
        "id": 5
    },
    "2": {
        "nome": "Alta",
        "id": 4
    },
    "3": {
        "nome": "Média",
        "id": 3
    },
    "4": {
        "nome": "Baixa",
        "id": 2
    },
    "5": {
        "nome": "Muito baixa",
        "id": 1
    }
}

MAPA_LOCALIZACOES = {
    "1": "Unidade C",
    "2": "0 Sobreloja Unidade A",
    "3": "0 Térreo Unidade A",
    "4": "1 Andar Unidade A",
    "5": "2 Andar Unidade A",
    "6": "3 Andar Unidade A",
    "7": "4 Andar Unidade A",
    "8": "5 Andar Unidade A",
    "9": "6 Andar Unidade A",
    "10": "7 Andar Unidade A",
    "11": "8 Andar Unidade A",
    "12": "9 Andar Unidade A",
    "13": "0 Andar Unidade B",
    "14": "1 Andar Unidade B",
    "15": "2 Andar Unidade B",
    "16": "3 Andar Unidade B",
    "17": "4 Andar Unidade B",
    "18": "5 Andar Unidade B",
    "19": "6 Andar Unidade B",
    "20": "Campanhas",
    "21": "Unidade Principal"
}

MAPA_ENTIDADES = {
    "1": 0,   # Serviços de TI → Entidade raiz
    "2": 3,   # Engenharia clínica / Patrimônio
    "3": 1,   # Manutenção
    "4": 8,   # Financeiro
    "5": 10,  # Suprimentos
    "6": 9,   # Jurídico
    "7": 7,   # Recursos Humanos
    "8": 11   # Marketing
}

MAPAS_CATEGORIAS = {
    "1": MAPA_CATEGORIAS_TI,
    "2": MAPA_CATEGORIAS_ENGENHARIA_PATRIMONIO,
    "3": MAPA_CATEGORIAS_MANUTENCAO,
    "4": MAPA_CATEGORIAS_FINANCEIRO,
    "5": MAPA_CATEGORIAS_SUPRIMENTOS,
    "6": MAPA_CATEGORIAS_JURIDICO,
    "7": MAPA_CATEGORIAS_RH,
    "8": MAPA_CATEGORIAS_MARKETING,
}

class ChamadoRequest(BaseModel):
    formulario: str
    urgencia: str
    categoria: str
    subcategoria: str | None = None
    localizacao: str
    requerente: str
    titulo: str | None = None
    descricao: str
    teamviewer: str | None = None

class UsuarioRequest(BaseModel):
    requerente: str

@app.post("/validar-usuario")
def validar_usuario(dados: UsuarioRequest):
    try:
        requerente_id = buscar_id_usuario_por_login_ou_email(dados.requerente)
        return {
            "valido": True,
            "mensagem": "Usuário encontrado",
            "usuario_id": requerente_id
        }
    except Exception:
        return {
            "valido": False,
            "mensagem": "Usuário não encontrado. Verifique o login e tente novamente.",
            "usuario_id": None
        }

@app.post("/criar-chamado")
def criar_chamado_api(dados: ChamadoRequest):


    # =========================
    # FORMULÁRIO / ÁREA
    # =========================
    formulario_nome = MAPA_FORMULARIOS.get(
        str(dados.formulario),
        dados.formulario
    )

    # =========================
    # TIPO DE REQUISIÇÃO PADRÃO
    # =========================

    tipo = {
        "nome": "Requisição",
        "id": 2
    }
    # =========================
    # URGÊNCIA
    # =========================
    urgencia = MAPA_URGENCIAS.get(str(dados.urgencia))

    if not urgencia:
        raise HTTPException(
            status_code=400,
            detail="Urgência inválida"
        )

    # =========================
    # MAPA DE CATEGORIAS DA ÁREA
    # =========================
    mapa_categorias = MAPAS_CATEGORIAS.get(
        str(dados.formulario)
    )

    if not mapa_categorias:
        raise HTTPException(
            status_code=400,
            detail="Área sem categorias configuradas"
        )

    # =========================
    # CATEGORIA
    # =========================
    categoria = mapa_categorias.get(
        str(dados.categoria)
    )

    if not categoria:
        raise HTTPException(
            status_code=400,
            detail="Categoria inválida"
        )

    # =========================
    # CATEGORIA COM OU SEM SUBCATEGORIA
    # =========================
    if "subcategorias" in categoria:

        subcategoria = categoria["subcategorias"].get(
            str(dados.subcategoria)
        )

        if not subcategoria:
            raise HTTPException(
                status_code=400,
                detail="Subcategoria inválida"
            )

        categoria_nome = categoria["nome"]
        subcategoria_nome = subcategoria["nome"]

        # ID final enviado ao GLPI
        categoria_id = subcategoria["id"]

    else:
        categoria_nome = categoria["nome"]
        subcategoria_nome = None

        # Se não existe subcategoria,
        # utiliza o ID da própria categoria
        categoria_id = categoria["id"]

    # =========================
    # ENTIDADE
    # =========================
    entidade_id = MAPA_ENTIDADES.get(
        str(dados.formulario),
        0
    )

    # =========================
    # LOCALIZAÇÃO
    # =========================
    localizacao_recebida = MAPA_LOCALIZACOES.get(
        str(dados.localizacao),
        dados.localizacao
    )

    localizacao_id = buscar_id_por_nome(
        "Location",
        localizacao_recebida
    )

    # =========================
    # REQUERENTE
    # =========================
    requerente_id = buscar_id_usuario_por_login_ou_email(
        dados.requerente
    )


    # =========================
    # TÍTULO AUTOMÁTICO
    # =========================

    if subcategoria_nome:
        titulo = f"(chatbot) {categoria_nome} - {subcategoria_nome}"
    else:
        titulo = f"(chatbot) {categoria_nome}"

    # =========================
    # TEAMVIEWER
    # =========================
    teamviewer = dados.teamviewer or "Não informado"

    # =========================
    # DESCRIÇÃO
    # =========================

    # Só mostra Subcategoria se houver uma
    texto_subcategoria = ""

    if subcategoria_nome:
        texto_subcategoria = f"Subcategoria: {subcategoria_nome}\n"

    descricao = f"""
Formulário: {formulario_nome}

Tipo de requisição: {tipo["nome"]}
Categoria: {categoria_nome}
{texto_subcategoria}Urgência: {urgencia["nome"]}
Localização: {localizacao_recebida}

TeamViewer:
{teamviewer}

Descrição:
{dados.descricao}
"""

    # =========================
    # CRIA O CHAMADO NO GLPI
    # =========================
    resultado = criar_chamado(
        titulo,
        descricao,
        categoria_id,
        localizacao_id,
        requerente_id,
        entidade_id,
        tipo["id"],
        urgencia["id"]
    )

    return {
        "mensagem": "Chamado criado com sucesso",
        "resultado": resultado
    }