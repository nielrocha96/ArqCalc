# EDITADO - ABRIL/5
import logging
logger = logging.getLogger(__name__)

from datetime import datetime
import json

from django.http import HttpResponse
from .services.pdf_service import ArqCalcReporter

from django.utils.text import slugify

from django.http                    import JsonResponse
from django.shortcuts               import render, redirect, get_object_or_404
from django.contrib.auth            import authenticate, login#, get_user_model
from django.contrib.auth.views      import PasswordResetView
from django.contrib                 import messages
from django.contrib.auth.models     import User
from django.core.paginator          import Paginator
from django.contrib.auth.decorators import login_required
from django.urls                    import reverse_lazy
from django.views                   import View
from django.template.loader import render_to_string

from arqcalc_webapp.models import ProjectCosts

from .services.table_service import TablePresenter

def login_view(request):
    if request.user.is_authenticated: return redirect('projetos')
    
    if request.method == "POST":
        email    = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'E-mail e/ou senha inválido(s).')
            return render(request, "login.html",{"email": email})

    return render(request, 'login.html')

def cadastro_view(request):
    if request.method == "POST":
        email     = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Validação simples
        if not email or not password1 or not password2:
            messages.error(request, "Por favor, preencha todos os campos.")
            return render(request, "cadastro.html",{"email": email})

        if password1 != password2:
            messages.error(request, "As senhas não coincidem.")
            return render(request, "cadastro.html",{"email": email})

        # Verificar se email já existe (User usa username, mas podemos usar email no lugar)
        if User.objects.filter(email=email).exists():
            messages.error(request, "Já existe uma conta com este e-mail.")
            return render(request, "cadastro.html",{"email": email})

        # Criar usuário - usar email como username
        user = User.objects.create_user(username=email, email=email, password=password1)
        user.save()

        messages.success(request, "Cadastro realizado com sucesso! Faça login.")
        return redirect('login')  # redireciona para página de login

    # GET: só renderiza o formulário
    return render(request, "cadastro.html")

