### EDITADO MAR-13
from django import template

register = template.Library()

@register.inclusion_tag('components/modal_template.html')
def render_modal(action_type, item_id, item_name=""):
  
    if action_type == 'delete':
        title        = "Confirmar Exclusão"
        content      = f"Tem certeza que deseja excluir '{item_name}'? Esta ação é irreversível."
        btn_class    = "btn_danger"
        confirm_text = "Excluir Agora"
    else: # 'edit'
        title        = "Editar Registro"
        content      = f"Deseja abrir o formulário de edição para '{item_name}'?"
        btn_class    = "btn_primary"
        confirm_text = "Editar"

    return {
        'title':        title,
        'content':      content,
        'btn_class':    btn_class,
        'confirm_text': confirm_text,
        'item_id':      item_id,
        'action_type':  action_type
    }