# EDITADO - ABRIL/2
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_LEFT

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Flowable, KeepTogether

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.fonts import addMapping

import os

import locale


def formatar_moeda(valor, moeda="EUR"):
    """
    Formata valores numéricos para string de moeda baseada na escolha do usuário.
    Simula o comportamento do CurrencyManager do JavaScript no lado do servidor.
    """
    configs = {
        'BRL': {'symbol': 'R$', 'decimal': ',', 'thousands': '.', 'locale': 'pt_BR'},
        'USD': {'symbol': '$', 'decimal': '.', 'thousands': ',', 'locale': 'en_US'},
        'EUR': {'symbol': '€', 'decimal': ',', 'thousands': '.', 'locale': 'de_DE'},
        'PYG': {'symbol': '₲', 'decimal': ',', 'thousands': '.', 'locale': 'es_PY'},
        'Peso argentino': {'symbol': 'ARS', 'decimal': ',', 'thousands': '.', 'locale': 'es_AR'},
    }
    
    conf = configs.get(moeda, configs['BRL'])
    
    # Formatação básica usando f-string para garantir precisão de 2 casas
    # O ReportLab aceita UTF-8, então os símbolos de Euro e Real funcionam bem.
    try:
        valor_float = float(valor)
        v_str = f"{valor_float:,.2f}"
        
        # Inverte separadores se necessário (padrão americano é vírgula para milhar)
        if conf['thousands'] == '.':
            v_str = v_str.replace(',', 'X').replace('.', ',').replace('X', '.')
            
        return f"{conf['symbol']} {v_str}"
    except:
        return f"{conf['symbol']} 0,00"


# =============================================================================
# CANVAS COSTUMIZADO PARA NUMERAÇÃO DE PÁGINAS
# =============================================================================
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total_pages = len(self._saved_page_states)

        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(total_pages)
            super().showPage()

        super().save()

    def draw_page_number(self, total_pages):
        # você NÃO desenha aqui — vamos usar no header_footer
        self._total_pages = total_pages

# =============================================================================
# CONFIGURAÇÃO DE FONTES
# =============================================================================
def registrar_fontes():
    """
    Tenta registrar a fonte Segoe UI do Windows para garantir a identidade visual.
    Caso não encontre, retorna 'Helvetica' como fallback padrão.
    """
    caminho_font = "C:/Windows/Fonts/segoeui.ttf"
    caminho_font_bold = "C:/Windows/Fonts/segoeuib.ttf"
    
    if os.path.exists(caminho_font) and os.path.exists(caminho_font_bold):
        # 1. Registra as fontes individualmente no ReportLab
        pdfmetrics.registerFont(TTFont('SegoeUI', caminho_font))
        pdfmetrics.registerFont(TTFont('SegoeUI-Bold', caminho_font_bold))
        
        # 2. MAPEAMENTO CRÍTICO: 
        # Vincula o estilo 'bold' da família 'SegoeUI' ao arquivo específico de negrito.
        addMapping('SegoeUI', 0, 0, 'SegoeUI')      # Normal
        addMapping('SegoeUI', 1, 0, 'SegoeUI-Bold') # Bold
        addMapping('SegoeUI', 0, 1, 'SegoeUI')      # Italic
        addMapping('SegoeUI', 1, 1, 'SegoeUI-Bold') # Bold-Italic
        
        return "SegoeUI"
    return "Helvetica"

font_padrao = registrar_fontes()

# =============================================================================
# COMPONENTES DE LAYOUT PERSONALIZADOS
# =============================================================================

