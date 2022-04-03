from dataclasses import dataclass
from datetime import datetime


@dataclass
class Registro:
    data_viagem: str = None
    valor_corrida: str = None
    pagamento: str = None
    local_cobranca: str = None
    corrida_cancelada: bool = False
    tipo_corrida: str = None
    motorista: str = None
    endereco_partida: str = None
    horario_partida: str = None
    endereco_chegada: str = None
    horario_chegada: str = None
    link: str = None

    def clear_list(self, lista):
        dados_validos = lista[:2]
        temp = '\n'.join(dados_validos).replace(
            'Minus\n', '').replace('Surge', '').split('\n')
        return temp

    def cancelada(self, dados):
        dirs_cancelado = ['data_viagem', 'valor_corrida',
                          'local_cobranca', 'pagamento', 'motorista', 'endereco_partida']
        if len(dados) == 5:
            self.pagamento = None
            dirs_cancelado.remove('pagamento')
        for dir, dado in zip(dirs_cancelado, dados):
            if dir == 'motorista':
                self.motorista = ' '.join(dado.split(' ')[5:])
                try:
                    self.tipo_corrida = dado.split(' ')[3]
                except:
                    breakpoint
                continue
            setattr(self, dir, dado)
        self.corrida_cancelada = True

    def completa(self, dados):
        dirs_completo = ['data_viagem', 'valor_corrida', 'local_cobranca',
                         'pagamento', 'motorista', 'endereco_partida',
                         'horario_partida', 'endereco_chegada', 'horario_chegada']
        if len(dados) == 8:
            self.pagamento = None
            dirs_completo.remove('pagamento')
        for dir, dado in zip(dirs_completo, dados):
            if dir == 'motorista':
                self.motorista = ' '.join(dado.split(' ')[5:])
                self.tipo_corrida = dado.split(' ')[3]
                continue
            setattr(self, dir, dado)

    def save_registro(self, dados, link):

        temp = self.clear_list(dados)
        if "Cancelada" in temp[1]:
            temp[1] = temp[1].replace('Cancelada', '')
            self.cancelada(temp)
        else:
            self.completa(temp)
        try:
            self.pagamento = self.pagamento.replace('•••• ', '')
        except:
            pass
        try:
            self.data_viagem = datetime.strptime(
                self.data_viagem, '%d %B %Y, %I:%M%p')
        except TypeError:
            breakpoint()
        self.link = link
        return self

    @classmethod
    def from_dict(cls, dado):
        return cls(**dado)
