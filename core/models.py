from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    local_evento = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField(verbose_name='Data do Evento')
    data_criacao = models.DateTimeField(auto_now=True)

    ativar_desativar = models.NullBooleanField(blank=True)

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    # class Meta: db_table = 'evento' <- não funcionou
    def __str__(self):
        return self.titulo

    def get_data_evento(self):
        return self.data_evento.strftime('%d/%m/%Y %H h : %M min')

    def get_data_input_evento(self):
        return self.data_evento.strftime('%Y-%m-%dT%H:%M')

    # Eventos atrasados menor que 20 dias da data atual.
    def get_evento_atrasado(self):
        if self.data_evento < datetime.now() - timedelta(days=20):
            return True
        
        return False

    # Eventos próximos que são menor que a data de hoje (todos) porém no html se senão entrar no get_evento_atrasado
    def get_evento_proximo(self):
        if ((self.data_evento < datetime.now())):
            return True
        
        return False