class GradientLineText(Table):
    """
    Cria um título de seção com uma linha de gradiente estilizada abaixo do texto
    e opcionalmente uma linha divisória no topo.
    """
    def __init__(self, text, style, show_separator=True, show_top_divider=False):
        self.text_content = text.upper()
        self.style = style
        self.show_separator = show_separator
        self.show_top_divider = show_top_divider
        
        # Cálculo dinâmico da largura da linha baseado no tamanho do texto
        fontSize = style.fontSize if hasattr(style, 'fontSize') else 16
        largura_texto = len(self.text_content) * (fontSize * 0.55) + 10
        
        para = Paragraph(f"<b>{self.text_content}</b>", style)
        largura_util = 18 * cm 
        self.margin_top = 25 if show_top_divider else 10
        
        super().__init__([[para]], colWidths=[largura_util])
        
        estilos = [
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12), 
            ('TOPPADDING', (0, 0), (-1, -1), self.margin_top),
            ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
        ]
        self.setStyle(TableStyle(estilos))
        self.largura_linha = largura_texto

    def draw(self):
        """Método de desenho personalizado para incluir o gradiente e linhas divisórias."""
        super().draw()
        canvas = self.canv
        
        # Desenha a linha superior se for necessário (ex: em quebras de página)
        if self.show_top_divider and canvas.getPageNumber() > 1 and canvas._y < 750: 
            canvas.saveState()
            canvas.setStrokeColor(colors.HexColor("#C6B3DF"))
            canvas.setLineWidth(1.5)
            canvas.line(0, self._height, 18*cm, self._height)
            canvas.restoreState()

        # Desenha o retângulo com gradiente roxo abaixo do título
        if self.show_separator:
            canvas.saveState()
            h_linha = 4
            w_linha = self.largura_linha + 10
            x_inicio, y_inicio, raio = 0, 6, 1
            path = canvas.beginPath()
            path.roundRect(x_inicio, y_inicio, w_linha, h_linha, raio)
            canvas.clipPath(path, stroke=0)
            canvas.linearGradient(x_inicio, y_inicio, x_inicio + w_linha, y_inicio,
                                  (colors.HexColor("#4C2192"), colors.HexColor("#8454CC")))
            canvas.restoreState()


# =============================================================================
# HEADER REPETINDO + GERENCIAMENTO DE QUEBRA DE PÁGINA
# =============================================================================
class HeaderRepeatingSection(Flowable):
    """
    Componente complexo que agrupa um título (GradientLineText) e uma tabela.
    Gerencia a repetição do título caso a tabela seja dividida entre páginas.
    """
    def __init__(self, title_text, table_obj, style, is_continuation=False):
        super().__init__()
        self.title_text = title_text
        self.table_obj = table_obj
        self.style = style
        self.is_continuation = is_continuation
        self.title_flowable = GradientLineText(title_text, style, show_separator=True, 
                                              show_top_divider=not is_continuation)
        self.width = 18 * cm
        self.height = 0

    def wrap(self, availWidth, availHeight):
        """Calcula o espaço necessário para o título e a tabela interna."""
        tw, th = self.title_flowable.wrap(availWidth, availHeight)
        mw, mh = self.table_obj.wrap(availWidth, max(0, availHeight - th))
        self.height = th + mh + 10 
        return self.width, self.height

    def draw(self):
        """Renderiza os componentes no canvas aplicando translação de coordenadas."""
        canvas = self.canv
        tw, th = self.title_flowable.wrap(self.width, self.height)
        canvas.saveState()
        canvas.translate(0, self.height - th)
        self.title_flowable.canv = canvas
        self.title_flowable.draw()
        canvas.restoreState()
        canvas.saveState()
        self.table_obj.canv = canvas
        self.table_obj.draw()
        canvas.restoreState()

    def split(self, availWidth, availHeight):
        """Lógica de quebra de página: se a tabela não couber, divide em duas seções com o mesmo título."""
        tw, th = self.title_flowable.wrap(availWidth, availHeight)
        if availHeight < th + 25: return []
        parts = self.table_obj.split(availWidth, availHeight - th)
        if not parts: return []
        p1 = HeaderRepeatingSection(self.title_text, parts[0], self.style, is_continuation=self.is_continuation)
        p2 = HeaderRepeatingSection(f"{self.title_text}", parts[1], self.style, is_continuation=True)
        return [p1, p2]

