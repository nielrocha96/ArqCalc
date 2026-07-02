# EDITADO MAR-23 

from django import template       # módulo para criar tags e filtros customizados para templates
register = template.Library()     # usada para registrar suas tags personalizadas

@register.simple_tag
def set_var(val):
    return val

#### EDITADA FEV-13
@register.filter
def get_item(dictionary, key):
    if not dictionary: return ""
    return dictionary.get(key, "")

@register.filter
def slug_under(value):
    from django.template.defaultfilters import slugify
    return slugify(value).replace('-', '_')

 # Define uma tag simples que pode retornar qualquer tipo de dado
 # Permite que a função receba o context do template (incluindo request)
@register.simple_tag(takes_context=True)

def get_table_vars(context):
    # no template, a função será usada como {% get_table_vars as table_vars %}
    ## context.get('requests') só funciona se django.template.context_processors.request estiver habilitado no TEMPLATES.
    request = context.get('request')
    print(f"DEBUG: Request encontrado? {request is not None}")

    
    if not request or not request.resolver_match: 
        print("DEBUG: Caiu no IF de segurança (Request ou ResolverMatch nulo)")
        return {'head': {}, 'body': {}}
   
    url_name = request.resolver_match.url_name   # Isso permite que a lógica dependa do nome da rota, e não da URL em si.
    print(f"DEBUG: URL Name detectada: '{url_name}'")

    # CONFIGURAÇÃO PARA TABELAS DAS TABS NA TELA NOVO_PROJETO #
    novo_projeto_tabs = {
        'dados': {
            'head': {'checkbox': 'false', 'delete': 'false'},
            'body': {'checkbox': 'false', 'delete': 'false', 'edit': 'false', 'copy': 'false', 'pdf': 'false'},
            "lists": {
                'content': {
                    "status": {
                        'select': {'class': ['select_item_status'], 'id': 'status_select'},
                        'button': {'class': ['selected_item_status']},
                        'list': {'class': ['custom_options_status']},
                        'item': {
                            'data_value': {
                                'Aguardando resposta': 'aguardando-resposta', 
                                'Aprovado': 'aprovado',
                                'Em andamento': 'em-andamento',
                                'Reprovado': 'reprovado',
                            }
                        },
                    },
                    "project_type": {
                        'select': {'class': ['select_item_base'], 'id': 'project_type'},
                        'button': {'class': ['selected_item_base']},
                        'list': {'class': ['custom_options_base']},
                        'item': {'data_value': {'Residencial': 'residencial', 'Arquitetônico': 'arquitetonico', 'Industrial': 'industrial', 'Outros': 'outro'}},
                    },
                    "classification": {
                        'select': {'class': ['select_item_base'], 'id': 'classification_project'},
                        'button': {'class': ['selected_item_base']},
                        'list': {'class': ['custom_options_base']},
                        'item': {'data_value': {'Novo': 'novo', 'Reforma': 'reforma'}},
                    },
                    "category": {
                        'select': {'class': ['select_item_base'], 'id': 'category'},
                        'button': {'class': ['selected_item_base']},
                        'list': {'class': ['custom_options_base']},
                        'item': {'data_value': {'Residencial': 'residencial', 'Comercial': 'comercial'}},
                    },
                }
            }
        },
        'custo': {
            'head': {'checkbox': 'true', 'delete': 'true'},
            'head_class': {'head':['table_head'], 'row': ['row_head_table']},
            'body': {'checkbox': 'true', 'delete': 'false', 'edit': 'false', 'copy': 'false', 'pdf': 'false'},
            'body_class': {'body':['table_body'], 'row': ['row_body_table'], 'collumn': ['content_collumn_body'], 'cell': ['input_table']},
        },
        'profissional': {
            'head': {'checkbox': 'true', 'delete': 'true'},
            'head_class': {'head':['table_head'], 'row': ['row_head_table']},
            'body': {'checkbox': 'true', 'delete': 'false', 'edit': 'false', 'copy': 'false', 'pdf': 'false'},
            'body_class': {'body':['table_body'], 'row': ['row_body_table'], 'collumn': ['content_collumn_body'], 'cell': ['input_table']},
        },
        'etapa': {
            'head': {'checkbox': 'false', 'copy': 'true', 'delete': 'true'},
            'head_class': {'head':['table_head'], 'row': ['row_head_table', 'row_head_primary']},
            'body': {'checkbox': 'true', 'delete': 'false', 'edit': 'false', 'copy': 'false', 'pdf': 'false'},
            'body_class': {'body':['table_body'], 'row': ['row_body_table'], 'collumn': ['content_collumn_body'], 'cell': ['input_table']},
            'lists': {
                "content": {
                    "professional_phase": {
                        'select': {'class': ['select_item_base'], 'id': 'professional_select'},
                        'button': {'class': ['selected_item_base']}, 
                        'list': {'class': ['custom_options_base']},
                    },
                    "style_project": { 
                        'select': {'class': ['select_item_base'], 'id': 'style_project_select'},
                        'button': {'class': ['selected_item_base']},
                        'list': {'class': ['custom_options_base']},
                        'item': {'data_value': {'Padrão': 'padrao', 'Simplificado': 'simplificado', 'Completo': 'completo'}},
                    }
                }
            }
        },
        'resumo': {
            'head': {'checkbox': 'false', 'copy': 'false', 'delete': 'false', 'order_by': 'true',},
            'head_class': {'head':['table_head','table_head_primary'], 'row': ['row_head_table', 'row_head_primary']},
            'body': {'checkbox': 'false', 'delete': 'false', 'edit': 'false', 'copy': 'false', 'pdf': 'false'},
            'body_class': {'body':['table_body'], 'row': ['row_body_table'], 'collumn': ['content_collumn_body'], 'cell': ['input_table_disabled']},
        },
        'preco': {
            'head':{},
            'body': {},
            'body_class': {'body':['table_body'], 'row': ['row_body_costs'], 'collumn': ['collumn_body_pricing']},
        }
    }

    # CONFIGURAÇÃO PARA TABELAS NAS DEMAIS TABELAS #
    configs = {
        'projetos': {
            'head': {'checkbox': 'true', 'delete': 'true'},
            'head_class': {
                'head':['table_head'],
                'row': ['row_head_table'],
            },
            'body': {'checkbox': 'true', 'delete': 'true', 'edit': 'true', 'copy': 'true', 'pdf': 'true'},
            'body_class': {
                'body':['table_body'],
                'row': ['row_body_table'],
                'collumn': ['content_collumn_body'],
            },
            "lists": {
                'content': {
                    "status": {
                        'select': {'class': ['select_item_status'], 'id': 'status_select'},
                        'button': {'class': ['selected_item_status']},
                        'list': {'class': ['custom_options_status']},
                        'item': {
                            'data_value': {
                                'Aguardando resposta': 'aguardando-resposta', 
                                'Aprovado': 'aprovado',
                                'Em andamento': 'em-andamento',
                                'Reprovado': 'reprovado',
                            }
                        },
                    },
                },
            },
            "filter":{
                "fields": {
                    'account_name': 'true',
                    'description': 'true',
                    'project_name': 'true',
                    'date_start' : 'true',
                    'date_end': 'true',
                    'status_input': 'true',
                    'value': 'false',
                }
            }
        },
        'custos_fixos': {
            'head': {'checkbox': 'true', 'delete': 'true'},
            'head_class': {
                'head':['table_head'],
                'row': ['row_head_table'],
            },
            'body': {'checkbox': 'true', 'delete': 'false', 'edit': 'true', 'copy': 'false', 'pdf': 'false'},
            'body_class': {
                'body':['table_body'],
                'row': ['row_body_table'],
                'collumn': ['content_collumn_body'],
                'cell': ['input_table', 'cell_none']
            },
            "filter":{
                "fields": {
                    'description': 'true',
                    'project_name': 'false',
                    'date_start' : 'false',
                    'date_end': 'false',
                    'status_input': 'false',
                    'value': 'true'
                }
            }
        },
        'impostos': {
            'head': {'checkbox': 'true', 'delete': 'true'},
            'head_class': {
                'head':['table_head'],
                'row': ['row_head_table'],
            },
            'body': {'checkbox': 'true', 'delete': 'false', 'edit': 'true', 'copy': 'false', 'pdf': 'false'},
            'body_class': {
                'body':['table_body'],
                'row': ['row_body_table'],
                'collumn': ['content_collumn_body'],
                'cell': ['input_table', 'cell_none',]
            },
            "filter":{
                "fields": {
                    'description': 'true',
                    'project_name': 'false',
                    'date_start' : 'false',
                    'date_end': 'false',
                    'status_input': 'false',
                    'value': 'true'
                }
            }
        },
        'configuracoes': { 
            'lists': {
                'content': {
                    'moeda': {
                        'select': {'class': ['select_item_base'], 'id': 'moeda_select'},
                        'button': {'class': ['selected_item_base']},
                        'list': {'class': ['custom_options_base']},
                        'item': {
                            'data_value': {
                                'Real Brasileiro (R$)': 'BRL',
                                'Dólar Americano ($)': 'USD',
                                'Euro (€)': 'EUR',
                            }
                        },
                    }
                }
            }
        }
    }

    if url_name == 'novo_projeto' :
        return novo_projeto_tabs
    
    if url_name == 'configuracoes' :
        return configs['configuracoes']
    
    # Busca a config pelo nome da url ou retorna o padrão
    ## retorna um dicionário com configurações para a tabela
    ## Se a rota não estiver no configs, retorna o padrão abaixo (tudo desativado).
    return configs.get(url_name, {
        'head': {'checkbox': 'false', 'delete': 'false'},
        'body': {'checkbox': 'false', 'delete': 'false', 'edit': 'false', 'copy': 'false', 'pdf': 'false'}
    })