# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Aviso, Atendimento, Materia

class RegistrarUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='Nome')
    last_name = forms.CharField(max_length=30, label='Sobrenome')
    email = forms.EmailField(max_length=100)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(
                email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Este email já está em uso.')
        return email


class AvisoForm(forms.ModelForm):

    class Meta:
         model = Aviso
         fields = [
             'turma',
             'materia',
             'tipo_aviso',
             'comentarios',
             'data_final',
         ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Busca as turmas que tem como representante o usuário logado
        self.fields['turma'].queryset = self.fields['turma'].queryset.filter(representante=user)
        # Traz as matérias em que a turma tem como representante o usuário logado
        self.fields['materia'].queryset = self.fields['materia'].queryset.filter(turma__representante=user)

class AtendimentoForm(forms.ModelForm):

    class Meta:
         model = Atendimento
         fields = [
             'turma',
             'professor',
             'dia',
             'horario_inicio',
             'horario_fim'
         ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Busca as turmas que tem como representante o usuário logado
        self.fields['turma'].queryset = self.fields['turma'].queryset.filter(representante=user)

class MateriaForm(forms.ModelForm):

    class Meta:
         model = Materia
         fields = [
             'nome',
             'local',
             'dia',
             'horario_inicio',
             'horario_fim',
             'turma',
             'professor'
         ]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Busca as turmas que tem como representante o usuário logado
        self.fields['turma'].queryset = self.fields['turma'].queryset.filter(representante=user)