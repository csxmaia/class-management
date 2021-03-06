from braces.views import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
# from django.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic import DetailView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from . import models
from .forms import RegistrarUserForm, AvisoForm, AtendimentoForm, MateriaForm


#Telas iniciais

class Index(TemplateView):
    template_name = 'base.html'

#------------CreateView--------------#
class UserCreateView(CreateView, #AnonymousRequiredMixin
                     ):
    model = User
    template_name = 'form.html'
    form_class = RegistrarUserForm
    success_url = reverse_lazy('login') # pra onde ir depois de cadastrar

    # Como enviar outros dados para tela
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Registrar-se como Aluno'
        context['input'] = 'Enviar'
        return context

class TurmaCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView): #Tela de crianção de turmas
    group_required = u"representante"
    model = models.Turma
    template_name = 'form.html'
    login_url = '/login/'
    success_url = reverse_lazy('visualizar_turma') # pra onde ir depois de cadastrar
    fields = [
        'nome',
        'alunos',
        'colegio'
    ]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Cadastro de Turma'
        context['input'] = 'Cadastrar'
        return context

    # trabalhar com os dados do formulário antes de salvar
    def form_valid(self, form):
        # Definindo o usuário da sessão como representante
        form.instance.representante = self.request.user
        return super().form_valid(form)


class ProfessorCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):  # Cadastro de Professores
    group_required = u"representante"
    template_name = 'form.html'
    model = models.Professor
    login_url = '/login/'
    success_url = reverse_lazy('visualizar_professor')  # pra onde ir depois de cadastrar
    fields = [
        'nome',
        'email'
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Cadastro de Professores'
        context['input'] = 'Adicionar Professor'
        return context


class ColegioCreateView(LoginRequiredMixin, CreateView):  # Cadastro de Professores
    template_name = 'form.html'
    model = models.Colegio
    login_url = '/login/'
    success_url = reverse_lazy('visualizar_colegio')  # pra onde ir depois de cadastrar
    fields = [
        'nome'
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Cadastro de Colegios'
        context['input'] = 'Adicionar Colegio'
        return context


class MateriaCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView): #Cadastro de Materias
    group_required = u"representante"
    template_name = 'form.html'
    model = models.Materia
    login_url = '/login/'
    success_url = reverse_lazy('visualizar_materia')
    # fields = [
    #     'nome',
    #     'local',
    #     'dia',
    #     'horario_inicio',
    #     'horario_fim',
    #     'turma',
    #     'professor'
    # ]
    form_class = MateriaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Cadastro de Materias'
        context['input'] = 'Adicionar Matéria'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class AtendimentoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView): #Cadastro de atendimentos
    group_required = u"representante"
    template_name = 'form.html'
    model = models.Atendimento
    login_url = '/login/'
    success_url = reverse_lazy('visualizar_atendimento')

    form_class = AtendimentoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Cadastro de Atendimento'
        context['input'] = 'Adicionar Atendimento'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class AvisoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):  #Cadastro de Aviso
    group_required = u"representante"
    template_name = 'form.html'
    model = models.Aviso
    login_url = '/login/'
    success_url = reverse_lazy('visualizar_aviso')

    # Define um formulário personalizado para esta View
    form_class = AvisoForm

   # fields = [
   #     'turma',
   #     'materia',
   #     'tipo_aviso',
   #     'comentarios',
   #     'data_final'
   # ]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Cadastrar Aviso'
        context['input'] = 'Adicionar Aviso'
        return context

    # Sobreescreve o método para poder guardar alguns dados no parâmetro 'kwargs'.
    # Assim podemos enviar dados para o forms.py
    # neste caso, guardamos o usuário que está acessando o site na posição 'instance'
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


# --------------- FIM DOS CADASTROS ---------------------#


# --------------- UpdateViews --------------- #
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = [
        'first_name',
        'last_name',
        'email',
        # 'is_active'
    ]
    template_name = 'form.html'

    # form_class = RegistrarUserForm
    success_url = reverse_lazy('index') # pra onde ir depois de cadastrar

    # Busca o usuário atual da seção
    def get_object(self, **kwargs):
        object = User.objects.get(pk=self.request.user.pk)
        return object

    # Como enviar outros dados para tela
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Alterar meus dados'
        context['input'] = 'Atualizar'
        return context


class TurmaUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView): #Tela de crianção de turmas
    group_required = u"representante"
    model = models.Turma
    template_name = 'form.html'
    login_url = '/login/'
    success_url = reverse_lazy('visualizar_turma')
    fields = [
        'nome',
        'alunos',
        'representante',
        'colegio'
    ]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Editar Turma'
        context['input'] = 'Salvar'
        return context

    # Função que pega o objeto do ID que está vindo na URL
    def get_object(self, queryset=None):
        # Além da pk da URL, verifica se o usuário também é representante
        self.object = models.Turma.objects.get(pk=self.kwargs['pk'], representante=self.request.user)
        return self.object


class ProfessorUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):  #Cadastro de Aviso
    group_required = u"representante"
    template_name = 'form.html'
    model = models.Professor
    login_url = '/login/'
    success_url = reverse_lazy('visualizar_professor')  # pra onde ir depois de cadastrar
    fields = [
        'nome',
        'email'
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Editar Professor'
        context['input'] = 'Salvar'
        return context


class ColegioUpdateView(LoginRequiredMixin, UpdateView):  # Cadastro de Professores
    template_name = 'form.html'
    model = models.Colegio
    login_url = '/login/'
    success_url = reverse_lazy('visualizar_colegio')  # pra onde ir depois de cadastrar
    fields = [
        'nome'
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Editar Colegio'
        context['input'] = 'Salvar'
        return context


class MateriaUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView): #Cadastro de Materias
    group_required = u"representante"
    template_name = 'form.html'
    model = models.Materia
    login_url = '/login/'
    success_url = reverse_lazy('visualizar_materia')

    form_class = MateriaForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Editar Materia'
        context['input'] = 'Salvar'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class AtendimentoUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView): #Cadastro de atendimentos
    group_required = u"representante"
    template_name = 'form.html'
    model = models.Atendimento
    login_url = '/login/'
    success_url = reverse_lazy('visualizar_atendimento')

    form_class = AtendimentoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Editar Atendimento'
        context['input'] = 'Salvar'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class AvisoUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):  #Cadastro de Aviso
    group_required = u"representante"
    template_name = 'form.html'
    model = models.Aviso
    login_url = '/login/'
    success_url = reverse_lazy('visualizar_aviso')

    form_class = AvisoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Editar Aviso'
        context['input'] = 'Salvar'
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


#---------------Delete View--------------#
class ProfessorDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):  #Cadastro de Aviso
    group_required = u"representante"
    template_name = 'formdelete.html'
    model = models.Professor
    login_url = '/login/'
    success_url = reverse_lazy('visualizar_professor')  # pra onde ir depois de cadastrar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Editar Professor'
        context['cadastro'] = 'o Professor'
        context['item'] = models.Professor.objects.get(pk=self.kwargs['pk']).nome
        context['input'] = 'Salvar'
        return context


#    def post(self, *args, **kwargs):
#        from django.db.models import ProtectedError
#        try:
#            return super().delete(self, *args, **kwargs)
#        except ProtectedError:
#            return reverse_lazy('protectDelete')


class ColegioDeleteView(LoginRequiredMixin, DeleteView):  # Cadastro de Professores
    template_name = 'formdelete.html'
    model = models.Colegio
    login_url = '/login/'
    success_url = reverse_lazy('visualizar_colegio')  # pra onde ir depois de cadastrar

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Editar Colegio'
        context['cadastro'] = 'o Colegio'
        context['item'] = models.Colegio.objects.get(pk=self.kwargs['pk']).nome
        context['input'] = 'Salvar'
        return context


class MateriaDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView): #Cadastro de Materias
    group_required = u"representante"
    template_name = 'formdelete.html'
    model = models.Materia
    login_url = '/login/'
    success_url = reverse_lazy('visualizar_materia')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Editar Materia'
        context['cadastro'] = 'a Materia'
        context['item'] = models.Materia.objects.get(pk=self.kwargs['pk']).nome
        context['input'] = 'Salvar'
        return context


class AtendimentoDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView): #Cadastro de atendimentos
    group_required = u"representante"
    template_name = 'formdelete.html'
    model = models.Atendimento
    login_url = '/login/'
    success_url = reverse_lazy('visualizar_atendimento')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Editar Atendimento'
        context['cadastro'] = 'o Atendimento do Professor'
        context['item'] = models.Atendimento.objects.get(pk=self.kwargs['pk']).professor
        context['input'] = 'Salvar'
        return context


