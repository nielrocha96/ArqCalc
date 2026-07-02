# EDITADO MAR-13

def projetos_context(request):
    projeto_mock = [
        {
            "id": 1,
            "description": "Projeto de expansão de usina solar para aumento da capacidade de geração de energia fotovoltaica na região norte de São Paulo.",
            "account_name": "Mariana Silva",
            "start_date": "2026-02-01",
            "end_date": "2026-05-15",
            "customer_name": "Tech Inovações LTDA",
            "project_name": "Expansão Fotovoltaica Norte",
            "street": "Avenida Paulista",
            "street_number": 1500,
            "street_additional": "Andar 12, Sala 1201",
            "neighborhood": "Bela Vista",
            "city": "São Paulo",
            "state": "SP",
            "size": 450,
            "project_status": "Aprovado",
            "project_type": "Industrial",
            "project_classification": "Alta Prioridade",
            "project_category": "Energia Renovável",
            "template_id": 10,
            "user_id": 42,
            "costs": [
                {
                    "id": 1,
                    "description": "Impressão",
                    "value": 150,
                    "project_name": "Expansão Fotovoltaica Norte",
                    "project_id": 1,
                },
                {
                    "id": 2,
                    "description": "Deslocamento Técnico",
                    "value": 300,
                    "project_name": "Expansão Fotovoltaica Norte",
                    "project_id": 1,
                },
            ],
            "people": [
                {"id": 1, "name": "Luiz", "position": "Arquiteto", "value_hour": 50},
                {"id": 2, "name": "Ana Clara", "position": "Engenheira Elétrica", "value_hour": 80},
            ],
            "phases": [
                {
                    "id": 1,
                    "name_phase": "Etapa 1: Levantamento",
                    "items_phases": [
                        {
                            "id": 1,
                            "item_name": "Medição de Área",
                            "time_hour": 3,
                            "value": 150,
                            "person_id": 1,
                            "person": "Luiz",
                            "project": "Expansão Fotovoltaica Norte",
                            "phase_id": 1,
                            "project_id": 1,
                        }
                    ],
                    "project_name": "Expansão Fotovoltaica Norte",
                    "project_id": 1,
                    "order": 1,
                }
            ],
            "pricing": [
                {"id": 1, "name": "Custo fixo", "value": 15, "project_id": 1},
                {"id": 2, "name": "Impostos", "value": 12.5, "project_id": 1},
            ],
        },
		{
			"id": 2,
			"description": "Projeto de implantação de automação predial para controle inteligente de iluminação, climatização e consumo energético.",
			"account_name": "Carlos Mendes",
			"start_date": "2026-03-05",
			"end_date": "2026-07-10",
			"customer_name": "Edifício Prime Tower",
			"project_name": "Automação Predial Inteligente",
			"street": "Rua Faria Lima",
			"street_number": 900,
			"street_additional": "Torre B",
			"neighborhood": "Itaim Bibi",
			"city": "São Paulo",
			"state": "SP",
			"size": 1800,
			"project_status": "Em andamento",
			"project_type": "Comercial",
			"project_classification": "Alta Prioridade",
			"project_category": "Automação",
			"template_id": 11,
			"user_id": 51,
			"costs": [
				{
					"id": 3,
					"description": "Sensores de Presença",
					"value": 1200,
					"project_name": "Automação Predial Inteligente",
					"project_id": 2,
				},
				{
					"id": 4,
					"description": "Central de Controle",
					"value": 3500,
					"project_name": "Automação Predial Inteligente",
					"project_id": 2,
				},
			],
			"people": [
				{"id": 3, "name": "Rafael", "position": "Engenheiro de Automação", "value_hour": 95},
				{"id": 4, "name": "Bruna", "position": "Técnica em Eletrônica", "value_hour": 55},
			],
			"phases": [
				{
					"id": 2,
					"name_phase": "Etapa 1: Diagnóstico",
					"items_phases": [
						{
							"id": 2,
							"item_name": "Mapeamento de Sistemas",
							"time_hour": 4,
							"value": 380,
							"person_id": 3,
							"person": "Rafael",
							"project": "Automação Predial Inteligente",
							"phase_id": 2,
							"project_id": 2,
						}
					],
					"project_name": "Automação Predial Inteligente",
					"project_id": 2,
					"order": 1,
				}
			],
			"pricing": [
				{"id": 3, "name": "Custo fixo", "value": 18, "project_id": 2},
				{"id": 4, "name": "Impostos", "value": 14, "project_id": 2},
			],
		},
        {
			"id": 3,
			"description": "Projeto de modernização da infraestrutura de rede e servidores para aumento de performance e segurança da informação.",
			"account_name": "Fernanda Rocha",
			"start_date": "2026-04-12",
			"end_date": "2026-08-01",
			"customer_name": "Tech Solutions Corp",
			"project_name": "Upgrade de Infraestrutura de TI",
			"street": "Avenida das Américas",
			"street_number": 300,
			"street_additional": "Sala 402",
			"neighborhood": "Barra da Tijuca",
			"city": "Rio de Janeiro",
			"state": "RJ",
			"size": 600,
			"project_status": "Aprovado",
			"project_type": "Tecnologia",
			"project_classification": "Média Prioridade",
			"project_category": "TI",
			"template_id": 14,
			"user_id": 60,
			"costs": [
				{
					"id": 5,
					"description": "Servidores Cloud",
					"value": 8000,
					"project_name": "Upgrade de Infraestrutura de TI",
					"project_id": 3,
				},
				{
					"id": 6,
					"description": "Firewall Corporativo",
					"value": 4200,
					"project_name": "Upgrade de Infraestrutura de TI",
					"project_id": 3,
				},
			],
			"people": [
				{"id": 5, "name": "Diego", "position": "Arquiteto de Sistemas", "value_hour": 120},
				{"id": 6, "name": "Camila", "position": "Analista de Redes", "value_hour": 75},
			],
			"phases": [
				{
					"id": 3,
					"name_phase": "Etapa 1: Planejamento",
					"items_phases": [
						{
							"id": 3,
							"item_name": "Levantamento de Requisitos",
							"time_hour": 6,
							"value": 720,
							"person_id": 5,
							"person": "Diego",
							"project": "Upgrade de Infraestrutura de TI",
							"phase_id": 3,
							"project_id": 3,
						}
					],
					"project_name": "Upgrade de Infraestrutura de TI",
					"project_id": 3,
					"order": 1,
				}
			],
			"pricing": [
				{"id": 5, "name": "Custo fixo", "value": 20, "project_id": 3},
				{"id": 6, "name": "Impostos", "value": 16, "project_id": 3},
			],
		},
		{
			"id": 4,
			"description": "Projeto de construção de residência sustentável com reaproveitamento de água da chuva e uso de materiais ecológicos.",
			"account_name": "Juliana Pacheco",
			"start_date": "2026-05-01",
			"end_date": "2026-10-30",
			"customer_name": "Residencial Green Life",
			"project_name": "Casa Sustentável Modelo",
			"street": "Rua das Palmeiras",
			"street_number": 77,
			"street_additional": "Lote 12",
			"neighborhood": "Eco Park",
			"city": "Florianópolis",
			"state": "SC",
			"size": 280,
			"project_status": "Em andamento",
			"project_type": "Residencial",
			"project_classification": "Alta Prioridade",
			"project_category": "Sustentabilidade",
			"template_id": 9,
			"user_id": 34,
			"costs": [
				{
					"id": 7,
					"description": "Sistema de Captação de Água",
					"value": 5200,
					"project_name": "Casa Sustentável Modelo",
					"project_id": 4,
				},
				{
					"id": 8,
					"description": "Painéis Solares Residenciais",
					"value": 9800,
					"project_name": "Casa Sustentável Modelo",
					"project_id": 4,
				},
			],
			"people": [
				{"id": 7, "name": "André", "position": "Engenheiro Ambiental", "value_hour": 100},
				{"id": 8, "name": "Marina", "position": "Arquiteta", "value_hour": 90},
			],
			"phases": [
				{
					"id": 4,
					"name_phase": "Etapa 1: Projeto Arquitetônico",
					"items_phases": [
						{
							"id": 4,
							"item_name": "Desenho da Planta",
							"time_hour": 10,
							"value": 900,
							"person_id": 8,
							"person": "Marina",
							"project": "Casa Sustentável Modelo",
							"phase_id": 4,
							"project_id": 4,
						}
					],
					"project_name": "Casa Sustentável Modelo",
					"project_id": 4,
					"order": 1,
				}
			],
			"pricing": [
				{"id": 7, "name": "Custo fixo", "value": 12, "project_id": 4},
				{"id": 8, "name": "Impostos", "value": 10, "project_id": 4},
			],
		},
    ]

    return {"projetos": projeto_mock}