#___________________________________________________________________
#                         NOVO PROJETO
# __________________________________________________________________
@login_required(login_url='login')
def novo_projeto_view(request):
    modo = request.GET.get('modo', 'create')
    project_id = request.GET.get('id')


    

    # Pegando todos os custos de um projeto específico
    # custos_projeto = ProjectCosts.objects.filter(project_id=project_id)

    # Para transformar isso em uma lista de dicionários (como no seu Mock Data):
    # db_data_custos = list(custos_projeto.values('id', 'description', 'value'))

    usuario = {
        "username": "Deivid Hernandez",
        "position": "Engenheiro",
    }

    # Mock Data
    # Subistituir o valor de cada atributo custo, profissional, etapa, resumo e preco pelo valor buscado no db, como o db_data_custos por exemplo.
    db_data = { 
        "dados": {
            "project_name" : 'Construção Centro Espacial',
            "customer_name": 'Roberto Carlos',
            'account_name': 'Raul Gil',
            'start_date' : datetime(2026, 3, 10),
            'end_date' : datetime(2026, 6, 20),
            'status': 'Reprovado',
            'cep': '12700-000',
            'street': 'João Resende',
            'street_additional': 'Frente ao mercadinho',
            'neighborhood': 'Turquias',
            'city': 'Megalopolis',
            'state': 'SP',
            'country': 'Brasil',
            'size': '22.2',
            'project_type': 'Arquitetônico',
            'classification_project': 'Reforma',
            'category_project': 'Comercial',
        },

        "custo": [
            {'id': 1, 'name': 'Servidor AWS', 'cost_value': 500.00}, 
            {'id': 2, 'name': 'Implememtação AWS', 'cost_value': 100.00}, 
        ],
       
        "profissional": [
            {'id': 1, 'person__name': 'Luiz', 'position': 'Dev Fullstack', 'valor_hour': 150.00},
            {'id': 2, 'person__name': 'Ana', 'position': 'Designer', 'valor_hour': 120.00},
        ],

        "etapa": {
            # Campo fora da lista de etapas, mas dentro da tab
            'style_project': 'Simplificado', 
            
            # 'templates' reflete a lógica de PhasesTemplates no seu models.py
            'templates': [
                {
                    'id': 1,
                    'template_name': 'Template Residencial',
                    # 'phases' reflete o modelo ProjectPhases / Phases
                    'phases': [
                        # {
                        #     'id': 10, # ID da Phase
                        #     'name': 'Levantamento',
                        #     'professional_selected': 'Luiz Silva', # Simulando o select do profissional
                            
                        #     # 'items' reflete o modelo PhasesTemplatesItems do models.py
                        #     'items': [
                        #         {
                        #             'id': 101,
                        #             'cells': [
                        #                 {'name': 'item', 'value': 'Medição in loco'},
                        #                 {'name': 'responsible', 'value': 'Luiz Silva'}, # Vinculado ao select
                        #                 {'name': 'time', 'value': '04:00'},
                        #                 {'name': 'total_item', 'value': 4.0}
                        #             ]
                        #         },
                        #         {
                        #             'id': 102,
                        #             'cells': [
                        #                 {'name': 'item', 'value': 'Desenho Técnico'},
                        #                 {'name': 'responsible', 'value': 'Ricardo M.'},
                        #                 {'name': 'time', 'value': '08:00'},
                        #                 {'name': 'total_item', 'value': 8.0}
                        #             ]
                        #         }
                        #     ]
                        # },
                        # {
                        #     'id': 11,
                        #     'name': 'Criação / Estudo Preliminar',
                        #     'professional_selected': 'Juliana Costa',
                        #     'items': [
                        #         {
                        #             'id': 103,
                        #             'cells': [
                        #                 {'name': 'item', 'value': 'Moodboard'},
                        #                 {'name': 'responsible', 'value': 'Juliana Costa'},
                        #                 {'name': 'time', 'value': '02:00'},
                        #                 {'name': 'total_item', 'value': 2.0}
                        #             ]
                        #         }
                        #     ]
                        # }
                    ]
                }
            ],
        },

        "resumo": [
            {'id': 1, 'item': 'parede',  'nome': 'Luiz', 'time': '5', 'total_item': 3},
            {'id': 2, 'item': 'piso', 'responsible': 'Juliana', 'time': '10', 'total_item': 2},
        ],

       "preco": [
            {'id': 1, 'description': 'Servidor AWS', 'cost_value': 500.00}, 
            {'id': 2, 'description': 'Implememtação AWS', 'cost_value': 100.00}, 
            {'id': 3, 'description': 'Servidor AWS', 'cost_value': 500.00}, 
            {'id': 4, 'description': 'Implememtação AWS', 'cost_value': 100.00}, 
        ],

    }

    custos_fixos = [
        {'id': 1, 'description': 'Custo Fixo 1', 'value': 1000.00},
        {'id': 2, 'description': 'Custo Fixo 2', 'value': 2000.00},
        {'id': 3, 'description': 'Custo Fixo 3', 'value': 1500.00},
        {'id': 4, 'description': 'Custo Fixo 4', 'value': 3000.00},
        {'id': 5, 'description': 'Custo Fixo 5', 'value': 2500.00},
        {'id': 6, 'description': 'Custo Fixo 6', 'value': 1800.00},
        {'id': 7, 'description': 'Custo Fixo 7', 'value': 2200.00},
    ]

    impostos_mock = [
        {'id': 1, 'description': 'ISS', 'value': 5.00}, # valor pode ser % ou fixo, dependendo da sua lógica JS
        {'id': 2, 'description': 'ICMS', 'value': 18.00},
        {'id': 3, 'description': 'Simples Nacional', 'value': 6.00},
    ]

    lista_custos_fixos = [
        {'id': c['id'], 'description': c['description'], 'value': c['value']} 
        for c in custos_fixos
    ]

    lista_impostos = [
        {'id': i['id'], 'description': i['description'], 'value': i['value']} 
        for i in impostos_mock
    ]


    tab_config = {
        "dados": {
            "headers": [""],
            "lists": {
                'content': {
                    "status": ['Aprovado', 'Aguardando resposta', 'Em andamento', 'Reprovado'],
                    "project_type": ['Residencial', 'Industrial', 'Arquitetônico', 'Outros'],
                    "classification": ['Novo', 'Reforma'],
                    "category": ['Residencial', 'Comercial'],
                }
            }
        },
        "custo":        {"headers": ['DESCRIÇÃO', 'VALOR'], "lists": {}},
        "profissional": {"headers": ["NOME", "CARGO", "VALOR"], "lists": {}},

        "etapa": {
            "headers": ['Item', 'Responsável', 'Tempo', 'Total Do Item'], 
            "lists":   {'content': {'style_project': ['Padrão', 'Simplificado', 'Completo']}}
        },

        "resumo": {"headers": ['Total (h)', 'Cargo', 'Custo', 'Proporção de   Custo'], "lists": {}},
        "preco":  {"headers": [''],  "lists": {}},
    }

    
    
    field_mapping = {
        "custo": ['name', 'cost_value'],
        "profissional": ['person__name', 'position', 'valor_hour'],
        "etapa": ['item', 'responsible', 'time', 'total_item'],
        "resumo": ['item', 'nome', 'time', 'total_item'],
        "preco": ['description', 'cost_value', ],
    }
    context_data = {}

    for key, fields in field_mapping.items():
        raw_data = db_data.get(key, [])
        
        if key == "etapa" and isinstance(raw_data, dict):
            # Processamento especial para a estrutura aninhada de Etapas
            processed_etapa = {
                "style_project": raw_data.get("style_project", "Padrão"),
                "templates": []
            }
            
            for template in raw_data.get("templates", []):
                new_template = {"phases": []}
                for phase in template.get("phases", []):
                    # Formatamos os itens da fase individualmente usando o TablePresenter
                    formatted_items = TablePresenter.format_collection(phase.get("items", []), fields)
                    
                    new_template["phases"].append({
                        "id": phase.get("id"),
                        "name": phase.get("name"),
                        "professional_selected": phase.get("professional_selected"),
                        "items": formatted_items 
                    })
                processed_etapa["templates"].append(new_template)
            
            context_data[key] = processed_etapa
        else:
            # Processamento padrão para listas simples (Custo, Profissional, etc)
            context_data[key] = TablePresenter.format_collection(raw_data, fields)
    
    comissoes = 2

    # variável para controle de exibição do banner - ajustar lógica conforme necessário

    banner = "False" 
   
    context = {
        'screen': 'Novo Projeto',
        "usuario": usuario,
        "tab_config": tab_config,
        "custo" :[ {
                'id': 'temp-1',
                'cells': [
                    { "name": "name",  'value': ''},
                    { "name": "cost_value",  'value': ''},
                ]
            }],
        "profissional": [{
            'id':'temp-1',
            'cells':[{"name": "nome",       "value": "", "is_status": False},
                     {"name": "position",   "value": "", "is_status": False},
                     {"name": "value_hour", "value": '', "is_status": False}
                    ]
        }],
         "etapa": {
            # Campo fora da lista de etapas, mas dentro da tab
            'style_project': 'Padrão', 
            
            # 'templates' reflete a lógica de PhasesTemplates no seu models.py
            'templates': [
                {
                    'id': 1,
                    'template_name': 'Template Residencial',
                    # 'phases' reflete o modelo ProjectPhases / Phases
                    'phases': [
                        {
                            'id': 1, # ID da Phase
                            'name': '',
                            'professional_selected': '', # Simulando o select do profissional
                            
                            # 'items' reflete o modelo PhasesTemplatesItems do models.py
                            'items': [
                                {
                                    'id': 'temp-101',
                                    'cells': [
                                        {'name': 'item', 'value': ''},
                                        {'name': 'responsible', 'value': ''}, # Vinculado ao select
                                        {'name': 'time', 'value': ''},
                                        {'name': 'total_item', 'value': ''}
                                    ]
                                },
                               
                            ]
                        },
                        
                    ]
                }
            ],
        },
        "preco" : [],
        "lista_custos_fixos": lista_custos_fixos,
        "lista_impostos": lista_impostos,
        "comissoes": comissoes,
        "banner": banner,
        "create": 'true',
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        context_data = {
            "titulo": "Clonar Projeto",
            "corpo": "Tem certeza que deseja clonar esta etapa?",
            "botoes": {
                "confirm": {"texto": "Confirmar", "class": "btn_copy_confirmation"},
                "cancel":  {"texto": "Cancelar", "class": "btn_primary"},
            }
        }
        return JsonResponse(context_data)

    if modo == 'edit':
        # Lógica para garantir que a estrutura de etapas e fases esteja sempre presente, mesmo que vazia, para evitar erros de renderização no front
        if not context_data["etapa"]["templates"][0] or len(context_data["etapa"]["templates"][0]["phases"]) == 0:
            # Se não houver fases, adiciona uma fase temporária para renderizar o bloco no front
            context_data["etapa"]["templates"][0]["phases"].append({
                'id': 'temp-1',
                'name': '',
                'professional_selected': '',
                'items': [
                    {
                        'id': 'temp-101',
                        'cells': [
                            {'name': 'item', 'value': ''},
                            {'name': 'responsible', 'value': ''},
                            {'name': 'time', 'value': ''},
                            {'name': 'total_item', 'value': ''}
                        ]
                    }
                ]
            })
        
        context = {
            'screen':       'Editar Projeto',
            "usuario":      usuario,
            "tab_config":   tab_config,
            "dados": db_data["dados"] ,
            "custo" :       context_data["custo"],
            "profissional": context_data["profissional"],
            "etapa" :       context_data["etapa"],
            "resumo":       context_data["resumo"],
            "preco" :       context_data["preco"],
            "lista_custos_fixos": lista_custos_fixos, # DEVE SER SUBSTITUÍDO PELO VALOR VINDO DO PROJETO, COM BASE NO project_id
            "lista_impostos": lista_impostos,
            "comissoes": comissoes,
            "banner": banner,
            "edit": 'true',
        }
    if modo == 'copy':
        context = {
            'screen':       'Copiar Projeto',
            "usuario":      usuario,
            "tab_config":   tab_config,
            "dados": db_data["dados"] ,
            "custo" :       context_data["custo"],
            "profissional": context_data["profissional"],
            "etapa" :       context_data["etapa"],
            "resumo":       context_data["resumo"],
            "preco" :       context_data["preco"],
            "lista_custos_fixos": lista_custos_fixos,
            "lista_impostos": lista_impostos,
            "comissoes": comissoes,
            "banner": banner,
            "copy": 'true',
        }

    return render(request, "novo_projeto.html", context)

# ______________________________________________________________________________
#                                   PROJETOS
# ______________________________________________________________________________
@login_required(login_url='login')
def projetos_view(request):
    # Se quiser passar dados dinâmicos, pode incluí-los no contexto
    f_account_name = request.GET.get('account_name', '').strip()
    f_description = request.GET.get('description', '').strip()
    f_project_name = request.GET.get('project_name', '').strip()
    f_status       = request.GET.get('status_input', '').strip()
    f_date_start   = request.GET.get('date_start', '').strip()
    f_date_end     = request.GET.get('date_end', '').strip()
    
    search_client = request.GET.get('search', '').strip()
    
    usuario = {
        "username": "Deivid Hernandez",
        "position": "Engenheiro",
    }
    
    data_list = [
        {
            "id": 1,
            "project_name": "Usina",
            "description": "Expansão de usina solar.",
            "account_name": "Mariana Silva",
            "start_date": "01/02/2026",
            "end_date": "15/05/2026",
            "status": "Aprovado",
        },
        {
            "id": 2,
            "project_name": "Sistema de Segurança",
            "description": "Implantação de sistema de segurança.",
            "account_name": "Marcos Oliveira",
            "start_date": "10/03/2026",
            "end_date": "20/06/2026",
            "status": "Em andamento",
        },
        {
            "id": 3,
            "project_name": "Atualização de Infra",
            "description": "Modernização da infraestrutura de TI.",
            "account_name": "Fernanda Rocha",
            "start_date": "12/04/2026",
            "end_date": "01/08/2026",
            "status": "Aguardando resposta",
        },
        {
            "id": 4,
            "project_name": "Escritório",
            "description": "Reforma do escritório central.",
            "account_name": "Carlos Mendes",
            "start_date": "15/01/2026",
            "end_date": "30/03/2026",
            "status": "Concluído",
        },
        {
            "id": 5,
            "project_name": "Aplicação",
            "description": "Desenvolvimento de app mobile.",
            "account_name": "Ana Paula",
            "start_date": "20/02/2026",
            "end_date": "10/07/2026",
            "status": "Em andamento",
        },
        {
            "id": 6,
            "project_name": "Cloud",
            "description": "Migração para cloud.",
            "account_name": "Ricardo Nunes",
            "start_date": "01/03/2026",
            "end_date": "01/05/2026",
            "status": "Aprovado",
        },
        {
            "id": 7,
            "project_name": "Treinamento Técnico",
            "description": "Treinamento de equipe técnica.",
            "account_name": "Patrícia Gomes",
            "start_date": "05/04/2026",
            "end_date": "25/04/2026",
            "status": "Concluído",
        },
        {
            "id": 8,
            "project_name" : "Site",
            "description": "Atualização do site institucional.",
            "account_name": "Bruno Azevedo",
            "start_date": "10/01/2026",
            "end_date": "15/02/2026",
            "status": "Concluído",
        },
        {
            "id": 9,
            "project_name": "CRM",
            "description": "Implementação de CRM.",
            "account_name": "Juliana Pires",
            "start_date": "18/03/2026",
            "end_date": "30/06/2026",
            "status": "Em andamento",
        },
        {
            "id": 10,
            "project_name": "Automação",
            "description": "Automação de processos internos.",
            "account_name": "Felipe Costa",
            "start_date": "05/02/2026",
            "end_date": "20/04/2026",
            "status": "Aprovado",
        },
        {
            "id": 11,
            "project_name":"APIs",
            "description": "Integração com APIs externas.",
            "account_name": "Renata Lima",
            "start_date": "01/05/2026",
            "end_date": "15/07/2026",
            "status": "Aguardando resposta",
        },
        {
            "id": 12,
            "project_name": "Dashboard",
            "description": "Criação de dashboard analítico.",
            "account_name": "Eduardo Farias",
            "start_date": "22/03/2026",
            "end_date": "30/05/2026",
            "status": "Em andamento",
        },
        {
            "id": 13,
            "project_name": "Identidade Visual",
            "description": "Padronização de identidade visual.",
            "account_name": "Larissa Monteiro",
            "start_date": "25/01/2026",
            "end_date": "28/02/2026",
            "status": "Concluído",
        },
        {
            "id": 14,
            "project_name": "BI",
            "description": "Implantação de BI.",
            "account_name": "Thiago Barros",
            "start_date": "10/04/2026",
            "end_date": "01/07/2026",
            "status": "Em andamento",
        },
        {
            "id": 15,
            "project_name":"Banco de Dados",
            "description": "Otimização de banco de dados.",
            "account_name": "Camila Rangel",
            "start_date": "12/02/2026",
            "end_date": "20/03/2026",
            "status": "Concluído",
        },
        {
            "id": 16,
            "project_name" : "Site",
            "description": "Criação de landing page.",
            "account_name": "Diego Martins",
            "start_date": "05/01/2026",
            "end_date": "30/01/2026",
            "status": "Concluído",
        },
        {
            "id": 17,
            "project_name" : "Site",
            "description": "Implementação de autenticação OAuth.",
            "account_name": "Sofia Almeida",
            "start_date": "08/03/2026",
            "end_date": "18/04/2026",
            "status": "Aprovado",
        },
        {
            "id": 18,
            "project_name" : "Site",
            "description": "Revisão de arquitetura backend.",
            "account_name": "Lucas Teixeira",
            "start_date": "01/04/2026",
            "end_date": "01/06/2026",
            "status": "Em andamento",
        },
        {
            "id": 19,
            "project_name" : "Site",
            "description": "Testes automatizados do sistema.",
            "account_name": "Paulo Henrique",
            "start_date": "05/05/2026",
            "end_date": "10/06/2026",
            "status": "Aguardando resposta",
        },
        {
            "id": 20,
            "project_name" : "Site",
            "description": "Deploy em ambiente produção.",
            "account_name": "Natália Freitas",
            "start_date": "01/06/2026",
            "end_date": "05/06/2026",
            "status": "Aprovado",
        },
        {
            "id": 21,
            "project_name" : "Site",
            "description": "Auditoria de segurança interna.",
            "account_name": "Rafael Torres",
            "start_date": "10/06/2026",
            "end_date": "05/07/2026",
            "status": "Em andamento",
        },
        {
            "id": 22,
            "project_name" : "Site",
            "description": "Configuração de servidor Linux.",
            "account_name": "Aline Bastos",
            "start_date": "15/05/2026",
            "end_date": "15/06/2026",
            "status": "Concluído",
        },
        {
            "id": 23,
            "project_name" : "Site",
            "description": "Integração com gateway pagamento.",
            "account_name": "Pedro Ramos",
            "start_date": "01/07/2026",
            "end_date": "10/08/2026",
            "status": "Aprovado",
        },
        {
            "id": 24,
            "project_name" : "Site",
            "description": "Criação de API pública.",
            "account_name": "Daniel Souza",
            "start_date": "20/06/2026",
            "end_date": "30/07/2026",
            "status": "Em andamento",
        },
        {
            "id": 25,
            "project_name" : "Site",
            "description": "Refatoração de código legado.",
            "account_name": "Beatriz Cunha",
            "start_date": "05/05/2026",
            "end_date": "25/06/2026",
            "status": "Em andamento",
        },
        {
            "id": 26,
            "project_name" : "Site",
            "description": "Implementação de cache Redis.",
            "account_name": "André Pacheco",
            "start_date": "10/07/2026",
            "end_date": "01/08/2026",
            "status": "Aguardando resposta",
        },
        {
            "id": 27,
            "project_name" : "Site",
            "description": "Monitoramento de infraestrutura.",
            "account_name": "Luciana Prado",
            "start_date": "01/06/2026",
            "end_date": "30/06/2026",
            "status": "Concluído",
        },
        {
            "id": 28,
            "project_name" : "Site",
            "description": "Análise de requisitos funcionais.",
            "account_name": "Gustavo Melo",
            "start_date": "20/05/2026",
            "end_date": "10/06/2026",
            "status": "Aprovado",
        },
        {
            "id": 29,
            "project_name" : "Site",
            "description": "Planejamento de migração dados.",
            "account_name": "Helena Duarte",
            "start_date": "05/07/2026",
            "end_date": "25/07/2026",
            "status": "Em andamento",
        },
        {
            "id": 30,
            "project_name" : "Site",
            "description": "Validação de performance sistema.",
            "account_name": "Igor Martins",
            "start_date": "15/06/2026",
            "end_date": "15/07/2026",
            "status": "Concluído",
        },
    ]

    if search_client:
        search_lower = search_client.lower()
        data_list = [
            i for i in data_list 
            if search_lower in i.get('account_name', '').lower() 
        ]

    filtered_data = data_list

    if f_account_name:
        filtered_data = [i for i in filtered_data if f_account_name.lower() in i['account_name'].lower()]

    if f_description:
        filtered_data = [i for i in filtered_data if f_description.lower() in i['description'].lower()]
    
    if f_project_name:
        filtered_data = [i for i in filtered_data if f_project_name.lower() in i['project_name'].lower()]

    if f_status and f_status.lower() != "todos": # "Todos" caso queira resetar
        # O valor do filtro pode ser enviado em texto legível (e.g. "Aprovado").
        # Normalizamos para comparar de forma consistente.
        f_status_slug = slugify(f_status)
        filtered_data = [
            i
            for i in filtered_data
            if slugify(i.get('status', '')) == f_status_slug
        ]

    # Filtro de Data (garantir que tanto o input quanto os dados sejam convertidos para date)
    def _parse_date(value: str):
        if not value:
            return None
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
            try:
                return datetime.strptime(value, fmt).date()
            except (ValueError, TypeError):
                continue
        return None

    if f_date_start:
        date_start = _parse_date(f_date_start)
        if date_start:
            filtered_data = [
                i
                for i in filtered_data
                if (item_date := _parse_date(i.get('start_date'))) is not None and item_date == date_start
            ]

    if f_date_end:
        date_end = _parse_date(f_date_end)
        if date_end:
            filtered_data = [
                i
                for i in filtered_data
                if (item_date := _parse_date(i.get('end_date'))) is not None and item_date == date_end
            ]

    paginator   = Paginator(filtered_data, 9)
    page_number = request.GET.get("page", 1)

    # Se houver qualquer filtro ativo, resetamos para a página 1.
    # Isso evita que um `page` antigo presente na URL impeça a exibição de resultados.
    if any([f_description, f_project_name, f_status, f_date_start, f_date_end]):
        page_number = 1

    page_obj    = paginator.get_page(page_number)

    custom_page_range = list(paginator.get_elided_page_range(page_number, on_each_side=1, on_ends=1))

    # MAPEAMENTO DO CONTEÚDO QUE DEVE APARECER NA TABLE
    # ESTE SCHEMA COMPÕE UMA LINHA DA TABLE E CADA ATRIBUTO É UMA CELULA
    table_schema = {
        "description":  {},
        "project_name": {},
        "start_date":   {"is_start_date": True},
        "end_date":     {"is_end_date": True},
        "status":       {"is_status": True},
    }
    
    table_data = []
   
    for item in page_obj.object_list:
        cells = []
        
        for field, config in table_schema.items():
            # PARA OS DADOS REAIS
            #value = getattr(item, field, "")
            #cell = {"value": value}

            cell = {"value": item.get(field, "")} #REMOVER
            cell.update(config)
            cells.append(cell)

        # PARA OS DADOS REAIS
        #table_data.append({
        #     "id": getattr(item, "id", None), 
        #     "cells": cells
        # }) 
        
        # REMOVER
        table_data.append({ "id": item.get("id"), "cells": cells })

    banner = "True" 
    
    lists = {
        'content': {
            "status": ['Aprovado', 'Aguardando resposta', 'Em andamento', 'Reprovado'],
            
        }
    }

    table_headers = ['DESCRIÇÃO', 'NOME DO PROJETO', 'INÍCIO', 'FIM', 'STATUS',]

    context = {
        "usuario":           usuario,
        "mensagem":          "Seja bem-vindo!",
        "table_header":      table_headers,
        "headers":           table_headers,
        "lists" : lists,
        "table_data":        table_data,
        "data_table":        table_data,
        "filters": {
            "description": f_description,
            "project_name": f_project_name,
            "status": f_status,
            "date_start": f_date_start,
            "date_end": f_date_end,
        },
        "page_obj":          page_obj,
        "custom_page_range": custom_page_range,
        "banner":            banner,
    } 

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        context_data = {
            "titulo": "Deletar Projeto",
            "corpo": "Tem certeza que deseja deletar? Esta ação não pode ser desfeita!",
            "botoes": {
                "confirm": {"texto": "Confirmar", "class": "btn_delete_confirmation"},
                "cancel":  {"texto": "Cancelar", "class": "btn_primary"},
            }
        }
        return JsonResponse(context_data)

    if request.headers.get('HX-Request'): return render(request, "components/table.html", context)

    return render(request, "projetos.html", context)


# ______________________________________________________________________________
#                                   CUSTOS FIXOS
# ______________________________________________________________________________
@login_required(login_url='login')
def custos_fixos_view(request):
    # Se quiser passar dados dinâmicos, pode incluí-los no contexto

  

    f_description = request.GET.get('description', '').strip()
    f_value = request.GET.get('value', '').strip()

    search_client = request.GET.get('search', '').strip()

    usuario = {
        "username": "Deivid Hernandez",
        "position": "Engenheiro",
    }

    # Mock de dados para os gráficos (Substitua pela lógica real do banco depois)
    data_list = [
        {
            "id": 1,  
            "client": "João",
            "description": "Expansão de usina solar.",  
            "value": 150000.00,
            'classification': 'Operacional',
        },
    
        {
            "id": 2,  
            "client": "Maria",
            "description": "Implantação de sistema de segurança.", 
            "value": 45200.50,
            'classification': 'Operacional',
        },
        {
            "id": 3,  
            "client": "Carlos",
            "description": "Modernização da infraestrutura de TI.", 
            "value": 89000.00,
            'classification': 'Operacional'
        },
        {
            "id": 4,  
            "client": "Ana",
            "description": "Reforma do escritório central.",        
            "value": 120500.00,
            'classification': 'Administrativo'
        },
        {
            "id": 5,  
            "client": "Beatriz",
            "description": "Desenvolvimento de app mobile.",        
            "value": 75000.00,
            'classification': 'Administrativo'
        },
        {
            "id": 6,  
            "client": "Diego",
            "description": "Migração para cloud.",                  
            "value": 32400.00,
            'classification': 'Administrativo'
        },
        
    ]
 
    if search_client:
        search_lower = search_client.lower()
        data_list = [
            i for i in data_list 
            if search_lower in i.get('description', '').lower() 
        ]

    filtered_data = data_list

    if f_description:
        filtered_data = [i for i in filtered_data if f_description.lower() in i['description'].lower()]

    if f_value:
        search_value = float(f_value)
        filtered_data = [i for i in filtered_data if float(i['value']) == search_value]
    

    soma_por_classificacao = {}

    for item in filtered_data:
        classe = item['classification']
        valor = float(item['value'])
        
        # Se a classe já existe no dicionário, soma o valor. Se não, cria com o valor atual.
        if classe in soma_por_classificacao:
            soma_por_classificacao[classe] += valor
        else:
            soma_por_classificacao[classe] = valor

    # 2. Agora montamos o chart_data usando os dados agrupados
    chart_data = {
        'rosca': {
            'labels': [item['description'] for item in filtered_data],
            'data': [float(item['value']) for item in filtered_data]
        },
        'pizza': {
            # .keys() nos dá as labels únicas (Administrativo, Operacional, etc)
            'labels': list(soma_por_classificacao.keys()),
            # .values() nos dá a soma total de cada uma dessas labels
            'data': list(soma_por_classificacao.values())
        }
    }
   
    paginator   = Paginator(filtered_data, 9)
    page_number = request.GET.get("page", 1)

    # Se houver qualquer filtro ativo, resetamos para a página 1.
    # Isso evita que um `page` antigo presente na URL impeça a exibição de resultados.
    if any([f_description, f_value]):
        page_number = 1

    page_obj    = paginator.get_page(page_number)

    custom_page_range = list(paginator.get_elided_page_range(page_number, on_each_side=1, on_ends=1))

    # MAPEAMENTO DO CONTEÚDO QUE DEVE APARECER NA TABLE
    # ESTE SCHEMA COMPÕE UMA LINHA DA TABLE E CADA ATRIBUTO É UMA CELULA
    table_schema = { "description": {}, "value": {} }

    table_data = TablePresenter.format_collection(page_obj.object_list, table_schema)
    
    banner = "True"
    
    table_headers = ['DESCRIÇÃO', 'VALOR']
    

    context = {
        "usuario":          usuario,
        "mensagem":          "Seja bem-vindo!",
        "table_header":      table_headers, 
        "headers":           table_headers, #para mão perder o valor de table_header na paginação
        "table_data":        table_data,
        "data_table":        table_data, #para mão perder o valor de table_data na paginação
        "filters": {
            "description": f_description,
            "value": f_value,
        },
        "chart_data": chart_data,
        "page_obj":          page_obj,
        "custom_page_range": custom_page_range,
        "request":           request,  # Adicionado para garantir que o request esteja no contexto do template
        "banner":            banner,   # Adicionado para controlar a exibição do banner
    }

    target = request.headers.get('HX-Request')
   
    if target: return render(request, "components/table.html", context)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Aqui você monta o "contexto" que o JS vai usar
        context_data = {
            "titulo": "Deletar",
            "corpo": "Tem certeza que deseja deletar os itens selecionados?",
            "botoes": {
                "confirm": {"texto": "Confirm", "class": "btn_delete_confirmation"},
                "cancel":  {"texto": "Cancel",  "class": "btn_primary"},
            }
        }
        return JsonResponse(context_data)

    return render(request, "custos_fixos.html", context)
    
# ______________________________________________________________________________
#                                   DASHBOARD
# ______________________________________________________________________________
@login_required(login_url='login')
def dashboard_view(request):
    context = {
        'totalsIndicators': {
            'project_count': 126,
            'project_opened_value': 6,
            'project_approved_value': 97,
            'project_value': 34000.00,
        },
        'projectApprovalHistory': {
            'labels': ['jan', 'fev', 'mar', 'abr', 'mai', 'jun'],
            'data': [3, 4, 2, 3, 4, 2]
        },
        'projectTypeChart': {
            'labels': ['Arquitetônico', 'Estrutural', 'Elétrico', 'PCI'],
            'data': [12, 3, 1, 1]
        },
        'projectClassificationChart': {
            'labels': ['Arquitetônico', 'Estrutural', 'Elétrico'],
            'data': [10, 4, 2]
        },
        'projectIndicators': {
            'percentProjectsApproved': 68,
            'averageProjectsBillingByMonth': 8200.75,
            'priceByRejectedProject': 326,
            'costByHourByProject':44.6,

            'priceByApprovedProject': {
                'average': 600,
                'labels': ['Jan', 'Feb', 'Mar'],
                'data': [9000, 9600, 9800]
            },

            'priceBySizeRejected':524,
            'timeBySize':10, 
            'workCostBySize': {
                'average': 987,
                'labels': ['Jan', 'Feb', 'Mar'],
                'data': [2100, 2200, 2600]
            }
        },
    }
    return render(request, 'dashboard.html', context)

# ______________________________________________________________________________
#                                   IMPOSTOS
# ______________________________________________________________________________
@login_required(login_url='login')
def impostos_view(request): 
    f_description = request.GET.get('description', '').strip()
    f_value = request.GET.get('value', '').strip()

    search_client = request.GET.get('search', '').strip()

    usuario = {
        "username": "Deivid Hernandez",
        "position": "Engenheiro",
    }

    #Mock substituir pela lista de impostos do bd
    data_list = [
        {
            "id": 1,  
            "description": "IRR",  
            "value": 15,
            'classification': 'Operacional',
        },
    
        {
            "id": 2,  
            "description": "IRT", 
            "value": 4,
            'classification': 'Operacional',
        },
        {
            "id": 3,  "description": "ACC", 
            "value": 8,
            'classification': 'Operacional'
        },
        {
            "id": 4,  
            "description": "RSS",        
            "value": 12,
            'classification': 'Administrativo'
        },
        {
            "id": 5,  
            "description": "AT",        
            "value": 7.5,
            'classification': 'Administrativo'
        },
        {
            "id": 6,  
            "description": "TR",                  
            "value": 3.2,
            'classification': 'Administrativo'
        },
        {
            "id": 7,  
            "description": "ACR",        
            "value": 12,
            'classification': 'Administrativo'
        },
        {
            "id": 8,  
            "description": "IRX",    
            "value": 8.5,
            'classification': 'Marketing'
        },
        {
            "id": 9,  
            "description": "IHT",                 
            "value": 5,
            'classification': 'Marketing'
        },
        {
            "id": 10, 
            "description": "BRC",      
            "value": 2,
            'classification': 'Marketing'
        },
        {
            "id": 11, 
            "description": "INH",         
            "value": 15,
            'classification': 'Marketing'
        },
        {
            "id": 12, 
            "description": "HN",       
            "value": 4,
            'classification': 'Marketing'
        },
        {
            "id": 13, 
            "description": "HT",    
            "value": 9,
            'classification': 'Marketing'
        },
    ]

    if search_client:
        search_lower = search_client.lower()
        data_list = [
            i for i in data_list 
            if search_lower in i.get('description', '').lower() 
        ]

    filtered_data = data_list

    if f_description:
        filtered_data = [i for i in filtered_data if f_description.lower() in i['description'].lower()]

    if f_value:
        search_value = float(f_value)
        filtered_data = [i for i in filtered_data if float(i['value']) == search_value]
    

    soma_por_classificacao = {}

    for item in filtered_data:
        classe = item['classification']
        valor = float(item['value'])
        
        # Se a classe já existe no dicionário, soma o valor. Se não, cria com o valor atual.
        if classe in soma_por_classificacao:
            soma_por_classificacao[classe] += valor
        else:
            soma_por_classificacao[classe] = valor

    # 2. Agora montamos o chart_data usando os dados agrupados
    chart_data = {
        'rosca': {
            'labels': [item['description'] for item in filtered_data],
            'data': [float(item['value']) for item in filtered_data]
        },
        'pizza': {
            # .keys() nos dá as labels únicas (Administrativo, Operacional, etc)
            'labels': list(soma_por_classificacao.keys()),
            # .values() nos dá a soma total de cada uma dessas labels
            'data': list(soma_por_classificacao.values())
        }
    }
   
   
    paginator   = Paginator(filtered_data, 9)
    page_number = request.GET.get("page", 1)

    # Se houver qualquer filtro ativo, resetamos para a página 1.
    # Isso evita que um `page` antigo presente na URL impeça a exibição de resultados.
    if any([f_description, f_value]):
        page_number = 1

    page_obj    = paginator.get_page(page_number)

    custom_page_range = list(paginator.get_elided_page_range(page_number, on_each_side=1, on_ends=1))

    # MAPEAMENTO DO CONTEÚDO QUE DEVE APARECER NA TABLE
    # ESTE SCHEMA COMPÕE UMA LINHA DA TABLE E CADA ATRIBUTO É UMA CELULA
    table_schema = { "description": {}, "value": {} }


    table_data = TablePresenter.format_collection(page_obj.object_list, table_schema)
    
    table_headers = ['DESCRIÇÃO', 'VALOR (%)']
    banner = "True"
    context = {
        "usuario":           usuario,
        "mensagem":          "Seja bem-vindo!",
        "table_header":      table_headers, 
        "headers":           table_headers, #para mão perder o valor de table_header na paginação
        "table_data":        table_data,
        "data_table":        table_data, #para mão perder o valor de table_data na paginação
        "filters": {
            "description": f_description,
            "value": f_value,
        },
        "chart_data": chart_data,
        "page_obj":          page_obj,
        "custom_page_range": custom_page_range,
        "request":           request,  # Adicionado para garantir que o request esteja no contexto do template
        "banner":            banner,   # Adicionado para controlar a exibição do banner
    }

    target = request.headers.get('HX-Request')
   
    if target: return render(request, "components/table.html", context)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Aqui você monta o "contexto" que o JS vai usar
        context_data = {
            "titulo": "Deletar",
            "corpo": "Tem certeza que deseja deletar os itens selecionados?",
            "botoes": {
                "confirm": {"texto": "Confirm", "class": "btn_delete_confirmation"},
                "cancel":  {"texto": "Cancel",  "class": "btn_primary"},
            }
        }
        return JsonResponse(context_data)

    return render(request, "impostos.html", context)

@login_required(login_url='login')
def configuracoes_view(request):
    from arqcalc_webapp.templatetags.config_table import get_table_vars

    type_coin = [
        'Real Brasileiro (R$)' ,
        'Dólar Americano ($)' ,
        'Euro (€)' ,
    ]

    user_data = {
            'nome': 'Luiz Henrique',
            'email': 'luiz.henrique@exemplo.com.br',
            'cep': '12940-000',
            'cidade': 'Atibaia',
            'estado': 'São Paulo',
            'pais': 'Brasil',
            'moeda_atual': 'BRL',  # Adicionado
        }

    context = {
    'user_data': user_data,
    'type_coin': type_coin,
    'cfg_table': get_table_vars({'request': request}),
    }
    
    
    return render(request, "configuracoes.html", context)


# ______________________________________________________________________________
#                                   GERAR PDF
# ______________________________________________________________________________

def calcular_precificacao(db_data, custos_fixos, impostos, comissao_percent, preco_venda):
    # =========================
    # CUSTO VARIÁVEL (ETAPAS)
    # =========================
    custo_variavel = 0
    for etapa in db_data.get('etapas', []):
        for sub in etapa.get('subetapas', []):
            custo_variavel += float(sub.get('custo', 0))

    # =========================
    # CUSTO ESPECÍFICO
    # =========================
    custo_especifico = sum(
        float(c.get('valor', 0)) for c in db_data.get('custos_especificos', [])
    )

    # =========================
    # CUSTO FIXO
    # =========================
    custo_fixo = sum(float(c.get('valor', 0)) for c in custos_fixos)

    # =========================
    # CUSTO OPERACIONAL
    # =========================
    custo_operacional = custo_variavel + custo_especifico + custo_fixo

    # =========================
    # IMPOSTOS (%)
    # =========================
    imposto_percent = sum(float(i.get('valor', 0)) for i in impostos)

    valor_imposto = (preco_venda * imposto_percent) / 100

    # =========================
    # COMISSÃO
    # =========================
    valor_comissao = (preco_venda * comissao_percent) / 100

    # =========================
    # LUCRO
    # =========================
    lucro = preco_venda - (valor_imposto + valor_comissao + custo_operacional)

    lucro_percentual = (
        (lucro / preco_venda) * 100 if preco_venda > 0 else 0
    )

    # =========================
    # PONTO DE EQUILÍBRIO
    # =========================
    divisor = 1 - ((imposto_percent + comissao_percent) / 100)
    ponto_equilibrio = custo_operacional / divisor if divisor > 0 else 0

    return {
        "composicao_custo": {
            "custo_variavel": custo_variavel,
            "custo_especifico": custo_especifico,
            "custo_fixo": custo_fixo,
            "custo_operacional": custo_operacional,
        },
        "preco_venda": {
            "preco_venda": preco_venda,
            "imposto": valor_imposto,
            "comissoes": valor_comissao,
            "custo_operacional": custo_operacional,
            "ponto_equilibrio": ponto_equilibrio,
            "preco_final": lucro,
            "margem_lucro": lucro_percentual,
        }
    }


def tempo_para_float(tempo_str):
    if not tempo_str:
        return 0.0

    tempo_str = str(tempo_str).replace(',', '.').lower()

    if 'h' in tempo_str:
        partes = tempo_str.split('h')
        horas = float(partes[0] or 0)
        minutos = float(partes[1] or 0) / 60 if len(partes) > 1 else 0
        return horas + minutos

    return float(tempo_str)


def calcular_resumo_e_etapas(db_data):
    profissionais_map = {
        p['nome']: float(p.get('valor_hora', 0))
        for p in db_data.get('profissionais', [])
    }

    total_custo_geral = 0

    # =========================
    # CALCULO POR ETAPA
    # =========================
    for etapa in db_data.get('etapas', []):
        custo_etapa = 0
        tempo_profissionais = {}

        for sub in etapa.get('subetapas', []):
            tempo = tempo_para_float(sub.get('tempo'))
            resp = sub.get('resp')

            valor_hora = profissionais_map.get(resp, 0)

            custo_item = tempo * valor_hora

            # salva no item (ESSENCIAL pro PDF)
            sub['custo_calculado'] = custo_item

            custo_etapa += custo_item

            # soma tempo por profissional dentro da etapa
            tempo_profissionais[resp] = tempo_profissionais.get(resp, 0) + tempo

        # regra do maior tempo
        tempo_total_etapa = max(tempo_profissionais.values(), default=0)

        etapa['total_custo'] = custo_etapa
        etapa['total_tempo'] = f"{tempo_total_etapa:.2f}"

        total_custo_geral += custo_etapa

    # =========================
    # RESUMO PROFISSIONAL
    # =========================
    resumo_profissionais = {}

    for etapa in db_data.get('etapas', []):
        for sub in etapa.get('subetapas', []):
            resp = sub.get('resp')

            if resp not in resumo_profissionais:
                resumo_profissionais[resp] = {'h': 0, 'c': 0}

            tempo = tempo_para_float(sub.get('tempo'))
            custo = sub.get('custo_calculado', 0)

            resumo_profissionais[resp]['h'] += tempo
            resumo_profissionais[resp]['c'] += custo

    db_data['resumo_profissionais'] = resumo_profissionais
    db_data['total_custo_geral'] = total_custo_geral

    return db_data

@login_required(login_url='login')
def exportar_projeto_pdf(request, id, currency='BRL'):

    user_moeda = currency # Pegue do front
    # Dicionário simulando uma tabela do banco de dados organizada por ID
    mock_database = {
        1: {
            "projeto_nome": "Cozinha Gourmet",
            "data_emissao": "20 de Março de 2026",
            "cliente": "Flávia Souza",
            "responsavel": "Sarah",
            "bairro": "Jardins",
            "cidade": "Belo Horizonte/MG",
            "data_inicio": "01/08/2022",
            "data_fim": "31/08/2022",
            "custos_especificos": [
                {"nome": "Impressão", "valor": 70.00},
                {"nome": "Visita Técnica", "valor": 250.00},
                {"nome": "RRT", "valor": 110.00},
                {"nome": "Impressão", "valor": 70.00},
                {"nome": "Visita Técnica", "valor": 150.00},
            ],
            "profissionais": [
                {"nome": "Sarah", "cargo": "Arquiteta Responsável", "valor_hora": 45.00},
                {"nome": "Rayane", "cargo": "Arquiteta", "valor_hora": 25.00},
                {"nome": "Sarah", "cargo": "Arquiteta Responsável", "valor_hora": 45.00},
                {"nome": "Rayane", "cargo": "Arquiteta", "valor_hora": 25.00},
                {"nome": "Sarah", "cargo": "Arquiteta Responsável", "valor_hora": 45.00},
                {"nome": "Rayane", "cargo": "Arquiteta", "valor_hora": 25.00},
                {"nome": "Sarah", "cargo": "Arquiteta Responsável", "valor_hora": 45.00},
                {"nome": "Rayane", "cargo": "Arquiteta", "valor_hora": 25.00},
                {"nome": "Sarah", "cargo": "Arquiteta Responsável", "valor_hora": 45.00},
                {"nome": "Rayane", "cargo": "Arquiteta", "valor_hora": 25.00},
                {"nome": "Sarah", "cargo": "Arquiteta Responsável", "valor_hora": 45.00},
                {"nome": "Rayane", "cargo": "Arquiteta", "valor_hora": 25.00},
                {"nome": "Sarah", "cargo": "Arquiteta Responsável", "valor_hora": 45.00},
            ],
            "etapas": [
                {
                    "numero": "01", "nome": "CONTATO",
                    "subetapas": [
                        {"nome": "Contato inicial", "resp": "Sarah", "tempo": "1h00", "custo": 45.00},
                        {"nome": "Organização de arquivos", "resp": "Rayane", "tempo": "2h00", "custo": 50.00},
                    ]
                },
                {
                    "numero": "02", "nome": "ORGANIZAÇÃO",
                    "subetapas": [
                        {"nome": "Contato inicial", "resp": "Sarah", "tempo": "1h00", "custo": 45.00},
                        {"nome": "Organização de arquivos", "resp": "Rayane", "tempo": "2h00", "custo": 50.00},
                    ]
                },
                { 
                    "numero": "03", "nome": "FINALIZAÇÃO",
                    "subetapas": [
                        {"nome": "Contato inicial", "resp": "Sarah", "tempo": "1h00", "custo": 45.00},
                        {"nome": "Organização de arquivos", "resp": "Rayane", "tempo": "2h30", "custo": 50.00},
                        {"nome": "Contato inicial", "resp": "Sarah", "tempo": "1h00", "custo": 45.00},
                        {"nome": "Organização de arquivos", "resp": "Rayane", "tempo": "2h00", "custo": 50.00},
                        {"nome": "Contato inicial", "resp": "Sarah", "tempo": "1h00", "custo": 45.00},
                        {"nome": "Organização de arquivos", "resp": "Rayane", "tempo": "2h00", "custo": 50.00},
                        {"nome": "Contato inicial", "resp": "Sarah", "tempo": "1h00", "custo": 45.00},
                        {"nome": "Organização de arquivos", "resp": "Rayane", "tempo": "2h00", "custo": 50.00},
                        {"nome": "Contato inicial", "resp": "Sarah", "tempo": "1h00", "custo": 45.00},
                        {"nome": "Organização de arquivos", "resp": "Rayane", "tempo": "2h00", "custo": 50.00},
                        {"nome": "Contato inicial", "resp": "Sarah", "tempo": "1h00", "custo": 45.00},
                        {"nome": "Organização de arquivos", "resp": "Rayane", "tempo": "2h00", "custo": 50.00},
                        {"nome": "Contato inicial", "resp": "Sarah", "tempo": "1h00", "custo": 45.00},
                        {"nome": "Organização de arquivos", "resp": "Rayane", "tempo": "2h00", "custo": 50.00},
                        {"nome": "Contato inicial", "resp": "Sarah", "tempo": "1h00", "custo": 45.00},
                        {"nome": "Organização de arquivos", "resp": "Rayane", "tempo": "2h00", "custo": 50.00},
                        {"nome": "Contato inicial", "resp": "Sarah", "tempo": "1h00", "custo": 45.00},
                        {"nome": "Organização de arquivos", "resp": "Rayane", "tempo": "2h00", "custo": 50.00},
                    ]
                },
                {
                    "numero": "02", "nome": "FABRICAÇÃO",
                    "subetapas": [
                        {"nome": "Contato inicial", "resp": "Sarah", "tempo": "1h00", "custo": 45.00},
                        {"nome": "Organização de arquivos", "resp": "Rayane", "tempo": "2h00", "custo": 50.00},
                    ]
                },
            ],
           
        }
    }

    # Busca o projeto no mock pelo ID (ou retorna 404 se não existir)
    db_data = mock_database.get(id)

    if not db_data:
        from django.http import Http404
        raise Http404("Projeto não encontrado no banco de dados.")

    lista_custos_fixos = [
        {"descricao": "Aluguel", "valor": 2000.00},
        {"descricao": "Software", "valor": 300.00},
        {"descricao": "Contabilidade", "valor": 650.00},
    ]

    lista_impostos = [
        {"descricao": "IRR", "valor": 15},
        {"descricao": "IRT", "valor": 4},
        {"descricao": "ACC", "valor": 8},
    ]

    comissao = 10  # Exemplo: 10% de comissão
    preco_venda = 8000.00  # Exemplo: preço de venda do

    precificacao = calcular_precificacao(
        db_data=db_data,
        custos_fixos=lista_custos_fixos,   # vindo da view
        impostos=lista_impostos,           # vindo da view
        comissao_percent=comissao,         # vindo da view
        preco_venda=preco_venda            # vindo do form/input
    )

    # Atribui o resultado da precificação ao db_data para que fique disponível no PDF
    db_data['precificacao'] = precificacao  
    # Calcula o resumo dos profissionais e etapas e também atribui ao db_data para o PDF
    db_data = calcular_resumo_e_etapas(db_data)
    # Atribui a moeda selecionada pelo usuário para o PDF exibir os valores corretamente
    db_data['moeda'] = user_moeda


    # --- DEBUG: Validação de Dados antes de enviar ao PDF ---
    cv = db_data['precificacao']['composicao_custo'].get('custo_variavel')
    pv = db_data['precificacao']['preco_venda'].get('preco_venda')
    
    print(f"\n{'='*30}")
    print(f"DEBUG PDF EXPORT:")
    print(f"Custo Variável: {cv} (Tipo: {type(cv)})")
    print(f"Preço de Venda: {pv} (Tipo: {type(pv)})")
    print(f"{'='*30}\n")

    if cv is None or cv == 0:
        logger.warning("ALERTA: Custo Variável está zerado ou nulo no mock!")

    if not db_data:
        from django.http import Http404
        raise Http404("Projeto não encontrado no banco de dados.")

    response = HttpResponse(content_type='application/pdf')
    nome_slug = slugify(db_data['projeto_nome'])
    response['Content-Disposition'] = f'attachment; filename="ARQCALC_{nome_slug}_{id}.pdf"'

    # Aqui você pode usar o db_data para preencher o PDF usando a classe ArqCalcReporter de services/pdf_service.py
    reporter = ArqCalcReporter(response, moeda=user_moeda)
    reporter.build(db_data)

    return response

class GerenciarItensView(View):

    def post(self, request, resource, id=None): # Aceita id opcional para editar
        # Mapeia o resource para o Model (adicione outros conforme crescer)
        model_map = {
            'custos_fixos': ProjectCosts,
            'impostos': ProjectCosts,  # <--- Adicione o model de impostos aqui
        }
        
        Model = model_map.get(resource)
        if not Model:
            return JsonResponse({'status': 'erro na operação', 'message': 'Recurso inválido'}, status=400)

        # Dados vindos do FormData do JS
        description = request.POST.get('description')
        value = request.POST.get('value')
        
        try:
            if id:
                # EDITAR
                item = Model.objects.get(id=id)
                item.description = description
                item.value = value
                # item.save()
            else:
                # CRIAR NOVO
                item.description = description
                item.value = value
                Model.objects.create(description=description, value=value)
            
            return JsonResponse({'status': 'sucesso'})
        except Exception as e:
            return JsonResponse({'status': 'erro na operação', 'message': str(e)}, status=500)
    
    # 'resource' virá da URL (projetos, custos_fixos, etc)
    def delete(self, request, resource):
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            resource_type = data.get('resource_type') # 'phase' ou 'item'
            
            # O 'resource' vem da URL (ex: 'projetos', 'custos_fixos')
            resource = self.kwargs.get('resource') 

            if resource_type == 'phase':
                # Lógica para deletar a ETAPA completa
                # Ex: ProjectPhase.objects.get(id=item_id).delete()
                print(f"Deletando Etapa ID: {item_id} do recurso {resource}")
            else:
                # Lógica para deletar apenas um ITEM da tabela
                # Ex: ProjectItem.objects.get(id=item_id).delete()
                print(f"Deletando Item ID: {item_id} do recurso {resource}")

            return JsonResponse({'status': 'success'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


# ============ NOTIFICAÇÕES ========================= #
@login_required(login_url='login')
def buscar_notificacoes_ajax(request):
    # Simulação de dados (Substitua pela sua consulta ao banco )
    notifications = [
        {
            "image": "/static/assets/img/avatars/2.jpg",
            "message": "Nova proposta recebida!",
            "name": "Tech Night"
        }
    ]

    html_content = render_to_string('components/modals/modal_notifications_content.html', {
        'notifications': notifications
    })
    
    #has_bow devera receber um valor entre false e true para identificar se há uma nova mensagem ou não e exibi-la junto ao icone de nova notificação
    has_new = len(notifications) > 0
    
    return JsonResponse({
        "has_new": has_new,
        "html": html_content
    })


# ============ ESQUECI MINHA SENHA ========================= #
class CustomPasswordResetView(PasswordResetView):
    template_name            = 'redefinir_senha/password_reset_form.html'
    subject_template_name    = 'redefinir_senha/password_reset_subject.txt' # assunto do e-mail
    html_email_template_name = 'redefinir_senha/password_reset_email.html'  # e-mail versão HTML
    email_template_name      = 'redefinir_senha/password_reset_email.txt'   # e-mail versão texto
    success_url = reverse_lazy('password_reset_done')


    def form_valid(self, form): # Envia o e-mail normalmente e salva o e-mail digitado na sessão
        response = super().form_valid(form)  # chama o envio do e-mail
        email = form.cleaned_data.get('email')
        self.request.session["email_para_recuperacao"] = email
        
        # redireciona normalmente para password_reset_done
        return response, 