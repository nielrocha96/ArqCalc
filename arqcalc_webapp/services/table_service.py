# presenters.py ou services/table_service.py

class TablePresenter:
    """
    Transforma dados brutos na estrutura esperada pelo componente table.html
    Estrutura esperada: [{'id': 1, 'cells': [{'name': '...', 'value': '...'}]}]
    """
    
    @staticmethod
    def format_collection(collection, fields):
        """
        Recebe uma lista de objetos/dicionários e os mapeia para o formato da tabela.
        """
        table_data = []
        
        for item in collection:
            # Assume que o item pode ser um dicionário ou objeto do Django
            item_id = item.get('id') if isinstance(item, dict) else getattr(item, 'id', None)
            
            cells = []
            for field in fields:
                # Busca o valor dinamicamente
                value = item.get(field) if isinstance(item, dict) else getattr(item, field, "")
                
                cells.append({
                    'name': field,
                    'value': value,
                    'is_status': field == 'status', # Exemplo de lógica para classes CSS
                })
            
            table_data.append({
                'id': item_id,
                'cells': cells
            })
            
        return table_data