import os
import django

# Substitua 'arqcalc_django.settings' pelo caminho correto do seu settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'arqcalc_django.settings')
django.setup()

from django.core.mail import send_mail
try:
    send_mail(
        'Teste de Conexão',                                          # assunto
        'email usando o dotenv',        # mensagem
        'contato@arqcalc.com.br',                                    # remetente
        ['dr.niel96@gmail.com'],                                     # lista de destinatários
        fail_silently=False,
        #html_message='<h1>Olá!</h1><p>Sua senha é <strong>123</strong></p>' # Opcional
        #bcc=['seu-email@hostinger.com.br'], # Você recebe uma cópia oculta
    )
except Exception as e: print('ERRO'+e)