def converter_tempo_para_float(tempo_str):
    """Converte formatos como '1h30', '1:30' ou '1,5' para float."""
    if not tempo_str:
        return 0.0
    try:
        tempo_str = str(tempo_str).replace(',', '.').lower()
        if 'h' in tempo_str:
            # Trata '1h30'
            partes = tempo_str.split('h')
            horas = float(partes[0]) if partes[0] else 0.0
            minutos = float(partes[1]) / 60 if len(partes) > 1 and partes[1] else 0.0
            return horas + minutos
        return float(tempo_str)
    except (ValueError, TypeError):
        return 0.0


# =============================================================================
# SERVIÇO DE GERAÇÃO DE PDF
# =============================================================================
class ArqCalcReporter:
    """Classe principal responsável por montar a estrutura do documento PDF."""
    def __init__(self, response, moeda='BRL'):
        # Configuração do template base (margens e tamanho A4)
        self.user_moeda = moeda
        self.doc = SimpleDocTemplate(
            response, pagesize=A4, 
            rightMargin=1.5*cm, 
            leftMargin=1*cm, 
            topMargin=3.5*cm, 
            bottomMargin=2*cm,
            allowSplitting=1
        )
        self.styles = getSampleStyleSheet()
        font_bold = 'SegoeUI-Bold' if font_padrao == 'SegoeUI' else 'Helvetica-Bold'
        
        # Estilos customizados para títulos de seções e subseções
        self.styles.add(ParagraphStyle(
            name='SecaoTitle', parent=self.styles['Normal'],
            fontName=font_bold, fontSize=16, textColor=colors.HexColor('#4B2C82'),
            spaceAfter=12, leading=20
        ))
        self.styles.add(ParagraphStyle(
            name='SubSecaoTitle', parent=self.styles['Normal'],
            fontName=font_bold, fontSize=11, textColor=colors.HexColor('#4B2C82'),
            spaceBefore=10, spaceAfter=8
        ))

        self.estilo_label = ParagraphStyle('PrecLabel', parent=self.styles['Normal'], fontName=font_padrao, textColor=colors.black, leftIndent=5)
        self.estilo_bold = ParagraphStyle('PrecBold', parent=self.styles['Normal'], fontName=font_bold, textColor=colors.black, leftIndent=5)

    def header_footer(self, canvas, doc):
        """Desenha o cabeçalho fixo e o rodapé espelhado em cada página."""
        canvas.saveState()
        largura_pag, altura_pag = A4[0], A4[1]

        canvas.setFillColor(colors.black)
        canvas.rect(0, altura_pag - 10, largura_pag, 10, fill=1, stroke=0)

        canvas.setFillColor(colors.HexColor('#F2F2F2'))
        canvas.rect(0, altura_pag - 50, largura_pag, 40, fill=1, stroke=0)

        x_roxo, y_roxo, w_roxo, h_roxo = 1.5 * cm, altura_pag - 55, 120, 50
        path = canvas.beginPath()
        path.roundRect(x_roxo, y_roxo, w_roxo, h_roxo, 4)

        canvas.saveState()
        canvas.clipPath(path, stroke=0, fill=0)
        canvas.linearGradient(
            x_roxo, y_roxo + h_roxo, x_roxo, y_roxo,
            (colors.HexColor('#6E45AB'), colors.HexColor('#321265'))
        )
        canvas.restoreState()

        canvas.setFillColor(colors.white)
        canvas.setFont('SegoeUI-Bold' if font_padrao == 'SegoeUI' else 'Helvetica-Bold', 18)
        canvas.drawCentredString(x_roxo + 60, y_roxo + 18, "ARQCALC")

        canvas.setFillColor(colors.black)
        canvas.setFont('SegoeUI-Bold' if font_padrao == 'SegoeUI' else 'Helvetica-Bold', 14)
        canvas.drawString(x_roxo + 140, altura_pag - 30, getattr(doc, 'projeto_nome', "").upper())

        canvas.setFont(font_padrao, 10)
        canvas.setFillColor(colors.grey)
        canvas.drawString(x_roxo + 140, altura_pag - 44, getattr(doc, 'data_emissao', ""))

        # =========================
        # FOOTER (rodapé espelhado)
        # =========================
        footer_black_h = 8
        footer_grey_h = 16

        # Cinza acima
        canvas.setFillColor(colors.HexColor('#F2F2F2'))
        canvas.rect(0, footer_black_h, largura_pag, footer_grey_h, fill=1, stroke=0)

        # Preto embaixo
        canvas.setFillColor(colors.black)
        canvas.rect(0, 0, largura_pag, footer_black_h, fill=1, stroke=0)
        

        # Contador centralizado
        footer_black_h = 8
        footer_grey_h = 16

        # Cinza
        canvas.setFillColor(colors.HexColor('#F2F2F2'))
        canvas.rect(0, footer_black_h, largura_pag, footer_grey_h, fill=1, stroke=0)

        # Preto
        canvas.setFillColor(colors.black)
        canvas.rect(0, 0, largura_pag, footer_black_h, fill=1, stroke=0)


        current = canvas.getPageNumber()
        total = getattr(canvas, '_total_pages', 1)
        texto = f"{current}-{total}"

        box_w = 20
        box_h = 20
        box_x = (largura_pag - box_w) / 2
        box_y = 0

        # fundo roxo
        canvas.setFillColor(colors.HexColor('#6E45AB'))
        canvas.setStrokeColor(colors.HexColor('#6E45AB'))  # evita borda preta bugada
        canvas.roundRect(box_x, box_y, box_w, box_h, 10, fill=1, stroke=0)

        # texto
        canvas.setFillColor(colors.white)
        canvas.setFont(
            'SegoeUI-Bold' if font_padrao == 'SegoeUI' else 'Helvetica-Bold',
            9
        )

        canvas.drawCentredString(
            largura_pag / 2,
            box_y + (box_h / 2) - 3,
            texto
        )

        canvas.restoreState()

    def criar_tabela_padrao(self, dados, col_widths, repeat_header=True):
        """Helper para criar objetos Table com estilo 'zebrado' e fontes configuradas."""
        t = Table(dados, colWidths=col_widths, repeatRows=1 if repeat_header else 0)
        cor_header, cor_zebra = colors.HexColor('#FBF8FF'), colors.HexColor('#FFFFFF')
        style_list = [
            ('FONTNAME', (0, 0), (-1, -1), font_padrao),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
        ]
        # Aplicação manual do efeito zebrado linha a linha
        for i in range(len(dados)):
            bg = cor_header if i % 2 == 0 else cor_zebra
            style_list.append(('BACKGROUND', (0, i), (-1, i), bg))
        t.setStyle(TableStyle(style_list))
        return t

    def build(self, db_data):
        """Processa o dicionário de dados (db_data) e constrói o PDF elemento por elemento."""
        elements = []
        self.doc.projeto_nome = db_data.get('projeto_nome', "PROJETO")
        self.doc.data_emissao = db_data.get('data_emissao', "")
        user_moeda = db_data.get('moeda', 'BRL')

        # Tags HTML inline para formatação de Paragraphs
        tag_label = '<b><font color="#4B2C82">'
        end_tag = '</font></b>'

        def fmt_field(label, value):
            return Paragraph(f'{tag_label}{label}:{end_tag} {value}', self.styles['Normal'])

        def fmt_label_only(label):
            return Paragraph(f'{tag_label}{label}{end_tag}', self.styles['Normal'])

        # ==================================
        #      SEÇÃO DADOS DO PROJETO  
        # ==================================
        dados_cli = [
            [fmt_field("Cliente", db_data['cliente']), fmt_field("Responsável", db_data['responsavel'])],
            [fmt_field("Bairro", db_data['bairro']), fmt_field("Início", db_data['data_inicio'])],
            [fmt_field("Cidade/UF", db_data['cidade']), fmt_field("Término", db_data['data_fim'])]
        ]
        t_dados = self.criar_tabela_padrao(dados_cli, [9*cm, 9*cm], repeat_header=False)
        elements.append(HeaderRepeatingSection("DADOS", t_dados, self.styles['SecaoTitle'], is_continuation=False))
        elements.append(Spacer(1, 0.6*cm))

        # ==================================
        #      SEÇÃO CUSTOS ESPECÍFICOS  
        # ==================================
        custos_brutos = db_data['custos_especificos']
        custos_formatados = []
        # Organiza os custos em duas colunas
        for i in range(0, len(custos_brutos), 2):
            linha = [fmt_field(custos_brutos[i]['nome'],  formatar_moeda(custos_brutos[i]['valor'], user_moeda))]
            if i + 1 < len(custos_brutos):
                linha.append(fmt_field(custos_brutos[i+1]['nome'], formatar_moeda(custos_brutos[i+1]['valor'], user_moeda)))
            else: linha.append("")
            custos_formatados.append(linha)
        t_custos = self.criar_tabela_padrao(custos_formatados, [9*cm, 9*cm], repeat_header=False)
        elements.append(HeaderRepeatingSection("CUSTOS ESPECÍFICOS", t_custos, self.styles['SecaoTitle']))
        elements.append(Spacer(1, 0.6*cm))

        # =========================
        #   SEÇÃO PROFISSIONAIS 
        # =========================
        
        r_prof = [[
            fmt_label_only(p['nome']), 
            p['cargo'], 
            fmt_field("Valor por hora", formatar_moeda(p['valor_hora'], user_moeda))
        ] for p in db_data['profissionais']]
        t_prof = self.criar_tabela_padrao(r_prof, [5*cm, 7*cm, 6*cm], repeat_header=False)
        elements.append(HeaderRepeatingSection("PROFISSIONAIS", t_prof, self.styles['SecaoTitle']))
        elements.append(Spacer(1, 0.6*cm))
        
        # =======================
        #     SEÇÃO ETAPAS  
        # =======================
        secao_etapas = []
        titulo_etapas = GradientLineText("ETAPAS", self.styles['SecaoTitle'], show_top_divider=True)

        cor_roxo_escuro = colors.HexColor('#4B2C82')
        cor_zebra_claro = colors.HexColor('#FBF8FF')

        for i, etapa in enumerate(db_data['etapas']):
            # Cabeçalho da Etapa específica
            header_row = [
                Paragraph(f'<b><font color="{cor_roxo_escuro}">{etapa["numero"]}. {etapa["nome"].upper()}</font></b>', self.styles['Normal']),
                Paragraph(f'<font color="{cor_roxo_escuro}"><b>Tempo:</b></font> (h): <b>{etapa.get("total_tempo", "0,0")}</b>', self.styles['Normal']),
                Paragraph(f'<font color="{cor_roxo_escuro}"><b>Custo:</b></font> ({user_moeda}): <b>{formatar_moeda(etapa.get("total_custo", 0.0), user_moeda)}</b>', self.styles['Normal'])
            ]
            
            dados_da_tabela = [header_row]
            
            # Subetapas daquela etapa
            for s in etapa['subetapas']:
                linha = [
                    Paragraph(s['nome'], self.styles['Normal']),
                    Paragraph(f"({s['resp']})", self.styles['Normal']),
                    Paragraph(f'<b><font color="{cor_roxo_escuro}">Tempo:</font></b> {s["tempo"]}', self.styles['Normal'])
                ]
                dados_da_tabela.append(linha)

            t_etapa = self.criar_tabela_padrao(dados_da_tabela, [5*cm, 7*cm, 6*cm], repeat_header=True)

            style_list = [
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('LEFTPADDING', (0, 0), (-1, -1), 8),
                ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
                ('BACKGROUND', (0, 0), (-1, 0), cor_zebra_claro),
            ]
            
            for row_idx in range(1, len(dados_da_tabela)):
                bg = colors.white if row_idx % 2 != 0 else cor_zebra_claro
                style_list.append(('BACKGROUND', (0, row_idx), (-1, row_idx), bg))
            
            t_etapa.setStyle(TableStyle(style_list))

            # Adiciona o título global apenas na primeira etapa, usando KeepTogether para evitar órfãos
            if i == 0:
                elements.append(KeepTogether([titulo_etapas, t_etapa]))
            else:
                elements.append(t_etapa)

            # Divisor visual entre etapas
            if i < len(db_data['etapas']) - 1:
                linha_sep = Table([['']], colWidths=[18*cm], rowHeights=[1])
                linha_sep.setStyle(TableStyle([
                    ('LINEBELOW', (0, 0), (-1, 0), 1, cor_roxo_escuro),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ]))
                elements.append(Spacer(1, 0.3*cm))
                elements.append(linha_sep)
                elements.append(Spacer(1, 0.4*cm))
            else:
                elements.append(Spacer(1, 0.6*cm))
        
        # ============================
        #      SEÇÃO PRECIFICAÇÃO 
        # ============================
        prec_data = db_data.get('precificacao', {})
        comp_custo = prec_data.get('composicao_custo', {})
        p_venda = prec_data.get('preco_venda', {})

        cor_roxa_suave = colors.Color(0.95, 0.93, 0.98)
        cor_roxa_linha = colors.Color(0.3, 0.1, 0.5)
        preto = colors.black

        estilo_label = ParagraphStyle('PrecLabel', parent=self.styles['Normal'], fontName=font_padrao, textColor=preto, leftIndent=5)
        estilo_bold = ParagraphStyle('PrecBold', parent=self.styles['Normal'], fontName=font_padrao + '-Bold', textColor=preto, leftIndent=5)

        # Tabela de Composição de Custos
        r_comp = [
            [fmt_label_only("COMPOSIÇÃO DO PREÇO FINAL")],
            [Paragraph("Custos variáveis:", estilo_label),"", Paragraph(f"+ <b>{formatar_moeda(comp_custo.get('custo_variavel', 0), user_moeda)}</b>", self.styles['Normal'])],
            [Paragraph("Custos específicos:", estilo_label),"", Paragraph(f"+ {formatar_moeda(comp_custo.get('custo_especifico', 0), user_moeda)}", self.styles['Normal'])],
            [Paragraph("Custos fixos:", estilo_label),"", Paragraph(f"+ {formatar_moeda(comp_custo.get('custo_fixo', 0), user_moeda)}", self.styles['Normal'])],
            [Paragraph("CUSTOS OPERACIONAIS:", estilo_bold),"", Paragraph(f"<b>= {formatar_moeda(comp_custo.get('custo_operacional', 0), user_moeda)}</b>", self.styles['Normal'])]
        ]
        
        t_comp = self.criar_tabela_padrao(r_comp, [10*cm,  4*cm, 4*cm], repeat_header=True)
        t_comp.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('BACKGROUND', (0, 0), (-1, 0), cor_roxa_suave),
            ('BACKGROUND', (0, 2), (-1, 2), cor_roxa_suave),
            ('BACKGROUND', (0, 4), (-1, 4), cor_roxa_suave),
            ('LINEBELOW', (2, 4), (1, 3), 1, cor_roxa_linha),
            ('BOTTOMPADDING', (1, 3), (1, 3), 9), 
        ]))

        elements.append(Spacer(1, 0.5*cm))
        elements.append(HeaderRepeatingSection("PRECIFICAÇÃO", t_comp, self.styles['SecaoTitle']))

        # Tabela de Preço de Venda e Margem
        r_venda = [
            [fmt_label_only("PREÇO DE VENDA"),"", Paragraph(f"<b>{formatar_moeda(p_venda.get('preco_venda', 0), user_moeda)}</b>", self.styles['Normal'])],

            [Paragraph("Impostos:", estilo_label), "", Paragraph(f"+ <b>{formatar_moeda(p_venda.get('imposto', 0), user_moeda)}</b>", self.styles['Normal'])],

            [Paragraph("Comissões:", estilo_label), "", Paragraph(f"+ <b>{formatar_moeda(p_venda.get('comissoes', 0), user_moeda)}</b>", self.styles['Normal'])],

            [Paragraph("Custos operacionais:", estilo_label), "", Paragraph(f"+ <b>{formatar_moeda(p_venda.get('custo_operacional', 0), user_moeda)}</b>", self.styles['Normal'])],

            [Paragraph(f"<b>LUCRO:</b>", estilo_bold), "", Paragraph(f"<b>{formatar_moeda(p_venda.get('preco_final', 0), user_moeda)}</b>", self.styles['Normal'])],
            [
                Paragraph(f"<b>LUCRO(%):</b> {p_venda.get('margem_lucro', 0):.2f}", estilo_label),
                Paragraph(f"<b>PONTO DE EQUILÍBRIO: {formatar_moeda(p_venda.get('ponto_equilibrio', 0), user_moeda)}</b>", self.styles['Normal'])
            ]
        ]

        t_venda = self.criar_tabela_padrao(r_venda, [7*cm,  7*cm, 4*cm], repeat_header=True)
        t_venda.setStyle(TableStyle([
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('BACKGROUND', (0, 0), (-1, 0), cor_roxa_suave),
            ('BACKGROUND', (0, 2), (-1, 2), cor_roxa_suave),
            ('BACKGROUND', (0, 4), (-1, 4), cor_roxa_suave),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        elements.append(Spacer(1, 0.3*cm))
        elements.append(t_venda)

        # =====================
        #     SEÇÃO RESUMO  
        # =====================
        elements.append(GradientLineText("RESUMO", self.styles['SecaoTitle'], show_top_divider=True))
        elements.append(Spacer(1, 0.4*cm))

        cor_roxo = colors.HexColor('#4B2C82')
        cor_roxo_claro = colors.HexColor('#F3EEFF')

        # ESTILOS ESPECÍFICOS PARA A SEÇÃO DE RESUMO
        self.styles.add(ParagraphStyle(
            name='ResumoNormal',
            parent=self.styles['Normal'],
            fontName=font_padrao,
            fontSize=10,
            leading=12,
        ))

        self.styles.add(ParagraphStyle(
            name='ResumoHeader',
            parent=self.styles['Normal'],
            fontName=font_padrao + '-Bold',
            fontSize=10,
            textColor=cor_roxo,
            leading=12,
        ))

        self.styles.add(ParagraphStyle(
            name='ResumoTotal',
            parent=self.styles['Normal'],
            fontName=font_padrao + '-Bold',
            fontSize=10,
            textColor=colors.black,
            leading=12,
        ))

        def p(txt):
            return Paragraph(str(txt), self.styles['ResumoNormal'])

        def p_header(txt):
            return Paragraph(str(txt), self.styles['ResumoHeader'])

        def p_total(txt):
            return Paragraph(str(txt), self.styles['ResumoTotal'])


        # FUNÇÃO DE ESTILO DA TABELA
        def aplicar_estilo_tabela_resumo(tabela_obj, num_linhas):
            GAP = 6

            estilo = TableStyle([
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 12),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),

                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),

                # GAP ENTRE CÉLULAS
                ('INNERGRID', (0, 0), (-1, -1), GAP, colors.white),

                # HEADER BG
                ('BACKGROUND', (0, 0), (-1, 0), cor_roxo_claro),
            ])

            # Zebra
            for i in range(1, num_linhas):
                if i % 2 == 0:
                    estilo.add('BACKGROUND', (0, i), (-1, i), cor_roxo_claro)

            # Linha total
            estilo.add('LINEABOVE', (0, -1), (-1, -1), 2, cor_roxo)

            tabela_obj.setStyle(estilo)
            return tabela_obj


        # CUSTO POR PROFISSIONAL
        elements.append(Paragraph("CUSTO POR PROFISSIONAL", self.styles['SubSecaoTitle']))

        res_prof_data = [
            [p_header("PROFISSIONAL"), p_header("TOTAL (h)"), p_header("CUSTO (R$)"), p_header("PROPORÇÃO CUSTO (%)")]
        ]

        total_horas_geral = 0.0
        total_custo_geral = db_data.get('total_custo_geral', 0)

        prof_summary = {}

        for etapa in db_data['etapas']:
            for sub in etapa['subetapas']:
                resp = sub['resp']
                if resp not in prof_summary:
                    prof_summary[resp] = {'h': 0.0, 'c': 0.0}

                h_val = converter_tempo_para_float(sub['tempo'])

                prof_summary[resp]['h'] += h_val
                prof_summary[resp]['c'] += sub.get('custo_calculado', 0)
                total_horas_geral += h_val

        for nome, val in prof_summary.items():
            prop = (val['c'] / total_custo_geral * 100) if total_custo_geral > 0 else 0
            res_prof_data.append([
                p(nome),
                p(f"{val['h']:.2f}"),
                p(formatar_moeda(val['c'], user_moeda)), # <--- aqui
                p(f"{prop:.1f}%")
            ])

        # TOTAL
        res_prof_data.append([
            p_total("TOTAL"),
            p_total(f"{total_horas_geral:.2f}"),
            p_total(formatar_moeda(total_custo_geral, user_moeda)), # <--- aqui
            p_total("")
        ])

        t_prof = Table(res_prof_data, colWidths=[7*cm, 3.5*cm, 3.5*cm, 4*cm])
        elements.append(aplicar_estilo_tabela_resumo(t_prof, len(res_prof_data)))
        elements.append(Spacer(1, 0.8*cm))


        # CUSTO POR ETAPA
        elements.append(Paragraph("CUSTO POR ETAPA", self.styles['SubSecaoTitle']))

        res_etapa_data = [
            [p_header("ETAPA"), p_header("TOTAL (h)"), p_header("CUSTO (R$)"), p_header("PROPORÇÃO CUSTO (%)")]
        ]

       
        total_horas_etapas = 0.0
        total_custo_etapas = 0.0

        for etapa in db_data['etapas']:
            custo_e = etapa.get('total_custo', 0.0)

            # converter tempo string → float
            tempo_e = converter_tempo_para_float(etapa.get('total_tempo', 0))

            prop = (custo_e / total_custo_geral * 100) if total_custo_geral > 0 else 0

            res_etapa_data.append([
                p(etapa['nome']),
                p(f"{tempo_e:.2f}"),
                p(formatar_moeda(custo_e, user_moeda)), # <--- aqui
                p(f"{prop:.1f}%")
            ])

            # soma  por etapa
            total_horas_etapas += tempo_e
            total_custo_etapas += custo_e

        # TOTAL
        res_etapa_data.append([
            p_total("TOTAL"),
            p_total(f"{total_horas_etapas:.2f}"),
            p_total(formatar_moeda(total_custo_etapas, user_moeda)), # <--- aqui
            p_total("")
        ])

        t_etapa = Table(res_etapa_data, colWidths=[7*cm, 3.5*cm, 3.5*cm, 4*cm])
        elements.append(aplicar_estilo_tabela_resumo(t_etapa, len(res_etapa_data)))

        # FINALIZAÇÃO
        self.doc.build(
            elements,
            onFirstPage=self.header_footer,
            onLaterPages=self.header_footer,
            canvasmaker=NumberedCanvas
        )   