class AvisoDeleteView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):  #Cadastro de Aviso
    group_required = u"representante"
    template_name = 'formdelete.html'
    model = models.Aviso
    login_url = '/login/'
    success_url = reverse_lazy('visualizar_aviso')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Editar Aviso'
        context['cadastro'] = 'o Aviso da Turma'
        context['item'] = models.Aviso.objects.get(pk=self.kwargs['pk']).turma
        context['input'] = 'Salvar'
        return context
#----------------List View---------------#
class UserListView(generic.ListView):
    model = User
    template_name = 'list/user_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Usuarios'
        return context

class ProfessorListView(generic.ListView):
    model = models.Professor
    template_name = 'list/professor_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Professores'
        return context

class ColegioListView(generic.ListView):
    model = models.Colegio
    template_name = 'list/colegio_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Colegios'
        return context


# Esse aqui vai ser para o admin poder alterar alguma coisa sobre a turma
# Quando digo admin, pode ser o admin do django ou o representante
class AdminTurmaListView(generic.ListView):
    model = models.Turma
    template_name = 'list/turma_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Turmas'
        return context

# Esse vai ser um exemplo de lista do ponto de vista do aluno
# Só vamos listar as turmas que o aluno está presente
class TurmaListView(generic.ListView):
    model = models.Turma
    template_name = 'list/turma_list.html'

    # Este é o método para fazer o filtro
    def get_queryset(self):
        # Este é um exemplo de quando só vai trazer a turma que o representante
        # é o usuário que está logado
        # self.object_list = models.Turma.objects.filter(
        #     representante=self.request.user)

        # Quando tem uma relação N para N traz todos as turmas desde que
        # o usuário seja um dos alunos matriculados nela
        self.object_list = models.Turma.objects.filter(
            alunos=self.request.user)
        return self.object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Turmas'
        return context

class MateriaListView(generic.ListView):
    model = models.Materia
    template_name = 'list/materia_list.html'

    def get_context_data(selfself, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Matérias'
        return context

class AtendimentoListView(generic.ListView):
    model = models.Atendimento
    template_name = 'list/atendimento_list.html'

    def get_context_data(selfself, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Atendimentos'
        return context

# Esta vai servir para trazer todos os avisos para o admin/representante
class AdminAvisoListView(generic.ListView):
    model = models.Aviso
    template_name = 'list/aviso_list.html'

    def get_context_data(selfself, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Avisos'
        return context

# Este só vai trazer os avisos das turmas que o usuário logado (aluno) está
class AvisoListView(generic.ListView):
    model = models.Aviso
    template_name = 'list/aviso_list.html'

    # Este é o método para fazer o filtro
    def get_queryset(self):
        # Neste caso vai buscar os avisos somente quando a turma desse aviso
        # tem o usuário logado como um dos alunos, por isso:
        # turma__alunos
        # O __ consegue buscar a relação turmaXaviso
        self.object_list = models.Aviso.objects.filter(
            turma__alunos=self.request.user)

        return self.object_list

    def get_context_data(selfself, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Avisos'
        return context


#---------------- DetailView ---------------------#
class TurmaDetailView(LoginRequiredMixin, DetailView): #Tela de crianção de turmas
    model = models.Turma
    template_name = 'detail/turma.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['titulo'] = self[0].nome
        context['avisos'] = models.Aviso.objects.filter(turma=self.kwargs['pk'])
        context['materias_seg'] = models.Materia.objects.filter(turma=self.kwargs['pk'],dia='Seg').order_by('horario_inicio')
        context['materias_ter'] = models.Materia.objects.filter(turma=self.kwargs['pk'],dia='Ter').order_by('horario_inicio')
        context['materias_qua'] = models.Materia.objects.filter(turma=self.kwargs['pk'],dia='Qua').order_by('horario_inicio')
        context['materias_qui'] = models.Materia.objects.filter(turma=self.kwargs['pk'],dia='Qui').order_by('horario_inicio')
        context['materias_sex'] = models.Materia.objects.filter(turma=self.kwargs['pk'],dia='Sex').order_by('horario_inicio')
        context['atendimentos'] = models.Atendimento.objects.filter(turma=self.kwargs['pk'])
        return context


#---------------- TemplateView -------------------#



class TurmasTemplateView(LoginRequiredMixin, TemplateView): #Tela de turmas do disponiveis para o usuario - pos login
    template_name = 'turmas.html'
    login_url = '/login/'

    # Como enviar outros dados para tela
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Listar somente a turma
        context['turmas'] = models.Turma.objects.all()
        context['titulo'] = 'Lista de Turmas'
        return context


#-----------------lixo---------------#