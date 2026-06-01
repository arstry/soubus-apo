from src.application.processador_dados import ProcessadorDados
from src.application.view_model import InputViewModel, ResultadoViewModel
from src.data.gerenciador_autenticacao import GerenciadorAutenticacao
from src.data.gerenciador_json_dados import GerenciadorJsonDados
from src.application.view.tela_resultados import TelaResultados


class MainIntegrador:
    def __init__(self) -> None:
        self._repositorio: GerenciadorJsonDados | None = None
        self._autenticador: GerenciadorAutenticacao | None = None
        self._processador: ProcessadorDados | None = None
        self._input_view_model: InputViewModel | None = None
        self._resultado_view_model: ResultadoViewModel | None = None
        self._tela_entrada: object | None = None
        self._tela_resultados: TelaResultados | None = None

    def iniciar_aplicacao(self) -> None:
        self._repositorio = GerenciadorJsonDados()
        self._autenticador = GerenciadorAutenticacao()
        self._processador = ProcessadorDados()

        self._input_view_model = InputViewModel(
            repositorio=self._repositorio,
            processador=self._processador,
        )
        self._resultado_view_model = ResultadoViewModel(
            repositorio=self._repositorio,
            autenticador=self._autenticador,
        )

    @property
    def input_view_model(self) -> InputViewModel:
        if self._input_view_model is None:
            raise RuntimeError(
                "MainIntegrador não foi inicializado. Chame iniciar_aplicacao() primeiro."
            )
        return self._input_view_model

    @property
    def resultado_view_model(self) -> ResultadoViewModel:
        if self._resultado_view_model is None:
            raise RuntimeError(
                "MainIntegrador não foi inicializado. Chame iniciar_aplicacao() primeiro."
            )
        return self._resultado_view_model

    @property
    def tela_entrada(self) -> object:
        if self._tela_entrada is None:
            if self._input_view_model is None:
                raise RuntimeError(
                    "MainIntegrador não foi inicializado. Chame iniciar_aplicacao() primeiro."
                )
            from src.application.view.tela_entrada import TelaEntrada
            self._tela_entrada = TelaEntrada(view_model=self._input_view_model)
        return self._tela_entrada

    @property
    def tela_resultados(self) -> TelaResultados:
        if self._tela_resultados is None:
            if self._resultado_view_model is None:
                raise RuntimeError(
                    "MainIntegrador não foi inicializado. Chame iniciar_aplicacao() primeiro."
                )
            self._tela_resultados = TelaResultados(view_model=self._resultado_view_model)
        return self._tela_resultados